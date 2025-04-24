import pytest
from app.friends.dao import FriendsDAO


@pytest.mark.parametrize("id_user,id_friends", [
    (1, 2),
    (2, 3),
])
async def test_invite_friends(id_user, id_friends):
    invite = await FriendsDAO.invite_friends(id_user, id_friends)
    
    assert invite.id_user == id_user
    assert invite.id_friends == id_friends
    
@pytest.mark.parametrize("id_user", [
    (4),
])
async def test_invite_list_friends(id_user):
    list = await FriendsDAO.invite_list_friends(id_user)
    
    
@pytest.mark.parametrize("id_user,id_friends", [
    (1, 2),
    (2, 3)
])
async def test_accept_friends(id_user, id_friends):
    accept = await FriendsDAO.accept_friends(id_user, id_friends)
    
    
@pytest.mark.parametrize("id_user,id_friends", [
    (3, 4)
])
async def test_reject_friends(id_user, id_friends):
    reject = await FriendsDAO.reject_friends(id_user, id_friends)
    

@pytest.mark.parametrize("id_user,id_friends", [
    (3, 4)
])
async def test_delete_friends(id_user, id_friends):
    delete = await FriendsDAO.delete_friends(id_user, id_friends)
    
    
@pytest.mark.parametrize("id_user", [
    (1)
])
async def test_list_possible_friends(id_user):
    list = await FriendsDAO.list_possible_friends(id_user)
    

@pytest.mark.parametrize("id_user", [
    (1)
])
async def test_my_friends(id_user):
    list = await FriendsDAO.my_friends(id_user)
    
    print(list)