from pydantic import BaseModel, UUID4
from typing import Optional
from datetime import datetime

# Shared properties
class OrganizationBase(BaseModel):
    name: Optional[str] = None

# Properties to receive via API on creation
class OrganizationCreate(OrganizationBase):
    name: str

# Properties to receive via API on update
class OrganizationUpdate(OrganizationBase):
    pass

class OrganizationInDBBase(OrganizationBase):
    id: UUID4
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True # Replaces orm_mode = True

# Additional properties to return via API
class Organization(OrganizationInDBBase):
    pass

# Additional properties stored in DB
class OrganizationInDB(OrganizationInDBBase):
    pass 