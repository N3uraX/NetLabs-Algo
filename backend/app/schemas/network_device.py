from pydantic import BaseModel, UUID4, validator, Field
from typing import Optional, Annotated
from datetime import datetime
from app.models.enums import DeviceType, DeviceStatus

# Shared properties
class NetworkDeviceBase(BaseModel):
    name: Annotated[str, Field(min_length=1, max_length=255)]
    description: Optional[str] = None
    device_type: DeviceType
    host: Annotated[str, Field(min_length=1, max_length=255)] # Could be IP or FQDN
    port: Optional[int] = None
    username: Optional[Annotated[str, Field(min_length=1, max_length=255)]] = None
    use_ssl: Optional[bool] = True
    ip_address: Optional[Annotated[str, Field(min_length=1, max_length=255)]] = None
    mac_address: Optional[Annotated[str, Field(min_length=1, max_length=17)]] = None # XX:XX:XX:XX:XX:XX
    serial_number: Optional[Annotated[str, Field(min_length=1, max_length=255)]] = None
    firmware_version: Optional[Annotated[str, Field(min_length=1, max_length=255)]] = None
    model: Optional[Annotated[str, Field(min_length=1, max_length=255)]] = None
    organization_id: Optional[UUID4] = None

    @validator("port")
    def port_must_be_in_range(cls, v):
        if v is not None and not (1 <= v <= 65535):
            raise ValueError("Port number must be between 1 and 65535")
        return v

# Properties to receive on item creation
class NetworkDeviceCreate(NetworkDeviceBase):
    password: Optional[Annotated[str, Field(min_length=1)]] = None # Password is sent on creation/update, not stored directly

# Properties to receive on item update
class NetworkDeviceUpdate(NetworkDeviceBase):
    name: Optional[Annotated[str, Field(min_length=1, max_length=255)]] = None
    device_type: Optional[DeviceType] = None
    host: Optional[Annotated[str, Field(min_length=1, max_length=255)]] = None
    password: Optional[Annotated[str, Field(min_length=1)]] = None # Allow password update
    status: Optional[DeviceStatus] = None # Allow status update directly if needed by admin

# Properties shared by models stored in DB
class NetworkDeviceInDBBase(NetworkDeviceBase):
    id: UUID4
    status: DeviceStatus
    encrypted_password: Optional[str] = None # Not exposed to client
    last_seen: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True # Pydantic V2 way to use orm_mode

# Properties to return to client (doesn't include encrypted_password)
class NetworkDevice(NetworkDeviceInDBBase):
    pass # Inherits all from InDBBase, but explicitly defined for clarity

# Properties stored in DB (includes encrypted_password)
class NetworkDeviceInDB(NetworkDeviceInDBBase):
    pass 