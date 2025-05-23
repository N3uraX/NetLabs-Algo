from pydantic import BaseModel, UUID4
from typing import Optional, Any
from datetime import datetime
from app.models.security_event import EventSeverity, EventStatus # Import enums

class SecurityEventBase(BaseModel):
    event_type: str
    severity: EventSeverity
    description: Optional[str] = None
    source_ip: Optional[str] = None
    destination_ip: Optional[str] = None
    device_id: Optional[str] = None
    user_id: Optional[UUID4] = None
    status: Optional[EventStatus] = EventStatus.NEW
    raw_log: Optional[Any] = None # Can be dict or str

class SecurityEventCreate(SecurityEventBase):
    timestamp: Optional[datetime] = None # Can be set by server if not provided

class SecurityEventUpdate(BaseModel):
    status: Optional[EventStatus] = None
    severity: Optional[EventSeverity] = None
    description: Optional[str] = None

class SecurityEventInDBBase(SecurityEventBase):
    id: UUID4
    timestamp: datetime
    
    class Config:
        from_attributes = True

class SecurityEvent(SecurityEventInDBBase):
    pass
