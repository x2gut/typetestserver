from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.use_cases.config import ConfigService
from src.application.use_cases.profile import ProfileService
from src.application.use_cases.result import ResultService
from src.application.use_cases.user import UserService
from src.infrastructure.database.base import get_session
from src.infrastructure.database.repositories.config import ConfigRepository
from src.infrastructure.database.repositories.profile import ProfileRepository
from src.infrastructure.database.repositories.result import ResultRepository
from src.infrastructure.database.repositories.user import UserRepository


async def get_user_repo(session: AsyncSession = Depends(get_session)):
    return UserRepository(session)


async def get_result_repo(session: AsyncSession = Depends(get_session)):
    return ResultRepository(session)


async def get_config_repo(session: AsyncSession = Depends(get_session)):
    return ConfigRepository(session=session)


async def get_profile_repo(session: AsyncSession = Depends(get_session)):
    return ProfileRepository(session)


async def get_user_service(user_repo: UserRepository = Depends(get_user_repo)):
    return UserService(user_repo)


async def get_result_service(result_repo: ResultRepository = Depends(get_result_repo)):
    return ResultService(result_repo)


async def get_config_service(config_repo: ConfigRepository = Depends(get_config_repo)):
    return ConfigService(config_repo)


async def get_profile_service(profile_repo: ProfileRepository = Depends(get_profile_repo)):
    return ProfileService(profile_repo)
