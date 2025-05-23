from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import Optional, List
from uuid import UUID
from datetime import datetime

from app.models.security_event import SecurityEvent
from app.schemas.security_event import SecurityEventCreate, SecurityEventUpdate

class CRUDSecurityEvent:
    async def get_event(self, db: AsyncSession, event_id: UUID) -> Optional[SecurityEvent]:
        result = await db.execute(select(SecurityEvent).filter(SecurityEvent.id == event_id))
        return result.scalars().first()

    async def get_events(
        self, db: AsyncSession, skip: int = 0, limit: int = 100, 
        start_time: Optional[datetime] = None, end_time: Optional[datetime] = None,
        severity: Optional[str] = None, event_type: Optional[str] = None
    ) -> List[SecurityEvent]:
        query = select(SecurityEvent).order_by(SecurityEvent.timestamp.desc())
        if start_time:
            query = query.filter(SecurityEvent.timestamp >= start_time)
        if end_time:
            query = query.filter(SecurityEvent.timestamp <= end_time)
        if severity:
            query = query.filter(SecurityEvent.severity == severity)
        if event_type:
            query = query.filter(SecurityEvent.event_type.ilike(f"%{event_type}%"))
            
        result = await db.execute(query.offset(skip).limit(limit))
        return result.scalars().all()

    async def create_event(self, db: AsyncSession, *, obj_in: SecurityEventCreate) -> SecurityEvent:
        db_obj = SecurityEvent(
            **obj_in.model_dump(exclude_unset=True),
            timestamp=obj_in.timestamp or datetime.utcnow()
        )
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def update_event(
        self, db: AsyncSession, *, db_obj: SecurityEvent, obj_in: SecurityEventUpdate
    ) -> SecurityEvent:
        update_data = obj_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

security_event = CRUDSecurityEvent() 