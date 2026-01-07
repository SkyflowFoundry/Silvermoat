"""Healthcare patient chatbot endpoint logic using AWS Bedrock"""
import os
import json
import boto3
from shared.responses import _resp, decimal_default


# Initialize Bedrock client
bedrock = boto3.client("bedrock-runtime", region_name=os.environ.get("BEDROCK_REGION", "us-east-1"))
BEDROCK_MODEL_ID = os.environ.get("BEDROCK_MODEL_ID", "anthropic.claude-3-5-sonnet-20240620-v1:0")

# Tool definitions for patient-facing healthcare chatbot
CUSTOMER_TOOLS = [
    {
        "name": "search_my_appointments",
        "description": "Search your appointments by date or status",
        "input_schema": {
            "type": "object",
            "properties": {
                "date": {"type": "string", "description": "Appointment date (YYYY-MM-DD)"},
                "status": {"type": "string", "enum": ["SCHEDULED", "COMPLETED", "CANCELLED"]}
            }
        }
    },
    {
        "name": "get_appointment_details",
        "description": "Get details of a specific appointment",
        "input_schema": {
            "type": "object",
            "properties": {
                "appointment_id": {"type": "string", "description": "Appointment ID"}
            },
            "required": ["appointment_id"]
        }
    },
    {
        "name": "search_my_prescriptions",
        "description": "Search your prescriptions by medication name or status",
        "input_schema": {
            "type": "object",
            "properties": {
                "medication": {"type": "string", "description": "Medication name"},
                "status": {"type": "string", "enum": ["ACTIVE", "FILLED", "EXPIRED"]}
            }
        }
    },
    {
        "name": "view_billing",
        "description": "View your billing statements and payment history",
        "input_schema": {
            "type": "object",
            "properties": {
                "status": {"type": "string", "enum": ["PENDING", "PAID", "OVERDUE"]}
            }
        }
    }
]


def execute_customer_tool(tool_name, tool_input, storage, patient_email):
    """Execute a patient-scoped tool call and return results"""
    # Get patient by email using GSI
    patients = storage.query_by_email("patient", patient_email)
    if not patients:
        return {"error": "Patient record not found"}

    patient = patients[0]
    patient_id = patient["id"]

    if tool_name == "search_my_appointments":
        # Note: appointments use customerId in GSI even though we call it patientId
        # Query appointments by patientId (stored as customerId in DynamoDB)
        items = storage.query_by_customer_id("appointment", patient_id)

        print(f"[DEBUG] search_my_appointments: patient_id='{patient_id}', total_appointments={len(items)}")

        # Filter by additional criteria
        if tool_input.get("date"):
            date = tool_input["date"]
            items = [i for i in items if date in i.get("data", {}).get("date", "")]
        if tool_input.get("status"):
            items = [i for i in items if tool_input["status"] == i.get("status")]
            print(f"[DEBUG] After status filter ({tool_input['status']}): {len(items)} appointments")

        return {"appointments": items[:10], "count": len(items)}

    elif tool_name == "get_appointment_details":
        appointment_id = tool_input["appointment_id"]
        item = storage.get("appointment", appointment_id)

        if not item:
            return {"error": "Appointment not found"}

        # Verify ownership (check both patientId and customerId for compatibility)
        if item.get("data", {}).get("patientId") != patient_id and item.get("customerId") != patient_id:
            return {"error": "Access denied"}

        return {"appointment": item}

    elif tool_name == "search_my_prescriptions":
        # Query prescriptions by patientId (stored as customerId in DynamoDB)
        items = storage.query_by_customer_id("prescription", patient_id)

        print(f"[DEBUG] search_my_prescriptions: patient_id='{patient_id}', total_prescriptions={len(items)}")

        # Filter by criteria
        if tool_input.get("medication"):
            medication = tool_input["medication"].lower()
            items = [i for i in items if medication in i.get("data", {}).get("medication", "").lower()]
        if tool_input.get("status"):
            items = [i for i in items if tool_input["status"] == i.get("status")]

        return {"prescriptions": items[:10], "count": len(items)}

    elif tool_name == "view_billing":
        # Get all medical records for this patient first
        medical_records = storage.query_by_customer_id("medical_record", patient_id)
        medical_record_ids = [mr["id"] for mr in medical_records]

        # Get all billing records and filter by medical record IDs
        all_billing = storage.scan("billing")
        items = [b for b in all_billing if b.get("data", {}).get("medicalRecordId") in medical_record_ids]

        print(f"[DEBUG] view_billing: patient_id='{patient_id}', total_billing={len(items)}")

        # Filter by status
        if tool_input.get("status"):
            items = [i for i in items if tool_input["status"] == i.get("status")]

        return {"billing": items[:10], "count": len(items)}

    return {"error": "Unknown tool"}


def handle_customer_chat(event, storage):
    """Handle patient chatbot requests with tool use"""
    try:
        body = json.loads(event.get("body", "{}"))
        user_message = body.get("message", "")
        patient_email = body.get("customerEmail", "")  # Using customerEmail for consistency
        conversation_history = body.get("history", [])

        if not user_message:
            return _resp(400, {"error": "Message is required"})

        if not patient_email:
            return _resp(400, {"error": "Patient email is required"})

        # Build messages array
        messages = conversation_history + [{"role": "user", "content": user_message}]

        # System prompt
        system_prompt = f"""You are a helpful patient assistant for Silvermoat Healthcare.
You are helping a patient with email: {patient_email}
You can help them view their appointments, prescriptions, and billing information.
Use the available tools to search and retrieve information when needed.
Be empathetic, professional, and helpful in your responses.
Remember to protect patient privacy and only show information for this specific patient."""

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

                    # Execute tool with patient email scope
                    result = execute_customer_tool(tool_name, tool_input, storage, patient_email)

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
        print(f"Error in patient chatbot handler: {str(e)}")
        return _resp(500, {"error": str(e)})
