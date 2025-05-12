from fastapi import APIRouter, Depends

from app.chat.dao import ChatDAO
from app.exceptions import UserIsNotGroupOwner
from app.groups.dao import GroupDAO, MemberGroupsDAO
from app.groups.schemas import SAcceptInGroup, SCreateGroup, SGroup
from app.groups.services import (
    accept_user_in_group,
    create_group,
    detail_group,
    join_group,
    leave_group,
    my_groups,
    reject_user_in_group,
    search_group,
)
from app.users.dependencies import get_current_user
from app.users.models import Users

router = APIRouter(
    prefix="/groups",
    tags=["API группы"]
)


@router.get('/all')
async def api_all_groups():
    return await GroupDAO.find_all()

@router.get("/search/{title}")
async def api_search_groups(title: str):
    return await search_group(title=title)

@router.get("/detail/{id_group}")
async def api_current_groups(id_group: int):
    return await detail_group(id_group=id_group)

@router.get("/my")
async def api_my_groups(current_user: Users = Depends(get_current_user)):
    return await my_groups(current_user.id)

@router.post("/create")
async def api_create_groups(data_group: SCreateGroup, current_user: Users = Depends(get_current_user)):
    data = await create_group(
        title=data_group.title,
        description=data_group.description,
        id_user=current_user.id
    )
    await ChatDAO.create(id_user=None, id_friends=None, id_group=data.id)
    return data

@router.post("/join")
async def api_join_group(data_group: SGroup, current_user: Users = Depends(get_current_user)):
    return await join_group(id_group=data_group.id, id_user=current_user.id)

@router.get("/list-invite-in-group/{group_id}")
async def api_list_invite_in_group(group_id: int):
    return {"data_users_in_invite_group": await MemberGroupsDAO.list_invite_in_group(group_id)}

@router.post("/accept")
async def api_accept_user_in_group(assept_data: SAcceptInGroup, current_user: Users = Depends(get_current_user)):
    return await accept_user_in_group(members_group_id=assept_data.members_group_id, current_user_id=current_user.id)

@router.post("/reject")
async def api_reject_user_in_group(assept_data: SAcceptInGroup, current_user: Users = Depends(get_current_user)):
    return await reject_user_in_group(members_group_id=assept_data.members_group_id, current_user_id=current_user.id)

@router.post("/leave")
async def api_leave_group(data_group: SGroup, current_user: Users = Depends(get_current_user)):
    return await leave_group(id_group=data_group.id, id_user=current_user.id)

@router.get("/possible")
async def api_possible_groups(current_user: Users = Depends(get_current_user)):
    return await GroupDAO.titles_with_members_count(user_id=current_user.id)