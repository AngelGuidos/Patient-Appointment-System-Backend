import pytest
from utils.jitsi_utils import generate_meeting_id, create_jitsi_meeting

def test_generate_meeting_id():
    # Test con nombre simple
    assert generate_meeting_id("John Doe", 123) == "telemedicina-johndoe-123"
    
    # Test con caracteres especiales
    result = generate_meeting_id("María José", 456)
    assert result == "telemedicina-mariajose-456" or result == "telemedicina-maríajosé-456"
    
    # Test con espacios múltiples
    assert generate_meeting_id("John    Doe", 789) == "telemedicina-johndoe-789"

def test_create_jitsi_meeting():
    # Test creación básica de reunión
    result = create_jitsi_meeting("John Doe", 123)
    expected_id = "telemedicina-johndoe-123"
    assert result["meeting_id"] == expected_id
    assert result["meeting_url"] == f"https://meet.jit.si/{expected_id}"
    assert result["token"] is None

    # Test con caracteres especiales
    result = create_jitsi_meeting("María José", 456)
    # Aceptamos ambas formas ya que la normalización de caracteres puede variar
    assert result["meeting_id"] in ["telemedicina-mariajose-456", "telemedicina-maríajosé-456"]
    assert result["meeting_url"].startswith("https://meet.jit.si/telemedicina-") 