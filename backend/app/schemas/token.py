from pydantic import BaseModel
from typing import Optional
from uuid import UUID

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenPayload(BaseModel):
    sub: Optional[str] = None # Subject (user identifier, typically email or id)
    user_id: Optional[UUID] = None # Custom claim for user_id 