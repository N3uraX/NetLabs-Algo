from fastapi import APIRouter

from app.api.v1 import auth, users, dashboard, websockets, network_devices

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["dashboard"])
api_router.include_router(websockets.router, prefix="/ws", tags=["websockets"])
api_router.include_router(network_devices.router, prefix="/network-devices", tags=["network-devices"]) 