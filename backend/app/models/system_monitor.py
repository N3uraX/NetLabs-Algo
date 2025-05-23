import uuid
from sqlalchemy import Column, String, DateTime, Float, JSON, Enum as SAEnum
from sqlalchemy.dialects.postgresql import UUID
from app.core.database import Base
from datetime import datetime

class SystemStatus(str, SAEnum):
    ONLINE = "online"
    OFFLINE = "offline"
    DEGRADED = "degraded"
    UNKNOWN = "unknown"

class SystemMonitor(Base):
    __tablename__ = "system_monitors"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    system_id = Column(String, nullable=False, index=True) # ID of the monitored system/asset
    system_name = Column(String, nullable=False, index=True)
    status = Column(SAEnum(SystemStatus, name="system_status_enum", create_type=False), default=SystemStatus.UNKNOWN, nullable=False, index=True)
    cpu_usage = Column(Float, nullable=True) # Percentage
    memory_usage = Column(Float, nullable=True) # Percentage
    disk_usage = Column(Float, nullable=True) # Percentage
    network_throughput_in = Column(Float, nullable=True) # Mbps
    network_throughput_out = Column(Float, nullable=True) # Mbps
    last_heartbeat = Column(DateTime, default=datetime.utcnow, index=True)
    additional_metrics = Column(JSON, nullable=True) # For any other specific metrics

    # This model is likely to be stored in TimescaleDB for performance with time-series data.
    # Ensure your TimescaleDB setup and Alembic migrations handle this appropriately. 