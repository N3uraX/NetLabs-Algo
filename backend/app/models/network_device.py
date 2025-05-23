import uuid
from sqlalchemy import Column, String, Integer, Boolean, DateTime, ForeignKey, Enum as SAEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime

from app.core.database import Base
from app.models.enums import DeviceType, DeviceStatus # Import the enums

class NetworkDevice(Base):
    __tablename__ = "network_devices"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    name = Column(String, index=True, nullable=False)
    description = Column(String, nullable=True)
    device_type = Column(SAEnum(DeviceType), nullable=False)
    
    host = Column(String, nullable=False)
    port = Column(Integer, nullable=True) # Specific port for management API (e.g., 8728 for MikroTik)
    username = Column(String, nullable=True) # Some devices might use API keys instead
    encrypted_password = Column(String, nullable=True) # Store encrypted password
    use_ssl = Column(Boolean, default=True) # For API connections that support SSL/TLS

    # Optional fields for more device details
    ip_address = Column(String, nullable=True) # Could be same as host, or a separate management IP
    mac_address = Column(String, nullable=True)
    serial_number = Column(String, nullable=True)
    firmware_version = Column(String, nullable=True)
    model = Column(String, nullable=True)
    
    status = Column(SAEnum(DeviceStatus), default=DeviceStatus.UNINITIALIZED)
    last_seen = Column(DateTime, nullable=True) # Timestamp of last successful communication

    organization_id = Column(UUID(as_uuid=True), ForeignKey("organizations.id"), nullable=True)
    organization = relationship("Organization", back_populates="network_devices")

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Future: relationship to monitoring data, logs, etc.

    def __repr__(self):
        return f"<NetworkDevice(name='{self.name}', host='{self.host}', type='{self.device_type.value}')>"

# Add to Organization model in organization.py:
# network_devices = relationship("NetworkDevice", back_populates="organization", cascade="all, delete-orphan") 