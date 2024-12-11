import uvicorn
from fastapi import FastAPI, Request
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from src.presentation.api.auth.routes import auth_router
from src.presentation.api.oath.routes import oauth_router
from src.presentation.api.profile.routes import profile_router
from src.presentation.api.result.routes import result_router
from src.presentation.api.user.routes import user_router
from src.presentation.api.user_config.routes import config_router


class AppConfig:
    def __init__(self, secret_key: str, allowed_origins: list, routers: list):
        self.secret_key = secret_key
        self.allowed_origins = allowed_origins
        self.routers = routers


def create_app(config: AppConfig):
    app = FastAPI()

    @app.middleware("http")
    async def add_token_to_headers(request: Request, call_next):
        access_token = request.cookies.get("access_token")
        if access_token:
            request.headers.__dict__["_list"].append((b"authorization", f"Bearer {access_token}".encode()))
        response = await call_next(request)
        return response

    app.add_middleware(SessionMiddleware, secret_key=config.secret_key)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=config.allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    for router in config.routers:
        app.include_router(router)

    return app


app_config = AppConfig(
    secret_key="secret-key-12345",
    allowed_origins=["http://localhost:3000", "http://localhost:8000"],
    routers=[auth_router, oauth_router, profile_router, result_router, user_router, config_router]
)
app = create_app(app_config)

if __name__ == "__main__":
    uvicorn.run(app, port=8000)
