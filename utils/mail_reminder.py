import os
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from controllers.appointmentController import getAllTodaysAppointment
from config.database import SessionLocal
from dotenv import load_dotenv
from datetime import datetime
from schemas.appointmentSchemas import *
from config.models import Appointment
from utils.mail_sender import BuildMail

load_dotenv()

MAIL_SENDER = os.getenv("EMAIL_SENDER", "")
MAIL_CREDETENTIALS = os.getenv("EMAIL_APP_PASSWORD", "")

scheduler = AsyncIOScheduler()

async def job_wrapper():
    async with SessionLocal() as db:
        appointments = await getAllTodaysAppointment(db)
        now = datetime.now().time()

        for appointment in appointments:
            beginTime = str(appointment.slot.Time).split(" - ")[0]
            appointment_time = datetime.strptime(beginTime, "%H:%M").time()
            

            dif_time = (
                datetime.combine(datetime.today(), appointment_time) -
                datetime.combine(datetime.today(), now)
            ).total_seconds() / 60

            if 0 <= dif_time <= 30 and appointment.ReminderSent == False:
                BuildMail(
                    subject=f"⏰ Recordatorio de cita médica por: {appointment.Problem}",
                    sender=MAIL_SENDER,
                    reciver=appointment.patient.Email,
                    credentials=MAIL_CREDETENTIALS,
                    paciente=appointment.patient.Name,
                    fecha=appointment.Date.strftime("%Y-%m-%d"),
                    enlace=appointment.MeetingLink,
                    tipo="recordatorio",
                    hora=beginTime
                )

                appointment.ReminderSent = True
                db.add(appointment)
                await db.commit()

def start_scheduler():
    scheduler.add_job(job_wrapper, IntervalTrigger(seconds=60))
    scheduler.start()