from datetime import datetime, timedelta

from jose import jwt
from passlib.context import CryptContext

from app.config import settings
from app.exceptions import IncorrectPasswordException, UserNotFound
from app.users.dao import UsersDAO

pwd_context = CryptContext(schemes=["bcrypt"])

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(hours=72)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, settings.ALGORITHM
    )
    return encoded_jwt

async def authenticate_user(login: str, password: str):
    user = await UsersDAO.find_one_or_none(login=login)
    if not (user and verify_password(password, user.hash_password)):
        return None
    return user

async def edit_password(id: int, last_password: str, new_password: str):
    user = await UsersDAO.find_one_or_none(id=id)
    
    if not (user and verify_password(last_password, user.hash_password)):
        raise IncorrectPasswordException
    
    hash_new_password = get_password_hash(new_password)
    
    result = await UsersDAO.edit_password(
        id=id,
        new_password=hash_new_password
    )

    return result