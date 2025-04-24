from app.exceptions import (
    GroupNotFound,
    NameAlreadyTaken,
    UserAlreadyInGroup,
    UserIsGroupOwner,
    UserNotFound,
)
from app.groups.dao import GroupDAO, MemberGroupsDAO
from app.users.dao import UsersDAO


async def search_group(title: str):
    return await GroupDAO.find_all(title=title)

async def detail_group(id_group):
    data_group = await GroupDAO.find_by_id(id_group)
    
    if not data_group:
        raise GroupNotFound
    
    data_admin_user = await UsersDAO.find_by_id(data_group.id_created)
    data_admin_user.hash_password = None
    
    data_users_in_group = await MemberGroupsDAO.all_user_in_one_group(id_group=id_group)
    
    data_group.admin_detail = data_admin_user
    data_group.data_users_in_group = data_users_in_group
    
    return data_group

async def my_groups(id_user: int):
    group_in_admin = await GroupDAO.find_all(id_created=id_user)
    group_in_user = await MemberGroupsDAO.find_group_in_user(id_user=id_user)
    return {
        "group_in_admin": group_in_admin,
        "group_in_user": group_in_user
    }

async def create_group(title: str, description: str, id_user: int):
    if await GroupDAO.find_one_or_none(title=title):
        raise NameAlreadyTaken
    
    if not await UsersDAO.find_by_id(id_user):
        raise UserNotFound
    
    return await GroupDAO.create(title=title, description=description, id_created=id_user)

async def check_user_and_group(id_group: int, id_user: int):
    if not await GroupDAO.find_by_id(id_group):
        raise GroupNotFound
    
    if not await UsersDAO.find_by_id(id_user):
        raise UserNotFound
    
    if await GroupDAO.find_one_or_none(id=id_group, id_created=id_user):
        raise UserIsGroupOwner

async def join_group(id_group: int, id_user: int):
    await check_user_and_group(id_group=id_group, id_user=id_user)
    
    if await MemberGroupsDAO.find_one_or_none(id_group=id_group, id_user=id_user):
        raise UserAlreadyInGroup
    
    return await MemberGroupsDAO.create(id_group=id_group, id_user=id_user)
    
async def leave_group(id_group: int, id_user: int):
    await check_user_and_group(id_group=id_group, id_user=id_user)

    if not await MemberGroupsDAO.find_one_or_none(id_group=id_group, id_user=id_user):
        raise GroupNotFound
    
    return await MemberGroupsDAO.delete_member(id_group=id_group, id_user=id_user)