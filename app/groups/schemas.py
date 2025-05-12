from pydantic import BaseModel, Field


class SCreateGroup(BaseModel):
    title: str = Field(...)
    description: str = Field(...)


class SGroup(BaseModel):
    id: int = Field(...)


class SAcceptInGroup(BaseModel):
    members_group_id: int = Field(...)