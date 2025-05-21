import uuid
from datetime import datetime, timedelta
import os
from jose import jwt
from dotenv import load_dotenv
import json

load_dotenv()

# Configuración de JaaS (Jitsi as a Service)
JITSI_DOMAIN = os.getenv("JITSI_DOMAIN", "8x8.vc")
JITSI_APP_ID = os.getenv("JITSI_APP_ID", "")
JITSI_KID = os.getenv("JITSI_KID", "")
JITSI_PRIVATE_KEY_PATH = os.getenv("JITSI_PRIVATE_KEY_PATH", "jitsi_private_key.pem")

# Leer clave privada
try:
    with open(JITSI_PRIVATE_KEY_PATH, "r") as f:
        JITSI_API_PRIVATE_KEY = f.read()
except Exception as e:
    print(f"[JITSI ERROR] No se pudo leer la clave privada: {str(e)}")
    raise


def generate_meeting_id(patient_name: str, appointment_id: int) -> str:
    """
    Genera un ID único para la sala de Jitsi (sin timestamp para reutilización).
    """
    safe_name = patient_name.lower().replace(" ", "-")
    return f"telemedicina-{safe_name}-{appointment_id}"


def generate_jwt(meeting_id: str) -> str:
    """
    Genera un token JWT firmado con la clave privada, con acceso a todas las salas ("room": "*").
    """
    payload = {
        "aud": "jitsi",
        "iss": "chat",
        "sub": JITSI_APP_ID,
        "room": "*",
        "exp": int((datetime.utcnow() + timedelta(hours=1)).timestamp()),
        "context": {
            "user": {
                "name": "Paciente",
                "moderator": True
            }
        },
        "features": {
            "recording": True,
            "livestreaming": True,
            "transcription": True,
            "outbound-call": True
        }
    }

    headers = {
        "alg": "RS256",
        "kid": JITSI_KID,
        "typ": "JWT"
    }

    try:
        print("[JITSI DEBUG] Header JWT:")
        print(json.dumps(headers, indent=2))
        print("[JITSI DEBUG] Payload JWT:")
        print(json.dumps(payload, indent=2))

        token = jwt.encode(payload, JITSI_API_PRIVATE_KEY, algorithm="RS256", headers=headers)

        print(f"[JITSI DEBUG] Token JWT generado:\n{token}")
        return token
    except Exception as e:
        print(f"[JITSI ERROR] Error generando JWT: {str(e)}")
        raise


def create_jitsi_meeting(patient_name: str, appointment_id: int) -> dict:
    """
    Crea la URL de la reunión con token.
    """
    try:
        meeting_id = generate_meeting_id(patient_name, appointment_id)
        token = generate_jwt(meeting_id)
        full_domain = f"{JITSI_APP_ID}.{JITSI_DOMAIN}"
        meeting_url = f"https://{full_domain}/{meeting_id}?jwt={token}"

        print(f"[JITSI] Enlace generado exitosamente: {meeting_url}")

        return {
            "meeting_id": meeting_id,
            "meeting_url": meeting_url,
            "token": token
        }

    except Exception as e:
        print(f"[JITSI ERROR] Error creando reunión: {str(e)}")
        return {
            "meeting_id": None,
            "meeting_url": None,
            "error": str(e)
        }
