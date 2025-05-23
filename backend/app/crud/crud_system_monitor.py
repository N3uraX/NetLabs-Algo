from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import Optional, List
from uuid import UUID
from datetime import datetime

from app.models.system_monitor import SystemMonitor
from app.schemas.system_monitor import SystemMonitorCreate, SystemMonitorUpdate

class CRUDSystemMonitor:
    async def get_system_metric(self, db: AsyncSession, metric_id: UUID) -> Optional[SystemMonitor]:
        result = await db.execute(select(SystemMonitor).filter(SystemMonitor.id == metric_id))
        return result.scalars().first()

    async def get_system_metrics(
        self, db: AsyncSession, system_id: Optional[str] = None, skip: int = 0, limit: int = 100,
        start_time: Optional[datetime] = None, end_time: Optional[datetime] = None
    ) -> List[SystemMonitor]:
        query = select(SystemMonitor).order_by(SystemMonitor.last_heartbeat.desc())
        if system_id:
            query = query.filter(SystemMonitor.system_id == system_id)
        if start_time:
            query = query.filter(SystemMonitor.last_heartbeat >= start_time)
        if end_time:
            query = query.filter(SystemMonitor.last_heartbeat <= end_time)
            
        result = await db.execute(query.offset(skip).limit(limit))
        return result.scalars().all()

    async def create_system_metric(self, db: AsyncSession, *, obj_in: SystemMonitorCreate) -> SystemMonitor:
        db_obj = SystemMonitor(
            **obj_in.model_dump(exclude_unset=True),
            last_heartbeat=obj_in.last_heartbeat or datetime.utcnow()
        )
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def update_system_metric(
        self, db: AsyncSession, *, db_obj: SystemMonitor, obj_in: SystemMonitorUpdate
    ) -> SystemMonitor:
        update_data = obj_in.model_dump(exclude_unset=True)
        if 'last_heartbeat' not in update_data or update_data['last_heartbeat'] is None:
            update_data['last_heartbeat'] = datetime.utcnow()
            
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

system_monitor = CRUDSystemMonitor() 