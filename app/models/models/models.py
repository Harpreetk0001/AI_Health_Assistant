import enum
import uuid
from datetime import datetime, time

from sqlalchemy import (
    Column, String, Float, Boolean, Integer, Enum, Text,
    ForeignKey, DateTime, Time
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class UserRole(enum.Enum):
    elderly = "elderly"
    caregiver = "caregiver"
    admin = "admin"

class FallSeverity(enum.Enum):
    low = "low"
    moderate = "moderate"
    severe = "severe"

# 1. users
class User(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    full_name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True, index=True)
    hashed_password = Column(String, nullable=False)
    role = Column(Enum(UserRole), nullable=False)
    language_preference = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    health_vitals = relationship("HealthVital", back_populates="user")
    fall_events = relationship("FallEvent", back_populates="user")
    emergency_contacts = relationship("EmergencyContact", back_populates="user")
    medication_schedules = relationship("MedicationSchedule", back_populates="user")
    reminder_logs = relationship("ReminderLog", back_populates="schedule")
    conversation_logs = relationship("ConversationLog", back_populates="user")
    activity_logs = relationship("ActivityLog", back_populates="user")
    device_integrations = relationship("DeviceIntegration", back_populates="user")
    suggestions = relationship("Suggestion", back_populates="user")
    mental_health_logs = relationship("MentalHealthLog", back_populates="user")
    ui_preferences = relationship("UIPreference", back_populates="user", uselist=False)

# 2. health_vitals
class HealthVital(Base):
    __tablename__ = "health_vitals"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    heart_rate = Column(Float, nullable=True)
    bp_systolic = Column(Float, nullable=True)
    bp_diastolic = Column(Float, nullable=True)
    temperature = Column(Float, nullable=True)
    spo2 = Column(Float, nullable=True)
    fall_detected = Column(Boolean, default=False)
    notes = Column(Text, nullable=True)

    user = relationship("User", back_populates="health_vitals")

# 3. fall_events
class FallEvent(Base):
    __tablename__ = "fall_events"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    severity = Column(Enum(FallSeverity), nullable=False)
    video_snapshot = Column(String, nullable=True)
    escalated = Column(Boolean, default=False)

    user = relationship("User", back_populates="fall_events")

# 4. emergency_contacts
class EmergencyContact(Base):
    __tablename__ = "emergency_contacts"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=False)
    relationship = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)
    priority = Column(Integer, nullable=False)
    notify_by_sms = Column(Boolean, default=False)

    user = relationship("User", back_populates="emergency_contacts")

# 5. medication_schedule
class MedicationSchedule(Base):
    __tablename__ = "medication_schedule"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    medication_name = Column(String, nullable=False)
    dosage = Column(String, nullable=False)
    frequency = Column(String, nullable=False)
    time_of_day = Column(Time, nullable=False)
    active = Column(Boolean, default=True)

    user = relationship("User", back_populates="medication_schedules")
    reminder_logs = relationship("ReminderLog", back_populates="schedule")

# 6. reminder_logs
class ReminderLog(Base):
    __tablename__ = "reminder_logs"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    schedule_id = Column(UUID(as_uuid=True), ForeignKey("medication_schedule.id"), nullable=False)
    sent_at = Column(DateTime, default=datetime.utcnow)
    acknowledged = Column(Boolean, default=False)

    schedule = relationship("MedicationSchedule", back_populates="reminder_logs")

# 7. conversation_logs
class ConversationLog(Base):
    __tablename__ = "conversation_logs"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    input_text = Column(Text, nullable=False)
    response_text = Column(Text, nullable=False)
    language = Column(String, nullable=True)

    user = relationship("User", back_populates="conversation_logs")

# 8. activity_logs
class ActivityLog(Base):
    __tablename__ = "activity_logs"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    action = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    ip_address = Column(String, nullable=True)

    user = relationship("User", back_populates="activity_logs")

# 9. device_integrations
class DeviceIntegration(Base):
    __tablename__ = "device_integrations"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    device_name = Column(String, nullable=False)
    last_sync = Column(DateTime, nullable=True)
    status = Column(String, nullable=False)

    user = relationship("User", back_populates="device_integrations")

# 10. suggestions
class Suggestion(Base):
    __tablename__ = "suggestions"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    category = Column(String, nullable=False)
    suggestion = Column(Text, nullable=False)

    user = relationship("User", back_populates="suggestions")

# 11. mental_health_logs
class MentalHealthLog(Base):
    __tablename__ = "mental_health_logs"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    mood_score = Column(Integer, nullable=False)
    notes = Column(Text, nullable=True)

    user = relationship("User", back_populates="mental_health_logs")

# 12. ui_preferences
class UIPreference(Base):
    __tablename__ = "ui_preferences"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), unique=True, nullable=False)
    font_size = Column(String, nullable=True)
    contrast_mode = Column(Boolean, default=False)
    voice_control = Column(Boolean, default=False)

    user = relationship("User", back_populates="ui_preferences")

