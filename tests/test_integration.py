import pytest
from fastapi.testclient import TestClient
from datetime import date, datetime
from sqlalchemy.ext.asyncio import AsyncSession
from main import app
from config.models import Patient, Appointment, Slot, Service
from config.database import SessionLocal
from utils.jitsi_utils import generate_meeting_id, create_jitsi_meeting
import uuid

# Configuración inicial
client = TestClient(app)

@pytest.fixture
async def test_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        await db.close()

@pytest.fixture
async def test_patient():
    patient_data = {
        "Name": "Test Patient",
        "Email": "test@example.com",
        "Password": "testpass123",
        "Phone": "1234567890",
        "Address": "Test Address"
    }
    response = client.post("/patient", json=patient_data)
    assert response.status_code == 200
    return response.json()

@pytest.mark.asyncio
async def test_virtual_appointment_jitsi_integration(mocker):
    """Prueba la integración completa de una cita virtual con Jitsi"""
    # Mock the BuildMail class
    mock_build_mail = mocker.patch('controllers.appointmentController.BuildMail')
    
    unique_id = str(uuid.uuid4())[:8]
    patient_data = {
        "Name": f"Test Patient Jitsi {unique_id}", 
        "Mobile": "1234567890",
        "Email": f"test.jitsi.{unique_id}@example.com",
        "Address": "Test Address",
        "Gender": "Male",
        "BloodGroup": "O+"
    }
    patient_response = client.post("/patient", json=patient_data)
    assert patient_response.status_code == 200, f"Falló la creación del paciente para Jitsi: {patient_response.text}"
    patient = patient_response.json()
    
    appointment_data = {
        "Problem": "Consulta Virtual de Prueba Jitsi",
        "Date": str(date.today()),
        "PatientId": patient["Id"],
        "ServiceId": 1,
        "SlotId": 1,
        "Modality": "Virtual"
    }
    
    response = client.post("/appointment", json=appointment_data)
    assert response.status_code == 200, f"Falló la creación de la cita para Jitsi: {response.text}"
    appointment = response.json()
    
    assert appointment["MeetingLink"] is not None
    assert "telemedicina" in appointment["MeetingLink"]
    assert patient["Name"].lower().replace(" ", "") in appointment["MeetingLink"]
    assert str(appointment["Id"]) in appointment["MeetingLink"]

    # Verificar que el enlace es válido según el formato esperado
    expected_meeting_id = generate_meeting_id(patient["Name"], appointment["Id"])
    expected_url = f"https://meet.jit.si/{expected_meeting_id}"
    assert appointment["MeetingLink"] == expected_url
    
    # Verify email was attempted to be sent
    mock_build_mail.assert_called_once()
    mock_build_mail.assert_called_with(
        subject=f"Cita de Telemedicina por: {appointment_data['Problem']}",
        sender=mocker.ANY,
        reciver=patient["Email"],
        credentials=mocker.ANY,
        paciente=patient["Name"],
        fecha=str(date.today()),
        enlace=appointment["MeetingLink"]
    )

@pytest.mark.asyncio
async def test_virtual_appointment_email_notification(mocker):
    """Prueba la integración del sistema de correos para citas virtuales"""
    unique_id = str(uuid.uuid4())[:8]
    patient_data = {
        "Name": f"Test Patient Email {unique_id}",
        "Mobile": "0987654321", 
        "Email": f"no-reply.email.{unique_id}@example.com", 
        "Address": "Test Address Email",
        "Gender": "Female",
        "BloodGroup": "A+"
    }
    patient_response = client.post("/patient", json=patient_data)
    assert patient_response.status_code == 200, f"Falló la creación del paciente para Email: {patient_response.text}"
    patient = patient_response.json()
    
    # Mock de BuildMail en el módulo donde se USA (controllers.appointmentController)
    mock_build_mail = mocker.patch('controllers.appointmentController.BuildMail')
    
    appointment_data = {
        "Problem": "Consulta Virtual con Notificación por Email",
        "Date": str(date.today()),
        "PatientId": patient["Id"],
        "ServiceId": 1,
        "SlotId": 1,
        "Modality": "Virtual"
    }
    
    response = client.post("/appointment", json=appointment_data)
    assert response.status_code == 200, f"Falló la creación de la cita para Email: {response.text}"
    appointment = response.json()
    
    mock_build_mail.assert_called_once()
    mock_build_mail.assert_called_with(
        subject=f"Cita de Telemedicina por: {appointment_data['Problem']}",
        sender=mocker.ANY,
        reciver=patient["Email"],
        credentials=mocker.ANY,
        paciente=patient["Name"],
        fecha=str(date.today()),
        enlace=appointment["MeetingLink"]
    )

@pytest.mark.asyncio
async def test_invalid_virtual_appointment_creation():
    """Prueba el manejo de errores en la creación de citas virtuales"""
    invalid_appointment_data = {
        "Problem": "Consulta Inválida",
        "Date": str(date.today()),
        "PatientId": 999999, # ID de paciente que no existe
        "ServiceId": 1,
        "SlotId": 1,
        "Modality": "Virtual"
    }
    
    response = client.post("/appointment", json=invalid_appointment_data)
    assert response.status_code == 400
    assert "Patient not found" in response.json()["detail"] 