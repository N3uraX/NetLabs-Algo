from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import Optional, List
from uuid import UUID
from datetime import datetime

from app.models.threat import Threat
from app.schemas.threat import ThreatCreate, ThreatUpdate

class CRUDThreat:
    async def get_threat(self, db: AsyncSession, threat_id: UUID) -> Optional[Threat]:
        result = await db.execute(select(Threat).filter(Threat.id == threat_id))
        return result.scalars().first()

    async def get_threats(
        self, db: AsyncSession, skip: int = 0, limit: int = 100,
        severity: Optional[str] = None, status: Optional[str] = None, threat_type: Optional[str] = None
    ) -> List[Threat]:
        query = select(Threat).order_by(Threat.last_seen.desc())
        if severity:
            query = query.filter(Threat.severity == severity)
        if status:
            query = query.filter(Threat.status == status)
        if threat_type:
            query = query.filter(Threat.type.ilike(f"%{threat_type}%"))
            
        result = await db.execute(query.offset(skip).limit(limit))
        return result.scalars().all()

    async def create_threat(self, db: AsyncSession, *, obj_in: ThreatCreate) -> Threat:
        db_obj = Threat(
            **obj_in.model_dump(exclude_unset=True),
            first_seen=obj_in.first_seen or datetime.utcnow(),
            last_seen=obj_in.last_seen or datetime.utcnow()
        )
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def update_threat(
        self, db: AsyncSession, *, db_obj: Threat, obj_in: ThreatUpdate
    ) -> Threat:
        update_data = obj_in.model_dump(exclude_unset=True)
        if 'last_seen' not in update_data or update_data['last_seen'] is None:
            update_data['last_seen'] = datetime.utcnow()
            
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

threat = CRUDThreat() 