from pydantic.v1 import BaseSettings, Field


class GoogleAuthConfig(BaseSettings):
    client_id: str = Field(env="google_client_id")
    client_secret: str = Field(env="google_client_secret")
    redirect_uri: str = "http://localhost:8000/oauth/google/callback"

    class Config:
        env_file = ".env"
