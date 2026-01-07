"""
Shared business logic for healthcare domain operations.

This module contains healthcare-specific business logic used by Lambda handlers,
particularly patient upsert logic used when creating appointments and medical records.
"""


def upsert_patient_for_appointment(storage, body):
    """
    Extract patient data from appointment body and upsert patient.

    Args:
        storage: DynamoDBBackend instance
        body: Appointment request body containing patientName and patientEmail

    Returns:
        str: Patient ID if patient data provided, None otherwise

    Side effects:
        - Modifies body dict by removing patientName and patientEmail
        - Creates or updates patient record in DynamoDB
    """
    patient_name = body.get("patientName")
    patient_email = body.get("patientEmail")

    if patient_email:
        patient = storage.upsert_customer(patient_email, {
            "name": patient_name,
            "email": patient_email
        })
        # Remove duplicate fields from body
        body.pop("patientName", None)
        body.pop("patientEmail", None)
        return patient["id"]

    return None


def upsert_patient_for_medical_record(storage, body):
    """
    Extract patient data from medical record body and upsert patient.

    Args:
        storage: DynamoDBBackend instance
        body: Medical record request body containing either:
              - patientName and patientEmail (flat structure)
              - patient object (nested structure with email field)

    Returns:
        str: Patient ID if patient data provided, None otherwise

    Side effects:
        - Modifies body dict by removing patientName, patientEmail, or patient
        - Creates or updates patient record in DynamoDB
    """
    # Try nested patient object first (test/API pattern)
    patient_obj = body.get("patient")
    if patient_obj:
        patient_email = patient_obj.get("email")
        if patient_email:
            patient = storage.upsert_customer(patient_email, patient_obj)
            # Remove patient object from body
            body.pop("patient", None)
            return patient["id"]

    # Fall back to flat fields (legacy pattern)
    patient_name = body.get("patientName")
    patient_email = body.get("patientEmail") or body.get("patient_email")

    if patient_email:
        patient = storage.upsert_customer(patient_email, {
            "name": patient_name,
            "email": patient_email
        })
        # Remove duplicate fields from body
        body.pop("patientName", None)
        body.pop("patientEmail", None)
        body.pop("patient_email", None)
        return patient["id"]

    return None


def get_patient_id_from_medical_record(storage, medical_record_id):
    """
    Get patientId from a medical record (used for prescription creation).

    Args:
        storage: DynamoDBBackend instance
        medical_record_id: Medical record ID to look up

    Returns:
        str: Patient ID if medical record exists and has patientId, None otherwise
    """
    if not medical_record_id:
        return None

    medical_record = storage.get("medical_record", medical_record_id)
    if medical_record:
        return medical_record.get("patientId") or medical_record.get("customerId")

    return None
