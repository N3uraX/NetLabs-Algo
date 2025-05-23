from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from typing import List, Dict, Any
import asyncio
import random
from datetime import datetime

from app.api import deps
from app.models.user import User

router = APIRouter()

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)
            
    async def broadcast_json(self, data: Dict[str, Any]):
        for connection in self.active_connections:
            await connection.send_json(data)

manager = ConnectionManager()

@router.websocket("/ws/dashboard")
async def websocket_dashboard_endpoint(
    websocket: WebSocket,
    # current_user: User = Depends(deps.get_current_active_user) # Add this back once client sends token
):
    await manager.connect(websocket)
    # For now, we can't use current_user because typical WebSocket clients 
    # might not send auth headers in the same way as HTTP requests.
    # Token can be sent as a query parameter or as a first message after connection.
    # We will simulate this by asking for a token as the first message for demo purposes.
    
    # Simple auth placeholder: client should send token as first message
    # token = await websocket.receive_text()
    # try:
    #     user = await deps.get_current_user_from_token(token, db) # Imaginary function, needs db access
    #     if not user.is_active:
    #         await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
    #         manager.disconnect(websocket)
    #         return
    # except HTTPException:
    #     await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
    #     manager.disconnect(websocket)
    #     return

    # await manager.send_personal_message(f"Welcome User! You are connected to dashboard updates.", websocket)
    await manager.send_personal_message(f"Welcome! You are connected to dashboard updates.", websocket)

    try:
        while True:
            # This is a simple broadcaster. In a real app, you'd listen for specific messages
            # or push updates based on backend events (e.g., from Celery tasks or DB triggers).
            await asyncio.sleep(5) # Simulate sending updates every 5 seconds
            mock_update = {
                "type": "dashboard_update",
                "timestamp": datetime.utcnow().isoformat(),
                "new_events_count": random.randint(0, 5),
                "security_score_change": round(random.uniform(-0.5, 0.5), 2),
                "active_threats_change": random.randint(-2, 2)
            }
            await manager.broadcast_json(mock_update)
            # For testing specific client messages:
            # data = await websocket.receive_text()
            # await manager.send_personal_message(f"You wrote: {data}", websocket)
            # await manager.broadcast(f"Client wrote: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        print(f"Client disconnected from dashboard ws")
    except Exception as e:
        print(f"Error in dashboard websocket: {e}")
        manager.disconnect(websocket)
        await websocket.close() 