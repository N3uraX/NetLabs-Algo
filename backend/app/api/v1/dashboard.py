from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Any, List, Dict, Tuple, Optional
import random
from datetime import datetime, timedelta

from app import crud, models, schemas # Ensure schemas has the new dashboard specific schemas if any
from app.api import deps
from app.core.database import get_db
from app.models.security_event import EventSeverity
from app.models.threat import ThreatStatus, ThreatSeverity as ModelThreatSeverity # Aliased
from app.models.vulnerability import VulnerabilityStatus, VulnerabilitySeverity
from app.models.system_monitor import SystemStatus

router = APIRouter()

# --- Security Score Calculation Logic (Moved from services.py for now) ---
BASE_SCORE = 100.0
VULN_WEIGHTS = {
    VulnerabilitySeverity.CRITICAL: -10, VulnerabilitySeverity.HIGH: -5,
    VulnerabilitySeverity.MEDIUM: -2, VulnerabilitySeverity.LOW: -1, VulnerabilitySeverity.INFO: 0
}
THREAT_WEIGHTS = {
    ModelThreatSeverity.CRITICAL: -15, ModelThreatSeverity.HIGH: -7,
    ModelThreatSeverity.MEDIUM: -3, ModelThreatSeverity.LOW: -1,
}
EVENT_WEIGHTS = { 
    EventSeverity.CRITICAL: -5, EventSeverity.HIGH: -2,
    EventSeverity.MEDIUM: -0.5, EventSeverity.LOW: -0.1    
}
SYSTEM_HEALTH_WEIGHTS = {
    SystemStatus.OFFLINE: -3, SystemStatus.DEGRADED: -3,
    SystemStatus.ONLINE: 0, SystemStatus.UNKNOWN: -1 
}

async def calculate_current_security_score(db: AsyncSession) -> float:
    score = BASE_SCORE
    open_vulnerabilities = await crud.vulnerability.get_vulnerabilities(db, status=VulnerabilityStatus.OPEN, limit=None)
    for vuln in open_vulnerabilities: score += VULN_WEIGHTS.get(vuln.severity, 0)
    active_threats = await crud.threat.get_threats(db, status=ThreatStatus.ACTIVE, limit=None)
    for threat in active_threats: score += THREAT_WEIGHTS.get(threat.severity, 0)
    now = datetime.utcnow(); past_24_hours = now - timedelta(days=1)
    recent_events = await crud.security_event.get_events(db, start_time=past_24_hours, limit=None)
    for event in recent_events: score += EVENT_WEIGHTS.get(event.severity, 0)
    all_system_statuses = await crud.system_monitor.get_system_metrics(db, limit=None)
    latest_statuses: Dict[str, models.SystemMonitor] = {}
    for sm_record in all_system_statuses:
        if sm_record.system_id not in latest_statuses or \
           sm_record.last_heartbeat > latest_statuses[sm_record.system_id].last_heartbeat:
            latest_statuses[sm_record.system_id] = sm_record
    for system_id, sm_record in latest_statuses.items(): score += SYSTEM_HEALTH_WEIGHTS.get(sm_record.status, -1)
    return max(0.0, min(100.0, round(score, 1)))

async def get_security_score_with_trend(db: AsyncSession) -> Tuple[float, str]:
    current_score = await calculate_current_security_score(db)
    today_log = await crud.security_score_log.get_score_log_for_date(db, date=datetime.utcnow())
    should_log_new_score = False
    if not today_log or today_log.score != current_score:
        should_log_new_score = True
    if should_log_new_score:
         await crud.security_score_log.create_score_log(db, obj_in=schemas.SecurityScoreLogCreate(score=current_score, timestamp=datetime.utcnow()))
    trend = "stable"
    yesterday = datetime.utcnow() - timedelta(days=1)
    yesterday_score_log = await crud.security_score_log.get_score_log_for_date(db, date=yesterday)
    if yesterday_score_log:
        if current_score > yesterday_score_log.score + 1: trend = "up"
        elif current_score < yesterday_score_log.score - 1: trend = "down"
    return current_score, trend
# --- End Security Score Calculation Logic ---

# Schemas for dashboard responses
class DashboardOverview(schemas.BaseModel):
    total_events: int
    active_threats: int
    vulnerabilities_count: int
    monitored_systems: int
    security_score: float # 0.0 to 100.0

class SecurityScoreResponse(schemas.BaseModel): # Renamed from SecurityScore to avoid conflict
    score: float
    trend: str # "up", "down", "stable"

class RecentEvent(schemas.BaseModel):
    id: str
    timestamp: datetime
    type: str
    severity: str
    description: str

class VulnerabilityDistributionItem(schemas.BaseModel):
    severity: str
    count: int

@router.get("/overview", response_model=DashboardOverview)
async def get_dashboard_overview(
    db: AsyncSession = Depends(get_db),
    current_user: models.User = Depends(deps.get_current_active_user)
) -> Any:
    current_calc_score, _ = await get_security_score_with_trend(db)
    now = datetime.utcnow(); past_24_hours = now - timedelta(days=1)
    events_last_24h_list = await crud.security_event.get_events(db, start_time=past_24_hours, limit=None)
    active_threats_list = await crud.threat.get_threats(db, status=ThreatStatus.ACTIVE, limit=None)
    open_vulnerabilities_list = await crud.vulnerability.get_vulnerabilities(db, status=VulnerabilityStatus.OPEN, limit=None)
    all_system_statuses = await crud.system_monitor.get_system_metrics(db, limit=None)
    latest_statuses: Dict[str, models.SystemMonitor] = {}
    for sm_record in all_system_statuses:
        if sm_record.system_id not in latest_statuses or \
           sm_record.last_heartbeat > latest_statuses[sm_record.system_id].last_heartbeat:
            latest_statuses[sm_record.system_id] = sm_record
    return DashboardOverview(
        total_events=len(events_last_24h_list),
        active_threats=len(active_threats_list),
        vulnerabilities_count=len(open_vulnerabilities_list),
        monitored_systems=len(latest_statuses),
        security_score=current_calc_score
    )

@router.get("/security-score", response_model=SecurityScoreResponse)
async def get_security_score(
    db: AsyncSession = Depends(get_db),
    current_user: models.User = Depends(deps.get_current_active_user)
) -> Any:
    score, trend = await get_security_score_with_trend(db)
    return SecurityScoreResponse(score=score, trend=trend)

@router.get("/active-threats", response_model=List[schemas.Threat])
async def get_active_threats(
    db: AsyncSession = Depends(get_db),
    current_user: models.User = Depends(deps.get_current_active_user)
) -> Any:
    return await crud.threat.get_threats(db, status=ThreatStatus.ACTIVE, limit=10)

@router.get("/systems-status", response_model=List[schemas.SystemMonitor])
async def get_systems_status(
    db: AsyncSession = Depends(get_db),
    current_user: models.User = Depends(deps.get_current_active_user)
) -> Any:
    return await crud.system_monitor.get_system_metrics(db, limit=15)

@router.get("/recent-events", response_model=List[RecentEvent])
async def get_recent_events(
    db: AsyncSession = Depends(get_db),
    current_user: models.User = Depends(deps.get_current_active_user)
) -> Any:
    events_from_db = await crud.security_event.get_events(db, limit=20)
    return [
        RecentEvent(
            id=str(event.id), timestamp=event.timestamp, type=event.event_type,
            severity=event.severity.value, description=event.description or "No description"
        ) for event in events_from_db
    ]

@router.get("/vulnerability-distribution", response_model=List[VulnerabilityDistributionItem])
async def get_vulnerability_distribution(
    db: AsyncSession = Depends(get_db),
    current_user: models.User = Depends(deps.get_current_active_user)
) -> Any:
    distribution_counts: Dict[VulnerabilitySeverity, int] = {sev: 0 for sev in VulnerabilitySeverity}
    vulnerabilities = await crud.vulnerability.get_vulnerabilities(db, status=models.VulnerabilityStatus.OPEN, limit=None)
    for vuln in vulnerabilities:
        if vuln.severity in distribution_counts: distribution_counts[vuln.severity] += 1
    return [ VulnerabilityDistributionItem(severity=sev.value, count=count) for sev, count in distribution_counts.items()]

# The old dashboard endpoints listed in the initial user query are slightly different.
# /api/v1/dashboard/metrics -> Combined into /overview or specific like /security-score
# /api/v1/dashboard/events -> Implemented as /recent-events
# /api/v1/dashboard/threats -> Implemented as /active-threats
# /api/v1/dashboard/vulnerabilities -> Implemented as /vulnerability-distribution 