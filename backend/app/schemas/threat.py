from pydantic import BaseModel, UUID4
from typing import Optional, Any, Dict, List
from datetime import datetime
from app.models.threat import ThreatSeverity, ThreatStatus # Import enums

class ThreatBase(BaseModel):
    name: str
    description: Optional[str] = None
    severity: ThreatSeverity
    status: Optional[ThreatStatus] = ThreatStatus.ACTIVE
    type: Optional[str] = None
    source: Optional[str] = None
    indicators: Optional[Dict[str, Any]] = None # Flexible for various IOC structures

class ThreatCreate(ThreatBase):
    first_seen: Optional[datetime] = None
    last_seen: Optional[datetime] = None

class ThreatUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    severity: Optional[ThreatSeverity] = None
    status: Optional[ThreatStatus] = None
    type: Optional[str] = None
    source: Optional[str] = None
    indicators: Optional[Dict[str, Any]] = None
    last_seen: Optional[datetime] = None

class ThreatInDBBase(ThreatBase):
    id: UUID4
    first_seen: datetime
    last_seen: datetime

    class Config:
        from_attributes = True

class Threat(ThreatInDBBase):
    pass 