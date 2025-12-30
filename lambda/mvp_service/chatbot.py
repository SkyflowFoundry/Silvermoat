"""Chatbot endpoint logic using AWS Bedrock"""
import os
import json
import boto3
from shared.responses import _resp, decimal_default
from shared.storage import DynamoDBBackend


# Initialize Bedrock client
bedrock = boto3.client("bedrock-runtime", region_name=os.environ.get("BEDROCK_REGION", "us-east-1"))
BEDROCK_MODEL_ID = os.environ.get("BEDROCK_MODEL_ID", "anthropic.claude-3-5-sonnet-20240620-v1:0")

# Tool definitions for Claude
TOOLS = [
    {
        "name": "search_quotes",
        "description": "Search insurance quotes by customer name or ZIP code",
        "input_schema": {
            "type": "object",
            "properties": {
                "name": {"type": "string", "description": "Customer name to search for"},
                "zip": {"type": "string", "description": "ZIP code to search for"}
            }
        }
    },
    {
        "name": "search_policies",
        "description": "Search insurance policies by policy number, holder name, or status",
        "input_schema": {
            "type": "object",
            "properties": {
                "policy_number": {"type": "string", "description": "Policy number"},
                "holder_name": {"type": "string", "description": "Policy holder name"},
                "status": {"type": "string", "enum": ["ACTIVE", "EXPIRED", "CANCELLED"]}
            }
        }
    },
    {
        "name": "search_claims",
        "description": "Search insurance claims by claim number, claimant name, or status",
        "input_schema": {
            "type": "object",
            "properties": {
                "claim_number": {"type": "string", "description": "Claim number"},
                "claimant_name": {"type": "string", "description": "Claimant name"},
                "status": {"type": "string", "enum": ["PENDING", "REVIEW", "APPROVED", "DENIED"]}
            }
        }
    },
    {
        "name": "search_payments",
        "description": "Search payments by policy ID or status",
        "input_schema": {
            "type": "object",
            "properties": {
                "policy_id": {"type": "string", "description": "Related policy ID"},
                "status": {"type": "string", "enum": ["PENDING", "COMPLETED", "FAILED"]}
            }
        }
    },
    {
        "name": "search_cases",
        "description": "Search cases by title, assignee, priority, or status",
        "input_schema": {
            "type": "object",
            "properties": {
                "title": {"type": "string", "description": "Case title keywords"},
                "assignee": {"type": "string", "description": "Assigned employee name"},
                "priority": {"type": "string", "enum": ["LOW", "MEDIUM", "HIGH"]},
                "status": {"type": "string", "enum": ["OPEN", "IN_PROGRESS", "RESOLVED", "CLOSED"]}
            }
        }
    },
    {
        "name": "get_entity_details",
        "description": "Get full details of a specific quote, policy, claim, payment, or case by ID",
        "input_schema": {
            "type": "object",
            "properties": {
                "entity_type": {"type": "string", "enum": ["quote", "policy", "claim", "payment", "case"]},
                "entity_id": {"type": "string", "description": "The unique ID of the entity"}
            },
            "required": ["entity_type", "entity_id"]
        }
    }
]


def execute_tool(tool_name, tool_input, storage):
    """Execute a tool call and return results"""

    if tool_name == "search_quotes":
        items = storage.scan("quote")

        # Filter by name or zip if provided
        if tool_input.get("name"):
            name_lower = tool_input["name"].lower()
            items = [i for i in items if name_lower in i.get("data", {}).get("name", "").lower()]
        if tool_input.get("zip"):
            items = [i for i in items if tool_input["zip"] == i.get("data", {}).get("zip")]

        return {"quotes": items[:10], "count": len(items)}

    elif tool_name == "search_policies":
        items = storage.scan("policy")

        # Filter by criteria
        if tool_input.get("policy_number"):
            pn = tool_input["policy_number"].lower()
            items = [i for i in items if pn in i.get("data", {}).get("policyNumber", "").lower()]
        if tool_input.get("holder_name"):
            hn = tool_input["holder_name"].lower()
            items = [i for i in items if hn in i.get("data", {}).get("holderName", "").lower()]
        if tool_input.get("status"):
            items = [i for i in items if tool_input["status"] == i.get("data", {}).get("status")]

        return {"policies": items[:10], "count": len(items)}

    elif tool_name == "search_claims":
        items = storage.scan("claim")

        # Filter by criteria
        if tool_input.get("claim_number"):
            cn = tool_input["claim_number"].lower()
            items = [i for i in items if cn in i.get("data", {}).get("claimNumber", "").lower()]
        if tool_input.get("claimant_name"):
            cn = tool_input["claimant_name"].lower()
            items = [i for i in items if cn in i.get("data", {}).get("claimantName", "").lower()]
        if tool_input.get("status"):
            items = [i for i in items if tool_input["status"] == i.get("status")]

        return {"claims": items[:10], "count": len(items)}

    elif tool_name == "search_payments":
        items = storage.scan("payment")

        # Filter by criteria
        if tool_input.get("policy_id"):
            items = [i for i in items if tool_input["policy_id"] == i.get("data", {}).get("policyId")]
        if tool_input.get("status"):
            items = [i for i in items if tool_input["status"] == i.get("data", {}).get("status")]

        return {"payments": items[:10], "count": len(items)}

    elif tool_name == "search_cases":
        items = storage.scan("case")

        # Filter by criteria
        if tool_input.get("title"):
            title = tool_input["title"].lower()
            items = [i for i in items if title in i.get("data", {}).get("title", "").lower()]
        if tool_input.get("assignee"):
            assignee = tool_input["assignee"].lower()
            items = [i for i in items if assignee in i.get("data", {}).get("assignee", "").lower()]
        if tool_input.get("priority"):
            items = [i for i in items if tool_input["priority"] == i.get("data", {}).get("priority")]
        if tool_input.get("status"):
            items = [i for i in items if tool_input["status"] == i.get("data", {}).get("status")]

        return {"cases": items[:10], "count": len(items)}

    elif tool_name == "get_entity_details":
        entity_type = tool_input["entity_type"]
        entity_id = tool_input["entity_id"]

        item = storage.get(entity_type, entity_id)
        if not item:
            return {"error": f"{entity_type} not found"}

        return {entity_type: item}

    return {"error": "Unknown tool"}


def handle_chat(event, storage):
    """Handle POST /chat endpoint"""
    try:
        body = json.loads(event.get("body", "{}"))
        user_message = body.get("message", "")
        conversation_history = body.get("history", [])

        if not user_message:
            return _resp(400, {"error": "message_required", "message": "Message is required"})

        # Build messages for Claude
        messages = conversation_history + [{"role": "user", "content": user_message}]

        # System prompt for insurance assistant
        system_prompt = "You are a helpful AI assistant for Silvermoat Insurance employees. You help employees search customer data, fill forms, and generate reports. When users ask about customers, policies, or claims, use the available tools to search the database. Be professional, concise, and accurate. Format data clearly for insurance context. When helping with forms, provide structured data that can pre-fill form fields."

        # Invoke Bedrock with tool use
        response = bedrock.invoke_model(
            modelId=BEDROCK_MODEL_ID,
            body=json.dumps({
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 4096,
                "system": system_prompt,
                "messages": messages,
                "tools": TOOLS,
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

                    # Execute the tool
                    result = execute_tool(tool_name, tool_input, storage)

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
                    "tools": TOOLS,
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
        print(f"Chat error: {str(e)}")
        return _resp(500, {"error": "chat_error", "message": str(e)})
