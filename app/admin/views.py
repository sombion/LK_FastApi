from sqladmin import ModelView
from app.friends.models import Friends
from app.users.models import Users

class UsersAdmin(ModelView, model=Users):
    column_list = [Users.id, Users.name, Users.login, Users.email]
    column_details_exclude_list = [Users.hash_password]
    can_delete = False
    name = "Пользователь"
    name_plural = "Пользователи"
    icon = "fa-solid fa-user"
    
class FriendsAdmin(ModelView, model=Friends):
    column_list = [Friends.id, Friends.id_user, Friends.id_friends, Friends.status_user, Friends.status_friends]
    name = "Друзья"
    name_plural = "Друзья"