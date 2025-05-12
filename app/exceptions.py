from typing import Any, Dict

from fastapi import HTTPException, status
from typing_extensions import Annotated, Doc


class LKException(HTTPException):
    status_code = 500
    detail = ""

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)

class UserAlreadyExistsException(LKException):
    status_code=status.HTTP_409_CONFLICT
    detail="Пользователь уже существует"

class IncorrectEmailOrPasswordException(LKException):
    status_code=status.HTTP_401_UNAUTHORIZED
    detail="Неверная почта или пароль"

class IncorrectPasswordException(LKException):
    status_code=status.HTTP_401_UNAUTHORIZED
    detail="Неверный пароль"

class TokenExpiredException(LKException):
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Токен истек"

class TokenAbsentException(LKException):
    status_code=status.HTTP_401_UNAUTHORIZED
    detail="Токен отсутствует"

class IncorrectTokenFormatException(LKException):
    status_code=status.HTTP_401_UNAUTHORIZED
    detail="Неверный формат токена"

class UserIsNotPresentException(LKException):
    status_code=status.HTTP_401_UNAUTHORIZED

class AlreadyFriends(LKException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Пользователи уже друзья или приглашение уже отправлено"

class UserNotFound(LKException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Пользователь не найден"

class InvitationNotFound(LKException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Приглашение не найдено"

class UserNotInFriendsList(LKException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Пользователя нет в списке друзей"

class CannotAddYourself(LKException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Нельзя отправить приглашение в друзья самому себе"

class NameAlreadyTaken(LKException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Данное название уже занято"

class GroupNotFound(LKException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Группа не найдена"

class UserAlreadyInGroup(LKException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Вы уже состоит в группе"

class UserIsGroupOwner(LKException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Вы является владельцем группы"

class UserIsNotGroupOwner(LKException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Вы не является владельцем группы"

class UserAlreadyAcceptInGroup(LKException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Уже учасник"