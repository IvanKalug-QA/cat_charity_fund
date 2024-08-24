from typing import Union

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from fastapi_users.authentication import (
    AuthenticationBackend, BearerTransport, JWTStrategy)
from fastapi_users import BaseUserManager, IntegerIDMixin, FastAPIUsers
from fastapi_users.exceptions import InvalidPasswordException

from app.core.db import get_async_session
from app.models import User
from app.core.config import settings
from app.schemas.user import UserCreate


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)


bearer_transport = BearerTransport(tokenUrl='auth/jwt/login')


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(settings.secret, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name='jwt',
    transport=bearer_transport,
    get_strategy=get_jwt_strategy
)


class UserManger(IntegerIDMixin, BaseUserManager[User, int]):
    async def validate_password(
            self, password: str, user: Union[UserCreate, User]) -> None:
        if len(password) < 3:
            raise InvalidPasswordException(
                reason='Password should be at least 3 characters'
            )
        if user.email in password:
            raise InvalidPasswordException(
                reason='Password should not contain e-mail'
            )


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManger(user_db)


fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend]
)

current_user = fastapi_users.current_user(active=True)
current_superuser = fastapi_users.current_user(active=True, superuser=True)