from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Any

from app import crud, schemas
from app.core import security
from app.core.database import get_db
from app.models.user import User 
from app.api import deps # Import deps

router = APIRouter()

@router.post("/login", response_model=schemas.Token)
async def login_for_access_token(
    db: AsyncSession = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = await crud.user.get_user_by_email(db, email=form_data.username)
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    elif not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    
    access_token = security.create_access_token(
        data={"sub": user.email, "user_id": str(user.id)} # Ensure user.id is string
    )
    return {"access_token": access_token, "token_type": "bearer"}

# /me endpoint
@router.get("/me", response_model=schemas.User)
async def read_users_me(current_user: User = Depends(deps.get_current_active_user)) -> Any: # Use deps
    """
    Get current user.
    """
    return current_user

# Placeholder for logout and refresh, as per instructions
# @router.post("/logout")
# async def logout():
#     # This would typically involve token blacklisting or session invalidation
#     return {"message": "Logout successful"}

# @router.post("/refresh", response_model=schemas.Token)
# async def refresh_token(current_user: User = Depends(deps.get_current_user)) -> Any: # Or a different dependency that doesn't check for active if refresh is allowed for inactive users
#     """
#     Refresh access token.
#     """
#     # This assumes the refresh token mechanism is separate or the original token can be used to get a new one before expiry
#     # For simplicity, re-using create_access_token. A more robust solution would use refresh tokens.
#     new_access_token = security.create_access_token(
#         data={"sub": current_user.email, "user_id": str(current_user.id)}
#     )
#     return {"access_token": new_access_token, "token_type": "bearer"}
