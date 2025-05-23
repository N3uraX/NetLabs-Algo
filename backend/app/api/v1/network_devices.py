from fastapi import APIRouter, Depends, HTTPException, status, Body
from typing import Any, List, Optional
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, models, schemas
from app.api import deps
from app.models.enums import DeviceType # For validation
from app.services.mikrotik_service import MikroTikService
# from app.core.config import settings # No longer needed for global MikroTik config

router = APIRouter()

# --- Network Device Management (CRUD) ---

@router.post("/", response_model=schemas.NetworkDevice, status_code=status.HTTP_201_CREATED)
async def create_network_device(
    *, 
    db: AsyncSession = Depends(deps.get_db),
    device_in: schemas.NetworkDeviceCreate,
    current_user: models.User = Depends(deps.get_current_active_superuser) # Only superusers can add devices
) -> models.NetworkDevice:
    """Create a new network device entry."""
    # Add additional validation if needed, e.g., check if host is reachable
    # For MikroTik, ensure port is typically set (e.g. 8728 or 8729)
    if device_in.device_type == DeviceType.MIKROTIK and device_in.port is None:
        device_in.port = 8729 if device_in.use_ssl else 8728 # Default MikroTik ports
    
    device = await crud.network_device.create_with_organization(
        db=db, obj_in=device_in, organization_id=device_in.organization_id # Or current_user.organization_id if applicable
    )
    return device

@router.get("/{device_id}", response_model=schemas.NetworkDevice)
async def read_network_device(
    *, 
    db: AsyncSession = Depends(deps.get_db),
    device_id: UUID,
    current_user: models.User = Depends(deps.get_current_active_user)
) -> models.NetworkDevice:
    """Get a specific network device by ID."""
    device = await crud.network_device.get(db=db, id=device_id)
    if not device:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Network device not found")
    # Add authorization check: if user can access this device (e.g., based on organization)
    return device

@router.get("/", response_model=List[schemas.NetworkDevice])
async def read_network_devices(
    db: AsyncSession = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user)
) -> List[models.NetworkDevice]:
    """Retrieve all network devices (paginated)."""
    # Add filtering by organization, type, status etc. if needed
    devices = await crud.network_device.get_multi(db, skip=skip, limit=limit)
    return devices

@router.put("/{device_id}", response_model=schemas.NetworkDevice)
async def update_network_device(
    *, 
    db: AsyncSession = Depends(deps.get_db),
    device_id: UUID,
    device_in: schemas.NetworkDeviceUpdate,
    current_user: models.User = Depends(deps.get_current_active_superuser) # Only superusers can update
) -> models.NetworkDevice:
    """Update a network device."""
    db_device = await crud.network_device.get(db=db, id=device_id)
    if not db_device:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Network device not found")
    
    if device_in.device_type == DeviceType.MIKROTIK and device_in.port is None and db_device.port is None:
        device_in.port = 8729 if (device_in.use_ssl if device_in.use_ssl is not None else db_device.use_ssl) else 8728
        
    device = await crud.network_device.update(db=db, db_obj=db_device, obj_in=device_in)
    return device

@router.delete("/{device_id}", response_model=schemas.NetworkDevice)
async def delete_network_device(
    *, 
    db: AsyncSession = Depends(deps.get_db),
    device_id: UUID,
    current_user: models.User = Depends(deps.get_current_active_superuser) # Only superusers can delete
) -> models.NetworkDevice:
    """Delete a network device."""
    device = await crud.network_device.remove(db=db, id=device_id)
    if not device:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Network device not found")
    return device

# --- MikroTik Specific Operations ---

async def get_mikrotik_service_for_device(device_id: UUID, db: AsyncSession = Depends(deps.get_db)) -> MikroTikService:
    """Dependency to get a MikroTik device from DB and return an initialized MikroTikService."""
    db_device = await crud.network_device.get(db=db, id=device_id)
    if not db_device:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Network device with ID {device_id} not found.")
    if db_device.device_type != DeviceType.MIKROTIK:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Device {device_id} is not a MikroTik device (type: {db_device.device_type})."
        )
    
    decrypted_password = crud.network_device.get_decrypted_password(db_obj=db_device)
    if db_device.username and decrypted_password is None and db_device.encrypted_password is not None:
         # Password was set but decryption failed
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to decrypt password for MikroTik device {device_id}. Check encryption key or data integrity."
        )

    if not db_device.port:
         raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Port not configured for MikroTik device {device_id}."
        )

    try:
        service = MikroTikService(
            host=db_device.host,
            username=db_device.username if db_device.username else "", # Ensure username is not None
            password=decrypted_password, # Can be None if not set in DB
            port=db_device.port, # Already checked for None
            use_ssl=db_device.use_ssl
        )
        return service
    except ValueError as e: # From MikroTikService __init__ if basic params are missing
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, # Or 400 if data in DB is considered invalid client-side
            detail=f"Error initializing MikroTik service for device {device_id}: {e}"
        )

@router.get("/mikrotik/{device_id}/system-resource", response_model=Optional[Any])
async def get_mikrotik_device_system_resource(
    device_id: UUID, # Renamed from get_mikrotik_system_resource to avoid conflict
    current_user: models.User = Depends(deps.get_current_active_user),
    mt_service: MikroTikService = Depends(get_mikrotik_service_for_device)
) -> Any:
    """Fetches system resource information from a specific MikroTik device."""
    try:
        resource_info = await mt_service.get_system_resource()
        if resource_info is None:
            # Update device status in DB to ERROR or OFFLINE
            # await crud.network_device.update(db, db_obj=..., obj_in={"status": DeviceStatus.OFFLINE})
            raise HTTPException(status_code=status.HTTP_504_GATEWAY_TIMEOUT, detail=f"Failed to retrieve data from MikroTik device {device_id} or no data available.")
        # Update device status to ONLINE and last_seen
        # await crud.network_device.update(db, db_obj=..., obj_in={"status": DeviceStatus.ONLINE, "last_seen": datetime.utcnow()})
        return resource_info
    except ConnectionError as e:
        raise HTTPException(status_code=status.HTTP_504_GATEWAY_TIMEOUT, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An unexpected error occurred: {e}")

@router.get("/mikrotik/{device_id}/interfaces", response_model=List[Any])
async def get_mikrotik_device_interfaces(
    device_id: UUID,
    current_user: models.User = Depends(deps.get_current_active_user),
    mt_service: MikroTikService = Depends(get_mikrotik_service_for_device)
) -> Any:
    """Fetches interface list from a specific MikroTik device."""
    try:
        interfaces = await mt_service.get_interfaces()
        return interfaces
    except ConnectionError as e:
        raise HTTPException(status_code=status.HTTP_504_GATEWAY_TIMEOUT, detail=str(e))
    except Exception as e: 
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An unexpected error occurred: {e}")

@router.get("/mikrotik/{device_id}/firewall-rules", response_model=List[Any])
async def get_mikrotik_device_firewall_rules(
    device_id: UUID,
    current_user: models.User = Depends(deps.get_current_active_user),
    mt_service: MikroTikService = Depends(get_mikrotik_service_for_device)
) -> Any:
    """Fetches firewall filter rules from a specific MikroTik device."""
    try:
        rules = await mt_service.get_firewall_rules()
        return rules
    except ConnectionError as e:
        raise HTTPException(status_code=status.HTTP_504_GATEWAY_TIMEOUT, detail=str(e))
    except Exception as e: 
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An unexpected error occurred: {e}")

@router.get("/mikrotik/{device_id}/arp-table", response_model=List[Any])
async def get_mikrotik_device_arp_table(
    device_id: UUID,
    current_user: models.User = Depends(deps.get_current_active_user),
    mt_service: MikroTikService = Depends(get_mikrotik_service_for_device)
) -> Any:
    """Fetches ARP table from a specific MikroTik device."""
    try:
        arp_entries = await mt_service.get_arp_table()
        return arp_entries
    except ConnectionError as e:
        raise HTTPException(status_code=status.HTTP_504_GATEWAY_TIMEOUT, detail=str(e))
    except Exception as e: 
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An unexpected error occurred: {e}")

# Note: The placeholder for /discover-devices is removed as it's a broader concept.
# Real-time network metrics collection would also be a separate, larger feature. 