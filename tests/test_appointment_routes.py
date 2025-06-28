import pytest
from fastapi.testclient import TestClient
from datetime import date
from main import app
from schemas.appointmentSchemas import AppointmentRequestModel, PrescriptionRequestModel
from unittest.mock import patch

client = TestClient(app)

@pytest.fixture
def appointment_data():
    return {
        "Problem": "Dolor de cabeza",
        "Date": str(date.today()),
        "PatientId": 1,
        "ServiceId": 1,
        "SlotId": 1,
        "Modality": "Virtual"
    }

def test_create_appointment_endpoint(appointment_data):
    # Mock the BuildMail class
    with patch('controllers.appointmentController.BuildMail') as mock_mail:
        response = client.post("/appointment", json=appointment_data)
        assert response.status_code == 200
        data = response.json()
        assert data["Problem"] == appointment_data["Problem"]
        assert data["Modality"] == appointment_data["Modality"]
        assert data["MeetingLink"] is not None
        assert "telemedicina" in data["MeetingLink"]
        
        # Verify email was attempted to be sent
        mock_mail.assert_called_once()

def test_create_appointment_invalid_data():
    invalid_data = {
        "Problem": "Dolor de cabeza",
        "Date": str(date.today()),
        "PatientId": 1,
        # Falta ServiceId y SlotId
        "Modality": "Virtual"
    }
    response = client.post("/appointment", json=invalid_data)
    assert response.status_code == 422  # Validation error

def test_get_patient_appointments():
    patient_id = 1
    response = client.get(f"/appointment/{patient_id}")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_todays_appointments():
    response = client.get("/todaysAppointments")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_all_appointments():
    response = client.get("/appointment")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_prescription():
    appointment_id = 1
    prescription_data = {
        "Prescription": "Paracetamol 500mg cada 8 horas"
    }
    response = client.post(f"/prescription/{appointment_id}", json=prescription_data)
    assert response.status_code == 200
    data = response.json()
    assert data["Prescription"] == prescription_data["Prescription"]
    assert data["Status"] == "Completed"

def test_get_total_pending_appointments():
    response = client.get("/totalPendingAppointment")
    assert response.status_code == 200
    assert isinstance(response.json(), int)

def test_get_jitsi_token():
    appointment_id = 1
    response = client.get(f"/appointment/{appointment_id}/jitsi/doctor")
    assert response.status_code == 200
    data = response.json()
    assert "meeting_id" in data
    assert "meeting_url" in data
    assert "token" in data 