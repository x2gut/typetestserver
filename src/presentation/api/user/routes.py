from fastapi import APIRouter, Depends, Response, status
from fastapi.responses import RedirectResponse
from fastapi.exceptions import HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jwt import ExpiredSignatureError

from src.application.exceptions.user import InvalidCredentials
from src.application.use_cases.user import UserService
from src.domain.user.dto.user import OutputUser
from src.domain.user.exceptions.user import UserNotFound, UserAlreadyExists
from src.infrastructure.dependencies import get_user_service
from src.infrastructure.security.jwt_service import decode_jwt
from src.presentation.api.user.requests import UpdateUserEmailRequest, SendEmailRequest
from src.presentation.api.user.respones import SuccessEmailChangeResponse

user_router = APIRouter(prefix="/user", tags=["User"])

http_bearer = HTTPBearer()

async def validate_user(credentials: HTTPAuthorizationCredentials = Depends(http_bearer)):
    try:
        payload = await decode_jwt(credentials.credentials)
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Signature has expired")
    if not payload.get("id"):
        raise HTTPException(status_code=401, detail="Invalid payload")
    return int(payload.get("id"))

@user_router.get("/")
async def get_user(user_id: int, user_service: UserService = Depends(get_user_service)) -> OutputUser:
    try:
        return await user_service.get_user_by_id(user_id)
    except UserNotFound:
        raise HTTPException(status_code=404, detail="User not found")


@user_router.put("/email")
async def update_user_email(user: UpdateUserEmailRequest,
                            user_service: UserService = Depends(get_user_service)) -> SuccessEmailChangeResponse:
    try:
        await user_service.change_user_email(user)
        return SuccessEmailChangeResponse
    except (InvalidCredentials, UserAlreadyExists) as e:
        if isinstance(e, InvalidCredentials):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
        elif isinstance(e, UserAlreadyExists):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already exists")


@user_router.post("/send-email")
async def confirm_email(user: SendEmailRequest,
                        user_service: UserService = Depends(get_user_service)) -> Response:
    try:
        await user_service.send_email(user)
        return Response(status_code=200)
    except UserNotFound:
        raise HTTPException(status_code=404, detail="User not found")


@user_router.get("/confirm-email")
async def confirm_email(token: str,
                        user_service: UserService = Depends(get_user_service)):
    try:
        payload = await decode_jwt(token)
        user_id = int(payload.get("sub"))
        await user_service.change_user_status(user_id, True)
        return RedirectResponse(url="http://localhost:3000/?confirmation=success")
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Token error: {e}")
