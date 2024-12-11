from fastapi import APIRouter, Depends, Response, status, Request
from fastapi.exceptions import HTTPException
from fastapi.security import HTTPBearer
from starlette.responses import JSONResponse

from src.application.exceptions.token import ExpiredSignature, InvalidTokenType, InvalidTokenPayload
from src.application.exceptions.user import InvalidCredentials
from src.application.use_cases.user import UserService
from src.domain.user.dto.user import UserLogin, UserCreate, OutputUser
from src.domain.user.exceptions.user import UserAlreadyExists, UserNotFound
from src.infrastructure.dependencies import get_user_service
from src.infrastructure.security.jwt_service import decode_jwt
from src.presentation.api.auth.requests import CreateUserRequest, LoginUserRequest
from src.presentation.api.auth.responses import TokenResponse, SuccessRefreshResponse, SuccessLogoutResponse, \
    SuccessLoginResponse

auth_router = APIRouter(prefix="/auth", tags=["Auth"])

http_bearer = HTTPBearer()


@auth_router.post("/register")
async def register_user(
        user: CreateUserRequest,
        response: Response,
        user_service: UserService = Depends(get_user_service),
) -> OutputUser:
    try:
        response.status_code = status.HTTP_201_CREATED
        user = await user_service.register_user(UserCreate(**user.dict()))
        return user
    except UserAlreadyExists as e:
        raise HTTPException(status_code=409, detail=str(e))


@auth_router.post("/login")
async def login_user(user: LoginUserRequest, user_service: UserService = Depends(get_user_service)):
    try:
        token_credentials = await user_service.login_user(UserLogin(**user.dict()))
    except (UserNotFound, InvalidCredentials):
        raise HTTPException(status_code=404, detail="Invalid credentials")
    response = JSONResponse(status_code=200, content=SuccessLoginResponse().dict())
    response.set_cookie(
        key="access_token", value=token_credentials.get("access_token"), httponly=True, max_age=60 * 60 * 24 * 14
    )
    response.set_cookie(
        key="refresh_token", value=token_credentials.get("refresh_token"), httponly=True, max_age=60 * 60 * 24 * 14
    )
    return response


@auth_router.get("/refresh")
async def refresh_user(request: Request, user_service: UserService = Depends(get_user_service)) -> TokenResponse:
    refresh_token = request.cookies.get("refresh_token")
    try:
        access_token, refresh_token = await user_service.refresh_user(refresh_token)
    except (ExpiredSignature, InvalidTokenType, InvalidTokenPayload) as e:
        raise HTTPException(status_code=401, detail=f"Token error: {e}")
    success_response = SuccessRefreshResponse()
    response = JSONResponse(success_response.dict())
    response.set_cookie(key="access_token", value=access_token, httponly=True)
    response.set_cookie(key="refresh_token", value=refresh_token, httponly=True)
    return response


@auth_router.get("/status")
async def check_auth_status(request: Request) -> OutputUser:
    access_token = request.cookies.get("access_token")
    if not access_token:
        raise HTTPException(status_code=403, detail="Not authorized")
    try:
        payload = await decode_jwt(access_token)
        user_id = payload.get("id")
        if not user_id:
            raise HTTPException(status_code=403, detail="Invalid token")
    except Exception as ex:
        raise HTTPException(status_code=401, detail=f"Token error: {ex}")
    return OutputUser(
        username=payload.get("sub"), email=payload.get("email"), id=user_id, is_active=payload.get("is_active")
    )


@auth_router.get("/logout")
async def logout_user(response: Response) -> SuccessLogoutResponse:
    response.delete_cookie("access_token", path="/")
    response.delete_cookie("refresh_token", path="/")
    return SuccessLogoutResponse
