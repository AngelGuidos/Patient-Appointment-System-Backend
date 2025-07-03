import os
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
import stripe
from schemas.appointmentSchemas import *
from config.models import Appointment, Patient, Slot, Service
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from fastapi import HTTPException
from dotenv import load_dotenv
from utils.mail_sender import BuildMail
from datetime import datetime, timedelta
from utils.timestamps_generators import timestamps_gen

stripe.api_key = "Enter_Your_API_Key"

from utils.jitsi_utils import get_jitsi_meeting_link_and_token, generate_jitsi_jwt

load_dotenv()

# Aqui deben de ir las credenciales del correo emisor 
MAIL_SENDER = os.getenv("EMAIL_SENDER", "")
MAIL_CREDETENTIALS = os.getenv("EMAIL_APP_PASSWORD", "")

async def createAppointment(appointment: AppointmentRequestModel, db: AsyncSession):
    patientResult = await db.execute(
        select(Patient).filter(Patient.Id == appointment.PatientId)
    )
    patientCheck = patientResult.scalars().first()

    if patientCheck is None:
        raise HTTPException(status_code=400, detail="Patient not found")

    slotResult = await db.execute(select(Slot).filter(Slot.Id == appointment.SlotId))
    slotCheck = slotResult.scalars().first()

    beginTime = str(slotCheck.Time).split(" - ")[0]
    endTime = str(slotCheck.Time).split(" - ")[1]

    if slotCheck is None:
        raise HTTPException(status_code=400, detail="Slot not found")

    serviceResult = await db.execute(
        select(Service).filter(Service.Id == appointment.ServiceId)
    )
    serviceCheck = serviceResult.scalars().first()

    if serviceCheck is None:
        raise HTTPException(status_code=400, detail="Service not found")

    if appointment.Modality not in ["Presential", "Virtual"]:
        raise HTTPException(
            status_code=400,
            detail="Modalidad inválida. Debe ser 'Presential' o 'Virtual'"
        )

    print(f"[BACKEND] Creando cita con modalidad: {appointment.Modality}")

    newAppointment = Appointment(
        Problem=appointment.Problem,
        Date=appointment.Date,
        PatientId=appointment.PatientId,
        ServiceId=appointment.ServiceId,
        SlotId=appointment.SlotId,
        Modality=appointment.Modality,
        MeetingLink=None,
    )
    db.add(newAppointment)
    await db.commit()
    await db.refresh(newAppointment)

    if appointment.Modality == "Virtual":
        nbf_timestamp, exp_timestamp = timestamps_gen(beginTime, endTime, appointment.Date)
        room_name = f"telemedicina-{patientCheck.Name.lower().replace(' ', '')}-{newAppointment.Id}"
        room_name = room_name.replace("ñ", "n")
        meeting_url = f"https://8x8.vc/{os.getenv('JITSI_APP_ID')}/{room_name}"

        patient_token = generate_jitsi_jwt(
            user_name=patientCheck.Name,
            user_id=patientCheck.Id,
            room_name=room_name,
            is_moderator=False,
            nbf_time=nbf_timestamp,
            exp_time=exp_timestamp
        )

        print(f"[BACKEND] Jwt de para el paciente generado: {patient_token}")
        
        patient_meeting_link = f"{meeting_url}?jwt={patient_token}"

        newAppointment.MeetingLink = patient_meeting_link
        await db.commit()
        await db.refresh(newAppointment)
        print(f"[BACKEND] Enlace de Jitsi JaaS generado: {meeting_url}")
    
        BuildMail (
                subject=f"Cita de Telemedicina por: {appointment.Problem}",
                sender=MAIL_SENDER,
                reciver=patientCheck.Email,
                credentials=MAIL_CREDETENTIALS,
                paciente=patientCheck.Name,
                fecha=str(appointment.Date),
                enlace=patient_meeting_link,
                tipo="confirmacion",
                hora=beginTime,
            )

    print(f"[BACKEND] Cita creada. ID: {newAppointment.Id}, Link: {newAppointment.MeetingLink}")
    return newAppointment

async def get_doctor_jitsi_info(appointment_id: int, db: AsyncSession):
    appointment = await db.get(Appointment, appointment_id)
    if not appointment or appointment.Modality != "Virtual":
        raise HTTPException(status_code=404, detail="Appointment not found or not virtual")

    patient = await db.get(Patient, appointment.PatientId)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    slotResult = await db.execute(select(Slot).filter(Slot.Id == appointment.SlotId))
    slotCheck = slotResult.scalars().first()

    beginTime = str(slotCheck.Time).split(" - ")[0]
    endTime = str(slotCheck.Time).split(" - ")[1]

    nbf_timestamp, exp_timestamp = timestamps_gen(beginTime, endTime, appointment.Date)

    doctor_name = "Dr"
    doctor_id = 1
    result = get_jitsi_meeting_link_and_token(
        user_name=doctor_name,
        user_id=doctor_id,
        appointment_id=appointment.Id,
        patient_name=patient.Name,
        is_moderator=True,
        nbf_time=nbf_timestamp,
        exp_time=exp_timestamp
    )
    print(f"[BACKEND] Respuesta de get_doctor: {result}")
    return result


async def getAllAppointment(db: AsyncSession):
    smt = (
        select(Appointment)
        .options(joinedload(Appointment.patient))
        .options(joinedload(Appointment.service))
        .options(joinedload(Appointment.slot))
        .filter(Appointment.Status == "Pending")
        .order_by(Appointment.Id.desc())
    )

    result = await db.execute(smt)
    appointments = result.scalars().all()
    return appointments


async def getAllTodaysAppointment(db: AsyncSession):
    result = await db.execute(
        select(Appointment)
        .options(joinedload(Appointment.patient))
        .options(joinedload(Appointment.service))
        .options(joinedload(Appointment.slot))
        .filter(
            Appointment.Date == datetime.now().date(), Appointment.Status == "Pending"
        )
        .order_by(Appointment.Id.desc())
    )
    appointments = result.scalars().all()
    if appointments is None:
        raise HTTPException(status_code=404, detail="Appointments not found")
    return appointments


async def getAllAppointmentAccPatient(patientId: int, db: AsyncSession):
    result = await db.execute(
        select(Appointment)
        .options(joinedload(Appointment.patient))
        .options(joinedload(Appointment.service))
        .options(joinedload(Appointment.slot))
        .filter(Appointment.PatientId == patientId)
        .order_by(Appointment.Id.desc())
    )
    appointments = result.scalars().all()
    if appointments is None:
        raise HTTPException(status_code=404, detail="Appointments not found")

    return appointments


async def createPrescription(
    appoinmentId: int, prescription: PrescriptionRequestModel, db: AsyncSession
):
    result = await db.execute(
        select(Appointment).filter(Appointment.Id == appoinmentId)
    )
    appointmentCheck = result.scalars().first()
    if appointmentCheck is None:
        raise HTTPException(status_code=400, detail="Appointment not found")

    appointmentCheck.Prescription = prescription.Prescription
    appointmentCheck.Status = "Completed"
    await db.commit()
    await db.refresh(appointmentCheck)

    return appointmentCheck


async def totalPendingAppointment(db: AsyncSession):
    result = await db.execute(
        select(Appointment).filter(Appointment.Status == "Pending")
    )
    appointments = result.scalars().all()
    if appointments is None:
        raise HTTPException(status_code=404, detail="Appointments not found")

    return len(appointments)


async def create_product():
    try:
        product = stripe.Product.create(
            name="Checkup", description="This are the charges for the service."
        )
        return product
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def create_price(product_id: str, amount: int, currency: str):
    try:
        price = stripe.Price.create(
            currency=currency, product=product_id, unit_amount=amount
        )
        return price
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def create_payment_link(price_id: str):
    try:
        payment_link = stripe.PaymentLink.create(
            line_items=[{"price": price_id, "quantity": 1}],
            after_completion={
                "type": "redirect",
                "redirect": {
                    "url": "http://localhost:5173/Appointments"
                },
            },
        )
        return payment_link
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def create_payment_link_for_appointment(payment: PaymentLinkRequestModel):
    try:
        product = await create_product()
        price = await create_price(product.id, payment.Amount, payment.Currency)
        payment_link = await create_payment_link(price.id)
        return {"url": payment_link.url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))