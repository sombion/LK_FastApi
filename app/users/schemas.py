from pydantic import BaseModel, Field

class SRegister(BaseModel):
    name: str = Field(...)
    login: str = Field(...)
    password: str = Field(...)
    email: str | None = Field(...)
    img: str | None = Field(default=None)
    
class SLogin(BaseModel):
    login: str = Field(...)
    password: str = Field(...) 
    
class SEditPassword(BaseModel):
    last_password: str = Field(...)
    new_password: str = Field(...)
    
class SIdUser(BaseModel):
    id_user: int = Field(...)