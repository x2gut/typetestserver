from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, Form
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jwt import ExpiredSignatureError
from starlette.responses import FileResponse

from src.application.exceptions.profile import FileIsNotAnImage
from src.application.use_cases.profile import ProfileService
from src.infrastructure.dependencies import get_profile_service
from src.infrastructure.security.jwt_service import decode_jwt

profile_router = APIRouter(prefix='/profile', tags=["Profile"])

http_bearer = HTTPBearer()


async def validate_user(credentials: HTTPAuthorizationCredentials = Depends(http_bearer)):
    try:
        payload = await decode_jwt(credentials.credentials)
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Signature has expired")
    if not payload.get("id"):
        raise HTTPException(status_code=401, detail="Invalid payload")
    return int(payload.get("id"))


@profile_router.get('/profile-picture')
async def get_profile_picture(user_id: int,
                              profile_service: ProfileService = Depends(get_profile_service)):
    profile_pic_url = await profile_service.get_profile_picture(user_id)
    return FileResponse(profile_pic_url, media_type="image")


@profile_router.put("/profile-picture")
async def update_profile_picture(user_id: int = Depends(validate_user),
                                 profilePicture: UploadFile = File(...),
                                 profile_service: ProfileService = Depends(get_profile_service)) -> FileResponse:
    try:
        profile_picture_url = await profile_service.upload_profile_picture(profilePicture)
        await profile_service.update_profile_picture(profile_picture_url, user_id)
    except FileIsNotAnImage:
        raise HTTPException(status_code=400, detail="File is not an image")
