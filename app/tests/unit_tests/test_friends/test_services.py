import pytest
from app.friends.services import invite_friends


@pytest.mark.parametrize("id_user,id_friends", [
    (1, 2),
])
async def test_services_invite_friends(id_user, id_friends):
    list = await invite_friends(id_user, id_friends)
    
    print(list)