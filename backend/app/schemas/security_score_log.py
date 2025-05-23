from pydantic import BaseModel, UUID4
from typing import Optional
from datetime import datetime

class SecurityScoreLogBase(BaseModel):
    score: float

class SecurityScoreLogCreate(SecurityScoreLogBase):
    timestamp: Optional[datetime] = None

class SecurityScoreLogInDBBase(SecurityScoreLogBase):
    id: UUID4
    timestamp: datetime

    class Config:
        from_attributes = True

class SecurityScoreLog(SecurityScoreLogInDBBase):
    pass 