import uuid
from sqlalchemy import Column, DateTime, Float
from sqlalchemy.dialects.postgresql import UUID
from app.core.database import Base
from datetime import datetime

class SecurityScoreLog(Base):
    __tablename__ = "security_score_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    score = Column(Float, nullable=False)
    # Add organization_id here if implementing multi-tenancy for scores
    # organization_id = Column(UUID(as_uuid=True), ForeignKey("organizations.id"), nullable=True, index=True) 