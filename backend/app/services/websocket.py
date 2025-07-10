from fastapi import WebSocket
from typing import List
import json

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.typing_users = {}

    async def connect(self, websocket: WebSocket, user_id: str):
        await websocket.accept()
        self.active_connections.append(websocket)
        self.typing_users[websocket] = {"user_id": user_id, "typing": False}

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        if websocket in self.typing_users:
            del self.typing_users[websocket]

    async def broadcast_message(self, message: dict):
        for connection in self.active_connections:
            await connection.send_json(message)

    async def broadcast_typing_status(self, user_id: str, is_typing: bool):
        message = {
            "type": "typing_status",
            "user_id": user_id,
            "is_typing": is_typing
        }
        await self.broadcast_message(message)

    async def broadcast_analysis_update(self, analysis_type: str, results: dict):
        message = {
            "type": "analysis_update",
            "analysis_type": analysis_type,
            "results": results
        }
        await self.broadcast_message(message)

manager = ConnectionManager()
