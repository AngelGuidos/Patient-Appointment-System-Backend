def generate_meeting_id(patient_name: str, appointment_id: int) -> str:
   
    safe_name = patient_name.lower().replace(" ", "")
    return f"telemedicina-{safe_name}-{appointment_id}"

def create_jitsi_meeting(patient_name: str, appointment_id: int) -> dict:
 
    meeting_id = generate_meeting_id(patient_name, appointment_id)
    meeting_url = f"https://meet.jit.si/{meeting_id}"

    return {
        "meeting_id": meeting_id,
        "meeting_url": meeting_url,
        "token": None
    }
