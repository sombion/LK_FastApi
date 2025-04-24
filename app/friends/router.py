from fastapi import APIRouter, Depends

from app.exceptions import UserNotFound
from app.friends.dao import FriendsDAO
from app.friends.schemas import SFriends, SFriendsDetail, SFriendsInvite
from app.friends.services import (accept_friends, delete_friends,
                                  invite_friends, reject_friends)
from app.groups.dao import GroupDAO, MemberGroupsDAO
from app.users.dao import UsersDAO
from app.users.dependencies import get_current_user
from app.users.models import Users

router = APIRouter(
    prefix="/fiends",
    tags=["API друзей"]
)

@router.get("/all")
async def api_all_friends(current_user: Users = Depends(get_current_user)):
    return await FriendsDAO.find_all()

@router.post("/detail")
async def api_detail_friends(data: SFriendsDetail):
    return await FriendsDAO.detail_friends(data.id_user, data.id_friends)
    
@router.get("/my-friends")
async def api_my_friends(current_user: Users = Depends(get_current_user)):
    return await FriendsDAO.my_friends(current_user.id)

@router.get("/invite-list")
async def api_invite_list(current_user: Users = Depends(get_current_user)):
    return await FriendsDAO.invite_list_friends(current_user.id)

@router.get("/possible")
async def api_list_possible_friends(current_user: Users = Depends(get_current_user)):
    return await MemberGroupsDAO.recommend_friends(id_user=current_user.id)
    
@router.post("/invite")
async def api_invite_friends(data_friends: SFriendsInvite, current_user: Users = Depends(get_current_user)):
    return await invite_friends(id_user=current_user.id, login_friend=data_friends.login_friend)

@router.post("/accept")
async def api_accept_friends(data_friends: SFriends, current_user: Users = Depends(get_current_user)):
    return await accept_friends(current_user.id, data_friends.id_friend)
    
@router.post("/reject")
async def api_reject_friends(data_friends: SFriends, current_user: Users = Depends(get_current_user)):
    return await reject_friends(current_user.id, data_friends.id_friend)
    
@router.delete("/delete/{id_friend}")
async def api_deleted_friends(id_friend: int, current_user: Users = Depends(get_current_user)):
    return await delete_friends(current_user.id, id_friend)