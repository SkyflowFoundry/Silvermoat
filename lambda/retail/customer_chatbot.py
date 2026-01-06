"""Retail customer chatbot endpoint logic using AWS Bedrock"""
import os
import json
import boto3
from shared.responses import _resp, decimal_default


# Initialize Bedrock client
bedrock = boto3.client("bedrock-runtime", region_name=os.environ.get("BEDROCK_REGION", "us-east-1"))
BEDROCK_MODEL_ID = os.environ.get("BEDROCK_MODEL_ID", "anthropic.claude-3-5-sonnet-20240620-v1:0")

# Tool definitions for customer-facing retail chatbot
CUSTOMER_TOOLS = [
    {
        "name": "search_my_orders",
        "description": "Search your orders by order number or status",
        "input_schema": {
            "type": "object",
            "properties": {
                "order_number": {"type": "string", "description": "Order number"},
                "status": {"type": "string", "enum": ["PENDING", "PROCESSING", "SHIPPED", "DELIVERED", "CANCELLED"]}
            }
        }
    },
    {
        "name": "track_order",
        "description": "Get tracking information for a specific order",
        "input_schema": {
            "type": "object",
            "properties": {
                "order_id": {"type": "string", "description": "Order ID to track"}
            },
            "required": ["order_id"]
        }
    },
    {
        "name": "browse_products",
        "description": "Browse available products by category or search term",
        "input_schema": {
            "type": "object",
            "properties": {
                "category": {"type": "string", "description": "Product category"},
                "search": {"type": "string", "description": "Search term"}
            }
        }
    }
]

# Domain mapping (retail → storage)
DOMAIN_MAPPING = {
    "product": "quote",
    "order": "policy",
    "customer": "customer"
}


def execute_customer_tool(tool_name, tool_input, storage, customer_email):
    """Execute a customer-scoped tool call and return results"""
    # Get customer by email using GSI
    customers = storage.query_by_email("customer", customer_email)
    if not customers:
        return {"error": "Customer not found"}

    customer = customers[0]
    customer_id = customer["id"]

    if tool_name == "search_my_orders":
        # Query orders by customerId using GSI
        items = storage.query_by_customer_id(DOMAIN_MAPPING["order"], customer_id)

        print(f"[DEBUG] search_my_orders: customer_id='{customer_id}', total_orders={len(items)}")

        # Filter by additional criteria
        if tool_input.get("order_number"):
            on = tool_input["order_number"].lower()
            items = [i for i in items if on in i.get("data", {}).get("orderNumber", "").lower()]
        if tool_input.get("status"):
            items = [i for i in items if tool_input["status"] == i.get("status")]
            print(f"[DEBUG] After status filter ({tool_input['status']}): {len(items)} orders")

        return {"orders": items[:10], "count": len(items)}

    elif tool_name == "track_order":
        order_id = tool_input["order_id"]
        item = storage.get(DOMAIN_MAPPING["order"], order_id)

        if not item:
            return {"error": "Order not found"}

        # Verify ownership
        if item.get("customerId") != customer_id:
            return {"error": "Access denied"}

        # Return order with tracking info
        return {"order": item}

    elif tool_name == "browse_products":
        # Get all active products
        items = storage.scan(DOMAIN_MAPPING["product"])
        items = [i for i in items if i.get("status") == "ACTIVE"]

        # Filter by criteria
        if tool_input.get("category"):
            cat = tool_input["category"].lower()
            items = [i for i in items if cat in i.get("data", {}).get("category", "").lower()]
        if tool_input.get("search"):
            search = tool_input["search"].lower()
            items = [i for i in items if
                    search in i.get("data", {}).get("name", "").lower() or
                    search in i.get("data", {}).get("description", "").lower()]

        return {"products": items[:20], "count": len(items)}

    return {"error": "Unknown tool"}


def handle_customer_chat(event, storage):
    """Handle POST /customer-chat endpoint for retail customers"""
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
        system_prompt = f"You are a helpful AI assistant for Silvermoat Retail customers. You help customers track their orders, browse products, and get support. The customer you're assisting is {customer_email}. When customers ask about their orders or want to browse products, use the available tools. Be professional, friendly, and helpful. Format data clearly. Only show information that belongs to this customer."

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
        print(f"Retail customer chat error: {str(e)}")
        return _resp(500, {"error": "chat_error", "message": str(e)})
