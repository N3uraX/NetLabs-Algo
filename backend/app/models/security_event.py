import uuid
from sqlalchemy import Column, String, DateTime, Text, ForeignKey, Enum as SAEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.core.database import Base
from datetime import datetime

class EventSeverity(str, SAEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class EventStatus(str, SAEnum):
    NEW = "new"
    ACKNOWLEDGED = "acknowledged"
    RESOLVED = "resolved"
    IGNORED = "ignored"

class SecurityEvent(Base):
    __tablename__ = "security_events"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    event_type = Column(String, nullable=False, index=True)
    severity = Column(SAEnum(EventSeverity, name="event_severity_enum", create_type=False), nullable=False, index=True)
    description = Column(Text)
    source_ip = Column(String, index=True)
    destination_ip = Column(String, index=True)
    device_id = Column(String, index=True) # Could be a ForeignKey to an Asset/Device model later
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True) # Optional link to a user
    status = Column(SAEnum(EventStatus, name="event_status_enum", create_type=False), default=EventStatus.NEW, nullable=False, index=True)
    raw_log = Column(Text) # Store the original log if available

    user = relationship("User") 