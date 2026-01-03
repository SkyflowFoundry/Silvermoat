"""Customer chatbot endpoint logic using AWS Bedrock"""
import os
import json
import boto3
from shared.responses import _resp, decimal_default
from shared.storage import DynamoDBBackend


# Initialize Bedrock client
bedrock = boto3.client("bedrock-runtime", region_name=os.environ.get("BEDROCK_REGION", "us-east-1"))
BEDROCK_MODEL_ID = os.environ.get("BEDROCK_MODEL_ID", "anthropic.claude-3-5-sonnet-20240620-v1:0")

# Tool definitions for customer-facing chatbot
CUSTOMER_TOOLS = [
    {
        "name": "search_my_policies",
        "description": "Search your insurance policies by policy number or status",
        "input_schema": {
            "type": "object",
            "properties": {
                "policy_number": {"type": "string", "description": "Policy number"},
                "status": {"type": "string", "enum": ["ACTIVE", "EXPIRED", "CANCELLED"]}
            }
        }
    },
    {
        "name": "search_my_claims",
        "description": "Search your insurance claims by claim number or status",
        "input_schema": {
            "type": "object",
            "properties": {
                "claim_number": {"type": "string", "description": "Claim number"},
                "status": {"type": "string", "enum": ["PENDING", "REVIEW", "APPROVED", "DENIED"]}
            }
        }
    },
    {
        "name": "search_my_payments",
        "description": "Search your payments by status",
        "input_schema": {
            "type": "object",
            "properties": {
                "status": {"type": "string", "enum": ["PENDING", "COMPLETED", "FAILED"]}
            }
        }
    },
    {
        "name": "get_my_entity_details",
        "description": "Get full details of a specific policy, claim, or payment by ID",
        "input_schema": {
            "type": "object",
            "properties": {
                "entity_type": {"type": "string", "enum": ["policy", "claim", "payment"]},
                "entity_id": {"type": "string", "description": "The unique ID of the entity"}
            },
            "required": ["entity_type", "entity_id"]
        }
    }
]


def execute_customer_tool(tool_name, tool_input, storage, customer_email):
    """Execute a customer-scoped tool call and return results"""

    if tool_name == "search_my_policies":
        items = storage.scan("policy")

        # Filter by customer email
        items = [i for i in items if i.get("data", {}).get("customer_email") == customer_email]

        # Filter by additional criteria
        if tool_input.get("policy_number"):
            pn = tool_input["policy_number"].lower()
            items = [i for i in items if pn in i.get("data", {}).get("policyNumber", "").lower()]
        if tool_input.get("status"):
            items = [i for i in items if tool_input["status"] == i.get("status")]

        return {"policies": items[:10], "count": len(items)}

    elif tool_name == "search_my_claims":
        # Get customer's policy IDs
        policies = storage.scan("policy")
        policy_ids = [p["id"] for p in policies if p.get("data", {}).get("customer_email") == customer_email]

        # Get all claims
        items = storage.scan("claim")

        # Filter by customer's policies
        items = [i for i in items if i.get("data", {}).get("policy_id") in policy_ids]

        # Filter by criteria
        if tool_input.get("claim_number"):
            cn = tool_input["claim_number"].lower()
            items = [i for i in items if cn in i.get("data", {}).get("claimNumber", "").lower()]
        if tool_input.get("status"):
            items = [i for i in items if tool_input["status"] == i.get("status")]

        return {"claims": items[:10], "count": len(items)}

    elif tool_name == "search_my_payments":
        # Get customer's policy IDs
        policies = storage.scan("policy")
        policy_ids = [p["id"] for p in policies if p.get("data", {}).get("customer_email") == customer_email]

        # Get all payments
        items = storage.scan("payment")

        # Filter by customer's policies
        items = [i for i in items if i.get("data", {}).get("policy_id") in policy_ids]

        # Filter by criteria
        if tool_input.get("status"):
            items = [i for i in items if tool_input["status"] == i.get("status")]

        return {"payments": items[:10], "count": len(items)}

    elif tool_name == "get_my_entity_details":
        entity_type = tool_input["entity_type"]
        entity_id = tool_input["entity_id"]

        item = storage.get(entity_type, entity_id)
        if not item:
            return {"error": f"{entity_type} not found"}

        # Verify ownership
        if entity_type == "policy":
            if item.get("data", {}).get("customer_email") != customer_email:
                return {"error": "Access denied"}
        elif entity_type in ["claim", "payment"]:
            # Get customer's policy IDs
            policies = storage.scan("policy")
            policy_ids = [p["id"] for p in policies if p.get("data", {}).get("customer_email") == customer_email]

            if item.get("data", {}).get("policy_id") not in policy_ids:
                return {"error": "Access denied"}

        return {entity_type: item}

    return {"error": "Unknown tool"}


def handle_customer_chat(event, storage):
    """Handle POST /customer-chat endpoint"""
    try:
        body = json.loads(event.get("body", "{}"))
        user_message = body.get("message", "")
        conversation_history = body.get("history", [])
        customer_email = body.get("customerEmail", "")

        if not user_message:
            return _resp(400, {"error": "message_required", "message": "Message is required"})

        if not customer_email:
            return _resp(400, {"error": "customer_email_required", "message": "Customer email is required for customer chat"})

        # Build messages for Claude
        messages = conversation_history + [{"role": "user", "content": user_message}]

        # System prompt for customer assistant
        system_prompt = f"You are a helpful AI assistant for Silvermoat Insurance customers. You help customers view their policies, track claims, and check payment history. The customer you're assisting is {customer_email}. When customers ask about their insurance information, use the available tools to search their data. Be professional, friendly, and accurate. Format data clearly. Only show information that belongs to this customer."

        # Invoke Bedrock with tool use
        response = bedrock.invoke_model(
            modelId=BEDROCK_MODEL_ID,
            body=json.dumps({
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 4096,
                "system": system_prompt,
                "messages": messages,
                "tools": CUSTOMER_TOOLS,
                "temperature": 0.7
            })
        )

        response_body = json.loads(response["body"].read())

        # Handle tool use loop
        while response_body.get("stop_reason") == "tool_use":
            # Extract tool calls
            assistant_message = {
                "role": "assistant",
                "content": response_body["content"]
            }
            messages.append(assistant_message)

            # Execute tools
            tool_results = []
            for content_block in response_body["content"]:
                if content_block["type"] == "tool_use":
                    tool_name = content_block["name"]
                    tool_input = content_block["input"]
                    tool_use_id = content_block["id"]

                    # Execute the tool with customer email filtering
                    result = execute_customer_tool(tool_name, tool_input, storage, customer_email)

                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": tool_use_id,
                        "content": json.dumps(result, default=decimal_default)
                    })

            # Send tool results back to Claude
            messages.append({
                "role": "user",
                "content": tool_results
            })

            # Continue conversation
            response = bedrock.invoke_model(
                modelId=BEDROCK_MODEL_ID,
                body=json.dumps({
                    "anthropic_version": "bedrock-2023-05-31",
                    "max_tokens": 4096,
                    "system": system_prompt,
                    "messages": messages,
                    "tools": CUSTOMER_TOOLS,
                    "temperature": 0.7
                })
            )

            response_body = json.loads(response["body"].read())

        # Extract final response
        assistant_content = response_body["content"]
        text_content = next((block["text"] for block in assistant_content if block["type"] == "text"), "")

        return _resp(200, {
            "response": text_content,
            "usage": response_body.get("usage", {}),
            "conversation": messages + [{"role": "assistant", "content": assistant_content}]
        })

    except Exception as e:
        print(f"Customer chat error: {str(e)}")
        return _resp(500, {"error": "chat_error", "message": str(e)})
