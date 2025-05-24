from pydantic import BaseModel
from typing import List, Optional, Any
from uuid import UUID
from datetime import datetime
# Assuming DeviceStatus might be used here. If not, it can be removed.
# If EventSeverity and other enums are defined in a central app.models.enums, import from there.
# For now, assuming they are accessible as per the project structure or direct import if needed.
from app.models.enums import DeviceStatus 
from app.models.security_event import EventSeverity # For recent events
# from app.models.threat import ThreatSeverity # If used for ActiveThreatItem
# from app.models.vulnerability import VulnerabilitySeverity # If used for VulnerabilityDistributionItem

class OverviewStats(BaseModel):
    total_devices: int
    online_devices: int
    offline_devices: int
    active_threats: int
    open_vulnerabilities: int
    critical_events_today: int

class SecurityScoreResponse(BaseModel):
    current_score: float
    trend: Optional[float] = None # e.g., change from previous period
    last_calculated_at: datetime
    # For simplicity, not including historical_scores list in the base schema here
    # It can be added if the API endpoint specifically returns it under this model.

class RecentEvent(BaseModel):
    id: UUID
    timestamp: datetime
    event_type: str
    severity: EventSeverity
    description: Optional[str] = None
    source_ip: Optional[str] = None

class VulnerabilityDistributionItem(BaseModel):
    severity: str # Or use VulnerabilitySeverity enum from app.models.vulnerability
    count: int

class SystemStatusItem(BaseModel):
    id: UUID
    name: str
    status: DeviceStatus
    last_heartbeat: Optional[datetime] = None

class ActiveThreatItem(BaseModel):
    id: UUID
    name: str
    severity: str # Or use ThreatSeverity enum from app.models.threat
    type: str
    last_seen: datetime

class DashboardOverview(BaseModel):
    # This schema is directly for the /overview endpoint as per the original request context
    # It might aggregate various pieces of information.
    # Based on the existing dashboard_service.py or dashboard.py API endpoint,
    # this should reflect what that endpoint is designed to return.
    # Let's assume it returns a structure similar to OverviewStats for now.
    total_devices: int
    online_devices: int
    active_threats: int
    open_vulnerabilities: int
    critical_events_today: int
    # security_score: float # Example if security score is directly part of overview

# Note: The original import was:
# from .dashboard import DashboardOverview, SecurityScoreResponse, RecentEvent, VulnerabilityDistributionItem
# Ensure these key schemas are defined. SystemStatusItem and ActiveThreatItem are auxiliary here but common. 