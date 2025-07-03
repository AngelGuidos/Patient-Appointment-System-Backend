from pydantic import BaseModel
from datetime import date
from typing import Optional


class AppointmentRequestModel(BaseModel):
    Problem: str
    Date: date
    PatientId: int
    ServiceId: int
    SlotId: int
    Modality: str
    MeetingLink: Optional[str] = None

    class Config:
        orm_mode = True


class AppointmentResponseModel(BaseModel):
    Id: int
    Problem: str
    Date: date
    Prescription: Optional[str]
    Status: Optional[str]
    PatientId: int
    ServiceId: int
    SlotId: int
    Modality: str 
    MeetingLink: Optional[str]
    ReminderSent: Optional[bool]

    class Config:
        orm_mode = True


class PrescriptionRequestModel(BaseModel):
    Prescription: str
    Status: Optional[str] = None

    class Config:
        orm_mode = True


class PaymentLinkRequestModel(BaseModel):
    Amount: int
    Currency: str = "usd"
