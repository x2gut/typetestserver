from authlib.integrations.base_client import OAuthError
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from authlib.integrations.starlette_client import OAuth
from starlette.requests import Request

from src.application.use_cases.user import UserService
from src.config.google_oauth import GoogleAuthConfig
from src.domain.user.dto.user import UserOauth
from src.infrastructure.dependencies import get_user_service

oauth_router = APIRouter(prefix="/oauth", tags=["Oath"])
google_oauth_config = GoogleAuthConfig()

oauth = OAuth()
oauth.register(
    name="google",
    client_id=google_oauth_config.client_id,
    client_secret=google_oauth_config.client_secret,
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    authorize_state="secret-key-12345",
    client_kwargs={
        "scope": "openid email profile",
    },
)


@oauth_router.get("/google/login")
async def login(request: Request):
    return await oauth.google.authorize_redirect(request, google_oauth_config.redirect_uri)


@oauth_router.get("/google/callback")
async def auth_callback(request: Request, user_service: UserService = Depends(get_user_service)):
    try:
        token = await oauth.google.authorize_access_token(request)
    except OAuthError as e:
        raise HTTPException(status_code=401, detail=f"Could not validate credentials {e}")
    user_info = token.get("userinfo")
    google_user_id = user_info.get("sub")
    token_credentials = await user_service.login_oauth_user(
        UserOauth(email=user_info.get("email"), google_id=google_user_id, username=user_info.get("name"))
    )
    response = RedirectResponse("http://localhost:3000/")
    response.set_cookie(
        key="access_token", value=f"{token_credentials.get('access_token')}", httponly=True, max_age=60 * 60 * 24 * 14
    )
    response.set_cookie(
        key="refresh_token", value=f"{token_credentials.get('refresh_token')}", httponly=True, max_age=60 * 60 * 24 * 14
    )
    return response
