import asyncio
import json

import redis.asyncio as aioredis
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.analysis import IncidentAnalysis
from app.config import REDIS_URL

router = APIRouter()

connected_clients = []


async def redis_listener():
    print("REDIS LISTENER: starting up", flush=True)
    try:
        r = aioredis.from_url(REDIS_URL)
        pubsub = r.pubsub()
        await pubsub.subscribe("analysis_updates")
        print("REDIS LISTENER: subscribed to analysis_updates", flush=True)

        async for message in pubsub.listen():
            print(f"REDIS LISTENER: got message: {message}")
            if message["type"] == "message":
                incident_id = int(message["data"])
                print(f"REDIS LISTENER: analysis done for incident {incident_id}")

                db = SessionLocal()
                try:
                    analysis = db.query(IncidentAnalysis).filter(
                        IncidentAnalysis.incident_id == incident_id
                    ).first()

                    if analysis:
                        payload = json.dumps({
                            "type": "analysis_complete",
                            "incident_id": incident_id,
                            "risk_level": analysis.risk_level,
                            "contributing_factors": analysis.contributing_factors,
                            "recommendations": analysis.recommendations,
                            "created_at": str(analysis.created_at),
                        })

                        print(f"REDIS LISTENER: sending to {len(connected_clients)} clients")
                        for client in connected_clients.copy():
                            try:
                                await client.send_text(payload)
                            except:
                                connected_clients.remove(client)
                finally:
                    db.close()
    except Exception as e:
        print(f"REDIS LISTENER ERROR: {e}")


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connected_clients.append(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        connected_clients.remove(websocket)