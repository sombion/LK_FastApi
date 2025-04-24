from pydantic import BaseModel, Field


class SFriendsInvite(BaseModel):
    login_friend: str = Field(...)
    
class SFriends(BaseModel):
    id_friend: int = Field(...)
    
class SFriendsDetail(BaseModel):
    id_user: int = Field(...)
    id_friends: int = Field(...)