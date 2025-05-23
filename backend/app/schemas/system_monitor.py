from pydantic import BaseModel, UUID4
from typing import Optional, Dict, Any
from datetime import datetime
from app.models.system_monitor import SystemStatus # Import enum

class SystemMonitorBase(BaseModel):
    system_id: str
    system_name: str
    status: Optional[SystemStatus] = SystemStatus.UNKNOWN
    cpu_usage: Optional[float] = None
    memory_usage: Optional[float] = None
    disk_usage: Optional[float] = None
    network_throughput_in: Optional[float] = None
    network_throughput_out: Optional[float] = None
    additional_metrics: Optional[Dict[str, Any]] = None

class SystemMonitorCreate(SystemMonitorBase):
    last_heartbeat: Optional[datetime] = None

class SystemMonitorUpdate(BaseModel):
    status: Optional[SystemStatus] = None
    cpu_usage: Optional[float] = None
    memory_usage: Optional[float] = None
    disk_usage: Optional[float] = None
    network_throughput_in: Optional[float] = None
    network_throughput_out: Optional[float] = None
    additional_metrics: Optional[Dict[str, Any]] = None
    last_heartbeat: Optional[datetime] = None

class SystemMonitorInDBBase(SystemMonitorBase):
    id: UUID4
    last_heartbeat: datetime

    class Config:
        from_attributes = True

class SystemMonitor(SystemMonitorInDBBase):
    pass 