from app.chat.dao import ChatDAO, MessagesDAO

async def my_chats(id_user: int):
    return await ChatDAO.my_chats(id_user=id_user)


async def detail_group(id_chat: int, id_user: int):
    data_chat = await ChatDAO.find_by_id(id=id_chat)
    if not (data_chat.id_user or data_chat.id_friends or data_chat.id_group):
        return {"detail": "Чат недоступен"}
    # Проверка группы
    return await MessagesDAO.detail(id_chat=data_chat.id)

async def send_messages(id_chat: int, id_user: int, text_messages: str):
    data_chat = await ChatDAO.find_by_id(id=id_chat)
    if not (data_chat.id_user or data_chat.id_friends or data_chat.id_group):
        return {"detail": "Чат недоступен"}
    
    return await MessagesDAO.create(
        text_message=text_messages, 
        id_chat=id_chat, 
        id_send_user=id_user
    )
    

async def find_my_chat_groups(id_user: int):
    # Поиск чатов групп 
    ...