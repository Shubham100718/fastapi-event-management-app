from pydantic import BaseModel, EmailStr, ConfigDict
from typing import List


class AttendeeCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: str


class AttendeeCheckIn(BaseModel):
    attendee_ids: List[int]


class AttendeeResponse(BaseModel):
    attendee_id: int
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: str
    event_id: int
    check_in_status: bool

    model_config = ConfigDict(from_attributes=True)

