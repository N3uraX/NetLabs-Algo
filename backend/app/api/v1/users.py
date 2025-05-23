from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Any, List
from uuid import UUID

from app import crud, models, schemas
from app.api import deps
from app.core.database import get_db

router = APIRouter()

@router.post("/", response_model=schemas.User, status_code=201)
async def create_user(
    *, 
    db: AsyncSession = Depends(get_db),
    user_in: schemas.UserCreate,
    # current_user: models.User = Depends(deps.get_current_active_superuser) # Optional: only superusers can create users
) -> Any:
    """
    Create new user.
    """
    user = await crud.user.get_user_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system.",
        )
    user = await crud.user.create_user(db=db, obj_in=user_in)
    return user

@router.get("/", response_model=List[schemas.User])
async def read_users(
    db: AsyncSession = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user) # Or superuser for more restriction
) -> Any:
    """
    Retrieve users.
    """
    users = await crud.user.get_users(db, skip=skip, limit=limit)
    return users

@router.get("/{user_id}", response_model=schemas.User)
async def read_user_by_id(
    user_id: UUID,
    current_user: models.User = Depends(deps.get_current_active_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """
    Get a specific user by id.
    """
    user = await crud.user.get_user(db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    # Add authorization check if needed: if user.id != current_user.id and not current_user.is_superuser:
    # raise HTTPException(status_code=403, detail="Not enough permissions")
    return user

@router.put("/{user_id}", response_model=schemas.User)
async def update_user(
    *,
    db: AsyncSession = Depends(get_db),
    user_id: UUID,
    user_in: schemas.UserUpdate,
    current_user: models.User = Depends(deps.get_current_active_user)
) -> Any:
    """
    Update a user.
    """
    user = await crud.user.get_user(db, user_id=user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this id does not exist in the system",
        )
    # Add authorization check: if user.id != current_user.id and not current_user.is_superuser:
    #     raise HTTPException(status_code=403, detail="Not enough permissions")
    user = await crud.user.update_user(db=db, db_obj=user, obj_in=user_in)
    return user

@router.delete("/{user_id}", response_model=schemas.User)
async def delete_user(
    *,
    db: AsyncSession = Depends(get_db),
    user_id: UUID,
    current_user: models.User = Depends(deps.get_current_active_superuser) # Typically only superusers can delete
) -> Any:
    """
    Delete a user.
    """
    user = await crud.user.get_user(db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    # Add self-deletion prevention if needed: if user.id == current_user.id:
    #     raise HTTPException(status_code=403, detail="Cannot delete own account")
    user = await crud.user.remove_user(db=db, user_id=user_id)
    return user 