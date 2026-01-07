"""Healthcare staff chatbot endpoint logic using AWS Bedrock"""
import os
import json
import boto3
from shared.responses import _resp, decimal_default


# Initialize Bedrock client
bedrock = boto3.client("bedrock-runtime", region_name=os.environ.get("BEDROCK_REGION", "us-east-1"))
BEDROCK_MODEL_ID = os.environ.get("BEDROCK_MODEL_ID", "anthropic.claude-3-5-sonnet-20240620-v1:0")

# Tool definitions for healthcare staff assistant
TOOLS = [
    {
        "name": "search_appointments",
        "description": "Search appointments by patient name, date, or status",
        "input_schema": {
            "type": "object",
            "properties": {
                "patient_name": {"type": "string", "description": "Patient name"},
                "date": {"type": "string", "description": "Appointment date (YYYY-MM-DD)"},
                "status": {"type": "string", "enum": ["SCHEDULED", "COMPLETED", "CANCELLED", "NO_SHOW"]}
            }
        }
    },
    {
        "name": "search_medical_records",
        "description": "Search medical records by patient name, record type, or status",
        "input_schema": {
            "type": "object",
            "properties": {
                "patient_name": {"type": "string", "description": "Patient name"},
                "record_type": {"type": "string", "description": "Type of medical record (visit, lab, imaging, etc.)"},
                "status": {"type": "string", "enum": ["ACTIVE", "ARCHIVED"]}
            }
        }
    },
    {
        "name": "search_prescriptions",
        "description": "Search prescriptions by patient name, medication, or status",
        "input_schema": {
            "type": "object",
            "properties": {
                "patient_name": {"type": "string", "description": "Patient name"},
                "medication": {"type": "string", "description": "Medication name"},
                "status": {"type": "string", "enum": ["ACTIVE", "FILLED", "EXPIRED", "CANCELLED"]}
            }
        }
    },
    {
        "name": "search_billing",
        "description": "Search billing records by patient name or status",
        "input_schema": {
            "type": "object",
            "properties": {
                "patient_name": {"type": "string", "description": "Patient name"},
                "status": {"type": "string", "enum": ["PENDING", "PAID", "OVERDUE"]}
            }
        }
    },
    {
        "name": "search_cases",
        "description": "Search cases by title, patient, priority, or status",
        "input_schema": {
            "type": "object",
            "properties": {
                "title": {"type": "string", "description": "Case title keywords"},
                "patient_name": {"type": "string", "description": "Patient name"},
                "priority": {"type": "string", "enum": ["LOW", "MEDIUM", "HIGH"]},
                "status": {"type": "string", "enum": ["OPEN", "IN_PROGRESS", "RESOLVED", "CLOSED"]}
            }
        }
    },
    {
        "name": "get_entity_details",
        "description": "Get full details of a specific appointment, medical record, prescription, billing, or case by ID",
        "input_schema": {
            "type": "object",
            "properties": {
                "entity_type": {"type": "string", "enum": ["appointment", "medical_record", "prescription", "billing", "case"]},
                "entity_id": {"type": "string", "description": "The unique ID of the entity"}
            },
            "required": ["entity_type", "entity_id"]
        }
    }
]


def execute_tool(tool_name, tool_input, storage):
    """Execute a tool call and return results"""
    if tool_name == "search_appointments":
        items = storage.scan("appointment")

        # Filter by criteria
        if tool_input.get("patient_name"):
            name = tool_input["patient_name"].lower()
            items = [i for i in items if name in i.get("data", {}).get("patientName", "").lower()]
        if tool_input.get("date"):
            date = tool_input["date"]
            items = [i for i in items if date in i.get("data", {}).get("date", "")]
        if tool_input.get("status"):
            status = tool_input["status"]
            items = [i for i in items if i.get("status") == status]

        return {"results": items[:10], "count": len(items)}

    elif tool_name == "search_medical_records":
        items = storage.scan("medical_record")

        # Filter by criteria
        if tool_input.get("patient_name"):
            name = tool_input["patient_name"].lower()
            items = [i for i in items if name in i.get("data", {}).get("patientName", "").lower()]
        if tool_input.get("record_type"):
            record_type = tool_input["record_type"].lower()
            items = [i for i in items if record_type in i.get("data", {}).get("recordType", "").lower()]
        if tool_input.get("status"):
            status = tool_input["status"]
            items = [i for i in items if i.get("status") == status]

        return {"results": items[:10], "count": len(items)}

    elif tool_name == "search_prescriptions":
        items = storage.scan("prescription")

        # Filter by criteria
        if tool_input.get("patient_name"):
            name = tool_input["patient_name"].lower()
            items = [i for i in items if name in i.get("data", {}).get("patientName", "").lower()]
        if tool_input.get("medication"):
            medication = tool_input["medication"].lower()
            items = [i for i in items if medication in i.get("data", {}).get("medication", "").lower()]
        if tool_input.get("status"):
            status = tool_input["status"]
            items = [i for i in items if i.get("status") == status]

        return {"results": items[:10], "count": len(items)}

    elif tool_name == "search_billing":
        items = storage.scan("billing")

        # Filter by criteria
        if tool_input.get("patient_name"):
            name = tool_input["patient_name"].lower()
            items = [i for i in items if name in i.get("data", {}).get("patientName", "").lower()]
        if tool_input.get("status"):
            status = tool_input["status"]
            items = [i for i in items if i.get("status") == status]

        return {"results": items[:10], "count": len(items)}

    elif tool_name == "search_cases":
        items = storage.scan("case")

        # Filter by criteria
        if tool_input.get("title"):
            title_words = tool_input["title"].lower()
            items = [i for i in items if title_words in i.get("data", {}).get("title", "").lower()]
        if tool_input.get("patient_name"):
            name = tool_input["patient_name"].lower()
            items = [i for i in items if name in i.get("data", {}).get("patientName", "").lower()]
        if tool_input.get("priority"):
            priority = tool_input["priority"]
            items = [i for i in items if i.get("data", {}).get("priority") == priority]
        if tool_input.get("status"):
            status = tool_input["status"]
            items = [i for i in items if i.get("status") == status]

        return {"results": items[:10], "count": len(items)}

    elif tool_name == "get_entity_details":
        entity_type = tool_input["entity_type"]
        entity_id = tool_input["entity_id"]
        item = storage.get(entity_type, entity_id)
        if item:
            return {"entity": item}
        else:
            return {"error": "Entity not found"}

    return {"error": "Unknown tool"}


def handle_chat(event, storage):
    """Handle chatbot requests with tool use"""
    try:
        body = json.loads(event.get("body", "{}"))
        user_message = body.get("message", "")
        conversation_history = body.get("history", [])

        if not user_message:
            return _resp(400, {"error": "Message is required"})

        # Build messages array
        messages = conversation_history + [{"role": "user", "content": user_message}]

        # System prompt
        system_prompt = """You are a helpful healthcare staff assistant for Silvermoat Healthcare.
You can help staff search for appointments, medical records, prescriptions, billing records, and cases.
Use the available tools to search and retrieve information when needed.
Be professional, concise, and helpful in your responses."""

        # Call Bedrock with tool use
        response = bedrock.converse(
            modelId=BEDROCK_MODEL_ID,
            messages=messages,
            system=[{"text": system_prompt}],
            toolConfig={"tools": [{"toolSpec": tool} for tool in TOOLS]},
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

                    # Execute tool
                    result = execute_tool(tool_name, tool_input, storage)

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
                toolConfig={"tools": [{"toolSpec": tool} for tool in TOOLS]},
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
        print(f"Error in chatbot handler: {str(e)}")
        return _resp(500, {"error": str(e)})
