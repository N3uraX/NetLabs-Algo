from typing import Optional, List
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.crud.base import CRUDBase
from app.models.organization import Organization
from app.schemas.organization import OrganizationCreate, OrganizationUpdate

class CRUDOrganization(CRUDBase[Organization, OrganizationCreate, OrganizationUpdate]):
    async def get_by_name(self, db: AsyncSession, *, name: str) -> Optional[Organization]:
        result = await db.execute(select(self.model).filter(self.model.name == name))
        return result.scalars().first()

    # You can add other organization-specific CRUD methods here if needed.
    # For example, finding all users in an organization, etc.
    # For now, inheriting from CRUDBase provides:
    # get(id), get_multi, create, update, remove

organization = CRUDOrganization(Organization) 