from fastapi import Depends, HTTPException, Response, status
from fastapi.routing import APIRouter
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jwt import ExpiredSignatureError

from src.application.use_cases.config import ConfigService
from src.domain.config.dto.config import Config as ConfigDTO, UpdateConfig, UpdateTheme, CreateConfig
from src.domain.config.exceptions.config import ConfigDoesNotExistException
from src.infrastructure.dependencies import get_config_service
from src.infrastructure.security.jwt_service import decode_jwt
from src.presentation.api.user_config.responses import SuccessConfigUpdate, SuccessConfigCreate

config_router = APIRouter(tags=["User config"], prefix="/config")

http_bearer = HTTPBearer()


async def validate_user(credentials: HTTPAuthorizationCredentials = Depends(http_bearer)):
    try:
        payload = await decode_jwt(credentials.credentials)
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Signature has expired")
    if not payload.get("id"):
        raise HTTPException(status_code=401, detail="Invalid payload")
    return int(payload.get("id"))


@config_router.get("/{user_id}")
async def get_user_config(user_id: int,
                          config_service: ConfigService = Depends(get_config_service),
                          token_user_id: int = Depends(validate_user)) -> ConfigDTO:
    if user_id != token_user_id:
        raise HTTPException(status_code=403, detail="Forbidden")
    config = await config_service.get_config(user_id)
    if config is None:
        raise HTTPException(status_code=404, detail="User configuration not found")
    return config


@config_router.post("/")
async def create_user_config(config: CreateConfig,
                             response: Response,
                             user_id: int = Depends(validate_user),
                             config_service: ConfigService = Depends(get_config_service)):
    if user_id != config.user_id:
        raise HTTPException(status_code=403, detail="Forbidden")
    await config_service.create_config(user_id, config.config, config.theme)
    response.status_code = status.HTTP_201_CREATED
    return SuccessConfigCreate()


@config_router.put("/")
async def update_user_config(config: UpdateConfig,
                             user_id: int = Depends(validate_user),
                             config_service: ConfigService = Depends(get_config_service)) -> SuccessConfigUpdate:
    if user_id != config.user_id:
        raise HTTPException(status_code=403, detail="Forbidden")
    try:
        await config_service.update_config(user_id, config.config)
    except ConfigDoesNotExistException:
        raise HTTPException(status_code=404, detail="User configuration not found")
    return SuccessConfigUpdate()


@config_router.put("/theme")
async def update_user_theme(theme: UpdateTheme,
                            user_id: int = Depends(validate_user),
                            config_service: ConfigService = Depends(get_config_service)):
    if user_id != theme.user_id:
        raise HTTPException(status_code=403, detail="Forbidden")
    await config_service.update_theme(user_id, theme.theme)
    return SuccessConfigUpdate()
