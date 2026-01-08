"""Fintech customer chatbot endpoint logic using AWS Bedrock"""
import os
import json
import boto3
from shared.responses import _resp, decimal_default


# Initialize Bedrock client
bedrock = boto3.client("bedrock-runtime", region_name=os.environ.get("BEDROCK_REGION", "us-east-1"))
BEDROCK_MODEL_ID = os.environ.get("BEDROCK_MODEL_ID", "anthropic.claude-3-5-sonnet-20240620-v1:0")

# Tool definitions for customer-facing fintech chatbot
CUSTOMER_TOOLS = [
    {
        "name": "search_my_accounts",
        "description": "Search your accounts by type or status",
        "input_schema": {
            "type": "object",
            "properties": {
                "account_type": {"type": "string", "description": "Account type (checking, savings, investment, etc.)"},
                "status": {"type": "string", "enum": ["ACTIVE", "CLOSED"]}
            }
        }
    },
    {
        "name": "get_account_details",
        "description": "Get details of a specific account",
        "input_schema": {
            "type": "object",
            "properties": {
                "account_id": {"type": "string", "description": "Account ID"}
            },
            "required": ["account_id"]
        }
    },
    {
        "name": "search_my_transactions",
        "description": "Search your transactions by date or amount",
        "input_schema": {
            "type": "object",
            "properties": {
                "date": {"type": "string", "description": "Transaction date (YYYY-MM-DD)"},
                "min_amount": {"type": "number", "description": "Minimum transaction amount"}
            }
        }
    },
    {
        "name": "search_my_loans",
        "description": "Search your loans by type or status",
        "input_schema": {
            "type": "object",
            "properties": {
                "loan_type": {"type": "string", "description": "Loan type (personal, mortgage, auto, business)"},
                "status": {"type": "string", "enum": ["ACTIVE", "PAID_OFF"]}
            }
        }
    },
    {
        "name": "view_my_cards",
        "description": "View your credit and debit cards",
        "input_schema": {
            "type": "object",
            "properties": {
                "card_type": {"type": "string", "description": "Card type (credit, debit)"},
                "status": {"type": "string", "enum": ["ACTIVE", "BLOCKED", "EXPIRED"]}
            }
        }
    }
]


def execute_customer_tool(tool_name, tool_input, storage, customer_email):
    """Execute a customer-scoped tool call and return results"""
    # Get customer by email using GSI
    customers = storage.query_by_email("customer", customer_email)
    if not customers:
        return {"error": "Customer record not found"}

    customer = customers[0]
    customer_id = customer["id"]

    if tool_name == "search_my_accounts":
        # Query accounts by customerId (stored as customerId in DynamoDB)
        items = storage.query_by_customer_id("account", customer_id)

        print(f"[DEBUG] search_my_accounts: customer_id='{customer_id}', total_accounts={len(items)}")

        # Filter by additional criteria
        if tool_input.get("account_type"):
            account_type = tool_input["account_type"].lower()
            items = [i for i in items if account_type in i.get("data", {}).get("accountType", "").lower()]
        if tool_input.get("status"):
            items = [i for i in items if tool_input["status"] == i.get("status")]
            print(f"[DEBUG] After status filter ({tool_input['status']}): {len(items)} accounts")

        return {"accounts": items[:10], "count": len(items)}

    elif tool_name == "get_account_details":
        account_id = tool_input["account_id"]
        item = storage.get("account", account_id)

        if not item:
            return {"error": "Account not found"}

        # Verify ownership (check both customerId in data and top-level)
        if item.get("data", {}).get("customerId") != customer_id and item.get("customerId") != customer_id:
            return {"error": "Access denied"}

        return {"account": item}

    elif tool_name == "search_my_transactions":
        # Query transactions by customerId (stored as customerId in DynamoDB)
        items = storage.query_by_customer_id("transaction", customer_id)

        print(f"[DEBUG] search_my_transactions: customer_id='{customer_id}', total_transactions={len(items)}")

        # Filter by criteria
        if tool_input.get("date"):
            date = tool_input["date"]
            items = [i for i in items if date in i.get("data", {}).get("date", "")]
        if tool_input.get("min_amount"):
            min_amount = tool_input["min_amount"]
            items = [i for i in items if float(i.get("data", {}).get("amount", 0)) >= min_amount]

        return {"transactions": items[:10], "count": len(items)}

    elif tool_name == "search_my_loans":
        # Query loans by customerId (stored as customerId in DynamoDB)
        items = storage.query_by_customer_id("loan", customer_id)

        print(f"[DEBUG] search_my_loans: customer_id='{customer_id}', total_loans={len(items)}")

        # Filter by criteria
        if tool_input.get("loan_type"):
            loan_type = tool_input["loan_type"].lower()
            items = [i for i in items if loan_type in i.get("data", {}).get("loanType", "").lower()]
        if tool_input.get("status"):
            items = [i for i in items if tool_input["status"] == i.get("status")]

        return {"loans": items[:10], "count": len(items)}

    elif tool_name == "view_my_cards":
        # Get all accounts for this customer first
        accounts = storage.query_by_customer_id("account", customer_id)
        account_ids = [acc["id"] for acc in accounts]

        # Get all cards and filter by account IDs
        all_cards = storage.scan("card")
        items = [c for c in all_cards if c.get("data", {}).get("accountId") in account_ids]

        print(f"[DEBUG] view_my_cards: customer_id='{customer_id}', total_cards={len(items)}")

        # Filter by criteria
        if tool_input.get("card_type"):
            card_type = tool_input["card_type"].lower()
            items = [i for i in items if card_type in i.get("data", {}).get("cardType", "").lower()]
        if tool_input.get("status"):
            items = [i for i in items if tool_input["status"] == i.get("status")]

        return {"cards": items[:10], "count": len(items)}

    return {"error": "Unknown tool"}


def handle_customer_chat(event, storage):
    """Handle customer chatbot requests with tool use"""
    try:
        body = json.loads(event.get("body", "{}"))
        user_message = body.get("message", "")
        customer_email = body.get("customerEmail", "")  # Using customerEmail for consistency
        conversation_history = body.get("history", [])

        if not user_message:
            return _resp(400, {"error": "Message is required"})

        if not customer_email:
            return _resp(400, {"error": "Customer email is required"})

        # Build messages array
        messages = conversation_history + [{"role": "user", "content": user_message}]

        # System prompt
        system_prompt = f"""You are a helpful customer assistant for Silvermoat Financial Services.
You are helping a customer with email: {customer_email}
You can help them view their accounts, transactions, loans, and cards.
Use the available tools to search and retrieve information when needed.
Be professional, friendly, and helpful in your responses.
Remember to protect customer privacy and only show information for this specific customer."""

        # Call Bedrock with tool use
        response = bedrock.converse(
            modelId=BEDROCK_MODEL_ID,
            messages=messages,
            system=[{"text": system_prompt}],
            toolConfig={"tools": [{"toolSpec": tool} for tool in CUSTOMER_TOOLS]},
            inferenceConfig={"maxTokens": 2000, "temperature": 0.7}
        )

        # Process response
        output_message = response["output"]["message"]
        stop_reason = response["stopReason"]

        # Handle tool use
        if stop_reason == "tool_use":
            # Execute tools and get results
            tool_results = []
            for content_block in output_message["content"]:
                if "toolUse" in content_block:
                    tool_use = content_block["toolUse"]
                    tool_name = tool_use["name"]
                    tool_input = tool_use["input"]
                    tool_use_id = tool_use["toolUseId"]

                    # Execute tool with customer email scope
                    result = execute_customer_tool(tool_name, tool_input, storage, customer_email)

                    tool_results.append({
                        "toolResult": {
                            "toolUseId": tool_use_id,
                            "content": [{"json": result}]
                        }
                    })

            # Continue conversation with tool results
            messages.append(output_message)
            messages.append({"role": "user", "content": tool_results})

            # Get final response
            final_response = bedrock.converse(
                modelId=BEDROCK_MODEL_ID,
                messages=messages,
                system=[{"text": system_prompt}],
                toolConfig={"tools": [{"toolSpec": tool} for tool in CUSTOMER_TOOLS]},
                inferenceConfig={"maxTokens": 2000, "temperature": 0.7}
            )

            output_message = final_response["output"]["message"]

        # Extract text response
        response_text = ""
        for content_block in output_message["content"]:
            if "text" in content_block:
                response_text = content_block["text"]
                break

        return _resp(200, {
            "response": response_text,
            "history": messages
        })

    except Exception as e:
        print(f"Error in customer chatbot handler: {str(e)}")
        return _resp(500, {"error": str(e)})
