import enum
from app.database import Base
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Enum, ForeignKey


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    is_active = Column(Integer, default=1)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    

class EventStatus(str, enum.Enum):
    scheduled = "scheduled"
    ongoing = "ongoing"
    completed = "completed"
    canceled = "canceled"


class Event(Base):
    __tablename__ = "events"
    event_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    location = Column(String, nullable=False)
    max_attendees = Column(Integer, nullable=False)
    status = Column(Enum(EventStatus), default=EventStatus.scheduled)
    attendees = relationship("Attendee", back_populates="event")


class Attendee(Base):
    __tablename__ = "attendees"
    attendee_id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone_number = Column(String, nullable=False)
    event_id = Column(Integer, ForeignKey("events.event_id"))
    check_in_status = Column(Boolean, default=False)
    event = relationship("Event", back_populates="attendees")

