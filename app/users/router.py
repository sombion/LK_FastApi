import os
import shutil
from uuid import uuid4

from fastapi import APIRouter, Depends, File, HTTPException, Response, UploadFile
from fastapi.responses import FileResponse, JSONResponse

from app.exceptions import IncorrectEmailOrPasswordException, UserAlreadyExistsException
from app.users.auth import (
    authenticate_user,
    create_access_token,
    edit_password,
    get_password_hash,
)
from app.users.dao import UsersDAO
from app.users.dependencies import get_current_user
from app.users.models import Users
from app.users.schemas import SEditPassword, SIdUser, SLogin, SRegister

router = APIRouter(
	prefix="/auth",
	tags=["Auth & Пользователи"]
)

@router.post("/register")
async def register_user(user_data: SRegister):
    existing_user = await UsersDAO.find_one_or_none(login=user_data.login)
    if existing_user:
        raise UserAlreadyExistsException
    hashed_password = get_password_hash(user_data.password)
    return await UsersDAO.create_user(
        name=user_data.name,
        login=user_data.login,
        hash_password=hashed_password,
        email=user_data.email,
    )

@router.post("/login")
async def login_user(response: Response, user_data: SLogin):
    user = await authenticate_user(user_data.login, user_data.password)
    if not user:
        raise IncorrectEmailOrPasswordException
    access_token = create_access_token({"sub": str(user.id)})
    response.set_cookie("lk_access_token", access_token, httponly=True)
    await UsersDAO.upgrade_visit_count(user.id)
    return {"access_token": access_token}

@router.post("/logout")
async def logout_user(response: Response):
    response.delete_cookie("lk_access_token")
    return {"detail": "Вы успешно вышли"}

@router.get("/me")
async def read_users_me(current_user: Users = Depends(get_current_user)):
    return current_user

@router.patch("/edit-password")
async def api_edit_password(data_password: SEditPassword, current_user: Users = Depends(get_current_user)):
    return await edit_password(
        id=current_user.id,
        last_password=data_password.last_password,
        new_password=data_password.new_password
    )

@router.get("/count-login")
async def api_count_login(current_user: Users = Depends(get_current_user)):
    return {"count": current_user.count_login}



@router.post("/upload-image")
async def upload_image(file: UploadFile = File(...), current_user: Users = Depends(get_current_user)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Файл не является изображением")

    file_extension = os.path.splitext(file.filename)[1]
    new_filename = f"{uuid4()}{file_extension}"
    file_path = os.path.join("app/img/", new_filename)

    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при сохранении файла: {str(e)}")

    await UsersDAO.upgrade_img(current_user.id, file_path)

    return JSONResponse(content={"filename": new_filename, "message": "Изображение успешно загружено"})

@router.get("/avatar")
def get_user_avatar(current_user: Users = Depends(get_current_user)):
    avatar_path = current_user.img
    if not os.path.exists(avatar_path):
        return FileResponse("app/img/default.jpg")
    return FileResponse(avatar_path, media_type="image/jpeg")


@router.post("/avatar")
async def get_current_user_avatar(data: SIdUser):
    current_user = await UsersDAO.find_by_id(id=data.id_user)
    avatar_path = current_user.img
    if not os.path.exists(avatar_path):
        return FileResponse("app/img/default.jpg")
    return FileResponse(avatar_path, media_type="image/jpeg")
