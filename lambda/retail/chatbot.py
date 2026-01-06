"""Retail employee chatbot endpoint logic using AWS Bedrock"""
import os
import json
import boto3
from shared.responses import _resp, decimal_default


# Initialize Bedrock client
bedrock = boto3.client("bedrock-runtime", region_name=os.environ.get("BEDROCK_REGION", "us-east-1"))
BEDROCK_MODEL_ID = os.environ.get("BEDROCK_MODEL_ID", "anthropic.claude-3-5-sonnet-20240620-v1:0")

# Tool definitions for retail assistant
TOOLS = [
    {
        "name": "search_products",
        "description": "Search products by SKU, name, category, or status",
        "input_schema": {
            "type": "object",
            "properties": {
                "sku": {"type": "string", "description": "Product SKU"},
                "name": {"type": "string", "description": "Product name"},
                "category": {"type": "string", "description": "Product category"},
                "status": {"type": "string", "enum": ["ACTIVE", "DISCONTINUED", "OUT_OF_STOCK"]}
            }
        }
    },
    {
        "name": "search_orders",
        "description": "Search orders by order number, customer name, or status",
        "input_schema": {
            "type": "object",
            "properties": {
                "order_number": {"type": "string", "description": "Order number"},
                "customer_name": {"type": "string", "description": "Customer name"},
                "status": {"type": "string", "enum": ["PENDING", "PROCESSING", "SHIPPED", "DELIVERED", "CANCELLED"]}
            }
        }
    },
    {
        "name": "search_inventory",
        "description": "Search inventory by location, product, or status",
        "input_schema": {
            "type": "object",
            "properties": {
                "location": {"type": "string", "description": "Warehouse location"},
                "product_id": {"type": "string", "description": "Product ID"},
                "status": {"type": "string", "enum": ["IN_STOCK", "LOW_STOCK", "OUT_OF_STOCK"]}
            }
        }
    },
    {
        "name": "search_cases",
        "description": "Search support cases by title, customer, priority, or status",
        "input_schema": {
            "type": "object",
            "properties": {
                "title": {"type": "string", "description": "Case title keywords"},
                "customer_name": {"type": "string", "description": "Customer name"},
                "priority": {"type": "string", "enum": ["LOW", "MEDIUM", "HIGH"]},
                "status": {"type": "string", "enum": ["OPEN", "IN_PROGRESS", "RESOLVED", "CLOSED"]}
            }
        }
    },
    {
        "name": "get_entity_details",
        "description": "Get full details of a specific product, order, inventory, or case by ID",
        "input_schema": {
            "type": "object",
            "properties": {
                "entity_type": {"type": "string", "enum": ["product", "order", "inventory", "case"]},
                "entity_id": {"type": "string", "description": "The unique ID of the entity"}
            },
            "required": ["entity_type", "entity_id"]
        }
    }
]

# Domain mapping (retail → storage)
DOMAIN_MAPPING = {
    "product": "quote",
    "order": "policy",
    "inventory": "claim",
    "case": "case"
}


def execute_tool(tool_name, tool_input, storage):
    """Execute a tool call and return results"""
    if tool_name == "search_products":
        items = storage.scan(DOMAIN_MAPPING["product"])

        # Filter by criteria
        if tool_input.get("sku"):
            sku = tool_input["sku"].lower()
            items = [i for i in items if sku in i.get("data", {}).get("sku", "").lower()]
        if tool_input.get("name"):
            name = tool_input["name"].lower()
            items = [i for i in items if name in i.get("data", {}).get("name", "").lower()]
        if tool_input.get("category"):
            cat = tool_input["category"].lower()
            items = [i for i in items if cat in i.get("data", {}).get("category", "").lower()]
        if tool_input.get("status"):
            items = [i for i in items if tool_input["status"] == i.get("status")]

        return {"products": items[:10], "count": len(items)}

    elif tool_name == "search_orders":
        items = storage.scan(DOMAIN_MAPPING["order"])

        # Filter by criteria
        if tool_input.get("order_number"):
            on = tool_input["order_number"].lower()
            items = [i for i in items if on in i.get("data", {}).get("orderNumber", "").lower()]
        if tool_input.get("customer_name"):
            cn = tool_input["customer_name"].lower()
            items = [i for i in items if cn in i.get("data", {}).get("customerName", "").lower()]
        if tool_input.get("status"):
            items = [i for i in items if tool_input["status"] == i.get("status")]

        return {"orders": items[:10], "count": len(items)}

    elif tool_name == "search_inventory":
        items = storage.scan(DOMAIN_MAPPING["inventory"])

        # Filter by criteria
        if tool_input.get("location"):
            loc = tool_input["location"].lower()
            items = [i for i in items if loc in i.get("data", {}).get("location", "").lower()]
        if tool_input.get("product_id"):
            items = [i for i in items if tool_input["product_id"] == i.get("data", {}).get("productId")]
        if tool_input.get("status"):
            items = [i for i in items if tool_input["status"] == i.get("status")]

        return {"inventory": items[:10], "count": len(items)}

    elif tool_name == "search_cases":
        items = storage.scan(DOMAIN_MAPPING["case"])

        # Filter by criteria
        if tool_input.get("title"):
            title = tool_input["title"].lower()
            items = [i for i in items if title in i.get("data", {}).get("title", "").lower()]
        if tool_input.get("customer_name"):
            cn = tool_input["customer_name"].lower()
            items = [i for i in items if cn in i.get("data", {}).get("customerName", "").lower()]
        if tool_input.get("priority"):
            items = [i for i in items if tool_input["priority"] == i.get("data", {}).get("priority")]
        if tool_input.get("status"):
            items = [i for i in items if tool_input["status"] == i.get("status")]

        return {"cases": items[:10], "count": len(items)}

    elif tool_name == "get_entity_details":
        entity_type = tool_input["entity_type"]
        entity_id = tool_input["entity_id"]

        storage_domain = DOMAIN_MAPPING.get(entity_type, entity_type)
        item = storage.get(storage_domain, entity_id)
        if not item:
            return {"error": f"{entity_type} not found"}

        return {entity_type: item}

    return {"error": "Unknown tool"}


def handle_chat(event, storage):
    """Handle POST /chat endpoint for retail employees"""
    try:
        body = json.loads(event.get("body", "{}"))
        user_message = body.get("message", "")
        conversation_history = body.get("history", [])

        if not user_message:
            return _resp(400, {"error": "message_required", "message": "Message is required"})

        # Build messages for Claude
        messages = conversation_history + [{"role": "user", "content": user_message}]

        # System prompt for retail assistant
        system_prompt = "You are a helpful AI assistant for Silvermoat Retail employees. You help employees search products, manage inventory, track orders, and handle customer support cases. When users ask about products, orders, or inventory, use the available tools to search the database. Be professional, concise, and accurate. Format data clearly for retail context. When helping with forms, provide structured data that can pre-fill form fields."

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
        print(f"Retail chat error: {str(e)}")
        return _resp(500, {"error": "chat_error", "message": str(e)})
