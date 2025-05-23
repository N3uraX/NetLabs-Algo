import uuid
from sqlalchemy import Column, String, DateTime, Text, ForeignKey, Enum as SAEnum, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.core.database import Base
from datetime import datetime

class ThreatSeverity(str, SAEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class ThreatStatus(str, SAEnum):
    ACTIVE = "active"
    CONTAINED = "contained"
    ERADICATED = "eradicated"
    RECOVERED = "recovered"
    CLOSED = "closed"

class Threat(Base):
    __tablename__ = "threats"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False, index=True)
    description = Column(Text)
    severity = Column(SAEnum(ThreatSeverity, name="threat_severity_enum", create_type=False), nullable=False, index=True)
    status = Column(SAEnum(ThreatStatus, name="threat_status_enum", create_type=False), default=ThreatStatus.ACTIVE, nullable=False, index=True)
    type = Column(String, index=True) # e.g., Malware, Phishing, DDoS
    source = Column(String) # e.g., External Feed, Internal Detection
    indicators = Column(JSON) # Store IOCs like IPs, Hashes, Domains
    first_seen = Column(DateTime, default=datetime.utcnow, index=True)
    last_seen = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, index=True)

    # Possible relationship to affected assets, events, etc.
    # event_id = Column(UUID(as_uuid=True), ForeignKey("security_events.id"))
    # event = relationship("SecurityEvent") 