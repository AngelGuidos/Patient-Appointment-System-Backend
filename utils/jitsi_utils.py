import os
from dotenv import load_dotenv
from .jass_jwt import JaaSJwtBuilder

load_dotenv()

JITSI_DOMAIN = os.getenv("JITSI_DOMAIN")
JITSI_APP_ID = os.getenv("JITSI_APP_ID")
JITSI_KID = os.getenv("JITSI_KID")
JITSI_PRIVATE_KEY_PATH = os.getenv("JITSI_PRIVATE_KEY_PATH")


def read_private_key():
    with open(JITSI_PRIVATE_KEY_PATH, "r") as f:
        return f.read()

def generate_meeting_id(patient_name: str, appointment_id: int) -> str:
    safe_name = patient_name.lower().replace(" ", "").replace("ñ", "n")
    return f"telemedicina-{safe_name}-{appointment_id}"

def generate_jitsi_jwt(user_name, user_id, room_name, is_moderator, nbf_time, exp_time):
    private_key = read_private_key()

    print(f"[JITSI DEBUG] Generating JWT for room: {room_name}, user: {user_name}, is_moderator: {is_moderator}")

    builder = (
        JaaSJwtBuilder()
        .withAppID(JITSI_APP_ID)
        .withApiKey(JITSI_KID)
        .withRoomName(room_name)
        .withUserName(user_name)
        .withUserId(str(user_id))
        .withModerator(is_moderator)
        .withLobbyEnabled(True)
        .withNbfTime(nbf_time)
        .withExpTime(exp_time)
    )
    token = builder.signWith(private_key)

    print(f"[JITSI DEBUG] JWT generated: {token}")

    return token.decode("utf-8") if isinstance(token, bytes) else token

def get_jitsi_meeting_link_and_token(user_name, user_id, appointment_id, patient_name, is_moderator, nbf_time, exp_time):
    room_name = generate_meeting_id(patient_name, appointment_id)
    meeting_url = f"https://{JITSI_DOMAIN}/{JITSI_APP_ID}/{room_name}"

    token = generate_jitsi_jwt(user_name, user_id, room_name, is_moderator, nbf_time, exp_time)

    print(f"[JITSI DEBUG] Meeting URL: {meeting_url}")
    print(f"[JITSI DEBUG] Token: {token}")
    return {
        "meeting_id": room_name,
        "meeting_url": meeting_url,
        "token": token
    }
