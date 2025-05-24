import pytest
from datetime import datetime, date
from unittest.mock import Mock, patch, AsyncMock
from controllers.appointmentController import createAppointment, getAllAppointment
from config.models import Appointment, Patient, Service, Slot
from schemas.appointmentSchemas import AppointmentRequestModel
from fastapi import HTTPException

@pytest.fixture
def mock_db():
    db = AsyncMock()
    # Configurar el comportamiento del mock para execute
    mock_result = AsyncMock()
    mock_scalars = AsyncMock()
    mock_scalars.first = Mock()  # first no necesita ser async
    mock_scalars.all = Mock()    # all no necesita ser async
    mock_result.scalars = Mock(return_value=mock_scalars)
    db.execute = AsyncMock(return_value=mock_result)
    return db

@pytest.fixture
def sample_appointment_data():
    return AppointmentRequestModel(
        Problem="Dolor de cabeza",
        Date=date.today(),
        PatientId=1,
        ServiceId=1,
        SlotId=1,
        Modality="Virtual"
    )

@pytest.fixture
def mock_patient():
    return Patient(
        Id=1,
        Name="John Doe",
        Email="john@example.com"
    )

@pytest.fixture
def mock_service():
    return Service(
        Id=1,
        Name="Consulta General"
    )

@pytest.fixture
def mock_slot():
    return Slot(
        Id=1,
        Time="09:00",
        Status="Available"
    )

@pytest.mark.asyncio
async def test_create_appointment_virtual(mock_db, sample_appointment_data, mock_patient, mock_service, mock_slot):
    # Configurar los mocks
    mock_db.execute.return_value.scalars.return_value.first.side_effect = [
        mock_patient,
        mock_slot,
        mock_service
    ]

    # Mock del envío de correo
    with patch('controllers.appointmentController.BuildMail') as mock_mail:
        result = await createAppointment(sample_appointment_data, mock_db)
        
        # Verificaciones
        assert result.Problem == sample_appointment_data.Problem
        assert result.Modality == "Virtual"
        assert result.MeetingLink is not None
        assert "telemedicina" in result.MeetingLink
        assert mock_mail.called

@pytest.mark.asyncio
async def test_create_appointment_presential(mock_db, sample_appointment_data, mock_patient, mock_service, mock_slot):
    sample_appointment_data.Modality = "Presential"
    
    # Configurar los mocks
    mock_db.execute.return_value.scalars.return_value.first.side_effect = [
        mock_patient,
        mock_slot,
        mock_service
    ]

    result = await createAppointment(sample_appointment_data, mock_db)
    
    # Verificaciones
    assert result.Problem == sample_appointment_data.Problem
    assert result.Modality == "Presential"
    assert result.MeetingLink is None

@pytest.mark.asyncio
async def test_create_appointment_invalid_modality(mock_db, sample_appointment_data):
    sample_appointment_data.Modality = "InvalidModality"
    
    with pytest.raises(HTTPException) as exc_info:
        await createAppointment(sample_appointment_data, mock_db)
    
    assert exc_info.value.status_code == 400
    assert "Modalidad inválida" in str(exc_info.value.detail)

@pytest.mark.asyncio
async def test_get_all_appointments_pending(mock_db):
    # Mock de citas pendientes
    mock_appointments = [
        Appointment(Id=1, Status="Pending"),
        Appointment(Id=2, Status="Pending")
    ]
    mock_db.execute.return_value.scalars.return_value.all.return_value = mock_appointments

    result = await getAllAppointment(mock_db)
    
    assert len(result) == 2
    assert all(appointment.Status == "Pending" for appointment in result) 