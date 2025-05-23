from typing import Any, Dict, Optional, List, Union
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update as sqlalchemy_update, delete as sqlalchemy_delete

from app.crud.base import CRUDBase
from app.models.network_device import NetworkDevice
from app.schemas.network_device import NetworkDeviceCreate, NetworkDeviceUpdate
from app.utils.crypto import encrypt_data, decrypt_data # For password handling

class CRUDNetworkDevice(CRUDBase[NetworkDevice, NetworkDeviceCreate, NetworkDeviceUpdate]):
    async def create_with_organization(
        self, db: AsyncSession, *, obj_in: NetworkDeviceCreate, organization_id: Optional[UUID] = None
    ) -> NetworkDevice:
        db_obj_data = obj_in.model_dump(exclude_unset=True)
        if "password" in db_obj_data and db_obj_data["password"]:
            db_obj_data["encrypted_password"] = encrypt_data(db_obj_data.pop("password"))
        else:
            # Ensure encrypted_password is None if no password provided or it's empty
            db_obj_data["encrypted_password"] = None

        if organization_id:
            db_obj_data["organization_id"] = organization_id
        
        db_obj = self.model(**db_obj_data)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def get(self, db: AsyncSession, id: UUID) -> Optional[NetworkDevice]:
        result = await db.execute(select(self.model).filter(self.model.id == id))
        return result.scalars().first()

    async def get_multi(self, db: AsyncSession, *, skip: int = 0, limit: int = 100) -> List[NetworkDevice]:
        result = await db.execute(select(self.model).offset(skip).limit(limit))
        return result.scalars().all()

    async def get_multi_by_organization(
        self, db: AsyncSession, *, organization_id: UUID, skip: int = 0, limit: int = 100
    ) -> List[NetworkDevice]:
        result = await db.execute(
            select(self.model)
            .filter(NetworkDevice.organization_id == organization_id)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    async def update(
        self, db: AsyncSession, *, db_obj: NetworkDevice, obj_in: Union[NetworkDeviceUpdate, Dict[str, Any]]
    ) -> NetworkDevice:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)

        if "password" in update_data and update_data["password"]:
            update_data["encrypted_password"] = encrypt_data(update_data.pop("password"))
        elif "password" in update_data and not update_data["password"]:
             # Explicitly setting password to empty or None means we remove it
            update_data["encrypted_password"] = None
            update_data.pop("password") # remove from update_data if it was just an empty string
        
        return await super().update(db, db_obj=db_obj, obj_in=update_data)

    async def remove(self, db: AsyncSession, *, id: UUID) -> NetworkDevice:
        result = await db.execute(select(self.model).filter(self.model.id == id))
        obj = result.scalars().first()
        if obj:
            await db.delete(obj)
            await db.commit()
        return obj

    # Helper to get decrypted password - use with extreme caution
    def get_decrypted_password(self, db_obj: NetworkDevice) -> Optional[str]:
        if db_obj.encrypted_password:
            try:
                return decrypt_data(db_obj.encrypted_password)
            except ValueError:
                # Log this error: decryption failed for device ID db_obj.id
                return None
        return None

network_device = CRUDNetworkDevice(NetworkDevice) 