from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta
from typing import Tuple, Optional, Dict

from app import crud, models, schemas
from app.models.security_event import EventSeverity
from app.models.threat import ThreatStatus, ThreatSeverity as ModelThreatSeverity
from app.models.vulnerability import VulnerabilityStatus, VulnerabilitySeverity
from app.models.system_monitor import SystemStatus

BASE_SCORE = 100.0

# Weights for scoring
VULN_WEIGHTS = {
    VulnerabilitySeverity.CRITICAL: -10,
    VulnerabilitySeverity.HIGH: -5,
    VulnerabilitySeverity.MEDIUM: -2,
    VulnerabilitySeverity.LOW: -1,
    VulnerabilitySeverity.INFO: 0
}

THREAT_WEIGHTS = {
    ModelThreatSeverity.CRITICAL: -15,
    ModelThreatSeverity.HIGH: -7,
    ModelThreatSeverity.MEDIUM: -3,
    ModelThreatSeverity.LOW: -1,
}

EVENT_WEIGHTS = {
    EventSeverity.CRITICAL: -5,
    EventSeverity.HIGH: -2,
    EventSeverity.MEDIUM: -0.5, # Minor impact for medium events on score
    EventSeverity.LOW: -0.1    # Very minor impact for low events
}

SYSTEM_HEALTH_WEIGHTS = {
    SystemStatus.OFFLINE: -3,
    SystemStatus.DEGRADED: -3,
    SystemStatus.ONLINE: 0,
    SystemStatus.UNKNOWN: -1 # Penalize if status is unknown
}

async def calculate_current_security_score(db: AsyncSession) -> float:
    """Calculates the current security score based on various factors."""
    score = BASE_SCORE

    # 1. Impact of Open Vulnerabilities
    open_vulnerabilities = await crud.vulnerability.get_vulnerabilities(
        db, status=VulnerabilityStatus.OPEN, limit=None # Consider all open vulnerabilities
    )
    for vuln in open_vulnerabilities:
        score += VULN_WEIGHTS.get(vuln.severity, 0)

    # 2. Impact of Active Threats
    active_threats = await crud.threat.get_threats(
        db, status=ThreatStatus.ACTIVE, limit=None # Consider all active threats
    )
    for threat in active_threats:
        score += THREAT_WEIGHTS.get(threat.severity, 0)

    # 3. Impact of Recent Security Events (last 24 hours)
    now = datetime.utcnow()
    past_24_hours = now - timedelta(days=1)
    recent_events = await crud.security_event.get_events(
        db, start_time=past_24_hours, limit=None # Consider all events in the last 24h
    )
    for event in recent_events:
        score += EVENT_WEIGHTS.get(event.severity, 0)
    
    # 4. Impact of System Health
    all_system_statuses = await crud.system_monitor.get_system_metrics(db, limit=None)
    # To ensure we use only the latest status for each system
    latest_statuses: Dict[str, models.SystemMonitor] = {}
    for sm_record in all_system_statuses:
        if sm_record.system_id not in latest_statuses or \
           sm_record.last_heartbeat > latest_statuses[sm_record.system_id].last_heartbeat:
            latest_statuses[sm_record.system_id] = sm_record
            
    for system_id, sm_record in latest_statuses.items():
        score += SYSTEM_HEALTH_WEIGHTS.get(sm_record.status, -1) # Default penalty for unknown status in weights

    return max(0.0, min(100.0, round(score, 1))) # Ensure score is between 0 and 100

async def get_security_score_with_trend(db: AsyncSession) -> Tuple[float, str]:
    """
    Calculates the current security score, logs it if necessary, and determines its trend.
    """
    current_score = await calculate_current_security_score(db)

    # Log the new score. In a production system, this might be done by a periodic task.
    # For this implementation, we log if no score exists for today or if the score has changed.
    today_log = await crud.security_score_log.get_score_log_for_date(db, date=datetime.utcnow())
    
    should_log_new_score = False
    if not today_log:
        should_log_new_score = True
    elif today_log.score != current_score: # Log if the score is different from the last log of today
        should_log_new_score = True

    if should_log_new_score:
         await crud.security_score_log.create_score_log(
             db, 
             obj_in=schemas.SecurityScoreLogCreate(score=current_score, timestamp=datetime.utcnow())
         )

    # Trend calculation
    trend = "stable"
    yesterday = datetime.utcnow() - timedelta(days=1)
    yesterday_score_log = await crud.security_score_log.get_score_log_for_date(db, date=yesterday)

    if yesterday_score_log:
        # Define a threshold for 'stable', e.g., +/- 1 point
        if current_score > yesterday_score_log.score + 1:
            trend = "up"
        elif current_score < yesterday_score_log.score - 1:
            trend = "down"
    
    return current_score, trend

async def get_dashboard_overview_data(db: AsyncSession) -> schemas.DashboardOverview:
    """Gathers all data required for the dashboard overview."""
    current_score, _ = await get_security_score_with_trend(db) # Trend is calculated but not used in this specific schema
    
    now = datetime.utcnow()
    past_24_hours = now - timedelta(days=1)
    
    events_last_24h_list = await crud.security_event.get_events(db, start_time=past_24_hours, limit=None)
    total_events_count = len(events_last_24h_list)

    active_threats_list = await crud.threat.get_threats(db, status=ThreatStatus.ACTIVE, limit=None)
    active_threats_count = len(active_threats_list)

    open_vulnerabilities_list = await crud.vulnerability.get_vulnerabilities(db, status=VulnerabilityStatus.OPEN, limit=None)
    open_vulnerabilities_count = len(open_vulnerabilities_list)
    
    all_system_statuses = await crud.system_monitor.get_system_metrics(db, limit=None)
    latest_statuses: Dict[str, models.SystemMonitor] = {}
    for sm_record in all_system_statuses:
        if sm_record.system_id not in latest_statuses or \
           sm_record.last_heartbeat > latest_statuses[sm_record.system_id].last_heartbeat:
            latest_statuses[sm_record.system_id] = sm_record
    monitored_systems_count = len(latest_statuses)

    return schemas.DashboardOverview(
        total_events=total_events_count,
        active_threats=active_threats_count,
        vulnerabilities_count=open_vulnerabilities_count,
        monitored_systems=monitored_systems_count,
        security_score=current_score 
    ) 