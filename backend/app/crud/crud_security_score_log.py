from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import Optional, List
from datetime import datetime, timedelta

from app.models.security_score_log import SecurityScoreLog
from app.schemas.security_score_log import SecurityScoreLogCreate

class CRUDSecurityScoreLog:
    async def get_latest_score_log(self, db: AsyncSession) -> Optional[SecurityScoreLog]:
        result = await db.execute(
            select(SecurityScoreLog)
            .order_by(SecurityScoreLog.timestamp.desc())
            .limit(1)
        )
        return result.scalars().first()

    async def get_score_logs_for_period(
        self, db: AsyncSession, start_date: datetime, end_date: datetime
    ) -> List[SecurityScoreLog]:
        result = await db.execute(
            select(SecurityScoreLog)
            .filter(SecurityScoreLog.timestamp >= start_date)
            .filter(SecurityScoreLog.timestamp < end_date)
            .order_by(SecurityScoreLog.timestamp.asc())
        )
        return result.scalars().all()
    
    async def get_score_log_for_date(self, db: AsyncSession, date: datetime) -> Optional[SecurityScoreLog]:
        # Get score for a specific day (most recent entry for that day)
        start_of_day = date.replace(hour=0, minute=0, second=0, microsecond=0)
        end_of_day = start_of_day + timedelta(days=1)
        result = await db.execute(
            select(SecurityScoreLog)
            .filter(SecurityScoreLog.timestamp >= start_of_day)
            .filter(SecurityScoreLog.timestamp < end_of_day)
            .order_by(SecurityScoreLog.timestamp.desc())
            .limit(1)
        )
        return result.scalars().first()

    async def create_score_log(self, db: AsyncSession, *, obj_in: SecurityScoreLogCreate) -> SecurityScoreLog:
        db_obj = SecurityScoreLog(
            score=obj_in.score,
            timestamp=obj_in.timestamp or datetime.utcnow()
        )
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

security_score_log = CRUDSecurityScoreLog() 