import json
from typing import Dict, List

from fastapi import APIRouter, Depends, Request, WebSocket, WebSocketDisconnect

from app.chat.config_ws import manager
from app.chat.dao import ChatDAO
from app.chat.schemas import SSendMessages
from app.chat.services import detail_group, find_my_chat_groups, my_chats, send_messages
from app.exceptions import TokenAbsentException
from app.users.dao import UsersDAO
from app.users.dependencies import get_current_user, get_token
from app.users.models import Users

router = APIRouter(
    prefix="/chat",
    tags=["API работы с чатами"]
)
    
@router.get("/detail/{id_chat}")
async def api_detail_group(id_chat: int, current_user: Users = Depends(get_current_user)):
    return await detail_group(id_chat=id_chat, id_user=current_user.id)

@router.get("/detail-info/{id_chat}")
async def api_detail_info_friends(id_chat: int, current_user: Users = Depends(get_current_user)):
    return await ChatDAO.detail_info_chat_friends(id_chat)

@router.get("/detail-info-group/{id_chat}")
async def api_detail_info_group(id_chat: int, current_user: Users = Depends(get_current_user)):
    return await ChatDAO.detail_info_chat_group(id_chat)

@router.post("/send-messages")
async def api_send_messages(data_messages: SSendMessages, current_user: Users = Depends(get_current_user)):
    return await send_messages(
        id_chat=data_messages.id_chat, 
        id_user=current_user.id,
        text_messages=data_messages.text_message
    )
    
@router.get("/my-chats-friends")
async def api_my_chat_friends(current_user: Users = Depends(get_current_user)):
    return await my_chats(current_user.id)

@router.get("/my-chats-groups")
async def api_my_chat_groups(current_user: Users = Depends(get_current_user)):
    return await ChatDAO.my_group_chats(current_user.id)

active_connections: Dict[int, List[WebSocket]] = {}

@router.websocket("/ws/{chat_id}")
async def websocket_endpoint(websocket: WebSocket, chat_id: int):
    await websocket.accept()

    if chat_id not in active_connections:
        active_connections[chat_id] = []
    active_connections[chat_id].append(websocket)

    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)

            await send_messages(
                id_chat=int(message["id_chat"]), 
                id_user=int(message["id_send_user"]),
                text_messages=message["text_message"]
            )

            for conn in active_connections[chat_id]:
                if conn != websocket:
                    await conn.send_text(json.dumps(message))

    except WebSocketDisconnect:
        active_connections[chat_id].remove(websocket)


@router.websocket("/ws/groups/{chat_id}")
async def websocket_endpoint_group(websocket: WebSocket, chat_id: int):
    await websocket.accept()

    if chat_id not in active_connections:
        active_connections[chat_id] = []
    active_connections[chat_id].append(websocket)

    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            message["login"] = (await UsersDAO.find_by_id(id=message["id_send_user"])).login
            
            await send_messages(
                id_chat=int(message["id_chat"]), 
                id_user=int(message["id_send_user"]),
                text_messages=message["text_message"]
            )

            for conn in active_connections[chat_id]:
                await conn.send_text(json.dumps(message))

    except WebSocketDisconnect:
        active_connections[chat_id].remove(websocket)
