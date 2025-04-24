from app.chat.dao import ChatDAO, MessagesDAO
from app.exceptions import (
    AlreadyFriends,
    CannotAddYourself,
    InvitationNotFound,
    UserNotFound,
    UserNotInFriendsList,
)
from app.friends.dao import FriendsDAO
from app.users.dao import UsersDAO


async def invite_friends(id_user: int, login_friend: str):
    friend_data = await UsersDAO.find_one_or_none(login=login_friend)
    
    if not friend_data:
        raise UserNotFound
    
    id_friends = friend_data.id
    
    if id_user == id_friends:
        raise CannotAddYourself
    
    if await FriendsDAO.check_friends_or_invite(id_user, id_friends):
        raise AlreadyFriends
    
    result = await FriendsDAO.invite_friends(id_user, id_friends)
    
    return result

async def check_invite(id_user: int, id_friends: int):
    data_invite = await FriendsDAO.check_invite_list_friends(id_user, id_friends)
    
    if not data_invite:
        raise InvitationNotFound
    
    return data_invite
        
    
async def accept_friends(id_user: int, id_friends: int):
    data_invite = await check_invite(id_user, id_friends)
    await ChatDAO.create(id_user=data_invite.id_user, id_friends=data_invite.id_friends, id_group=None)
    return await FriendsDAO.accept_friends(id_user, id_friends)

    
async def reject_friends(id_user: int, id_friends: int):
    await check_invite(id_user, id_friends)
    return await FriendsDAO.reject_friends(id_user, id_friends)
    
async def delete_friends(id_user: int, id_friends: int):
    if not await FriendsDAO.check_friends(id_user, id_friends):
        raise UserNotInFriendsList
    
    data_chat = await ChatDAO.search_chat_two_user(id_user=id_user, id_friends=id_friends)
    
    if not data_chat:
        return {"detail": "Что-то пошло не так, возможно диалога не существует"}
    
    await MessagesDAO.delete(id_chat=data_chat.id)
    await ChatDAO.delete(id_chat=data_chat.id)
    
    return await FriendsDAO.delete_friends(id_user, id_friends)