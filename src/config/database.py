from pydantic.v1 import BaseSettings, Field


class DbConfig(BaseSettings):
    postgres_username: str = Field(env="POSTGRES_USERNAME")
    postgres_password: str = Field(env="POSTGRES_PASS")
    postgres_host: str = Field(default="localhost", env="POSTGRES_HOST")
    postgres_port: int = Field(default=5432, env="POSTGRES_PORT")
    postgres_bd_name: str = Field(env="POSTGRES_BD_NAME")

    def get_db_url(self):
        return (
            f"postgresql+asyncpg://{self.postgres_username}:"
            f"{self.postgres_password}@"
            f"{self.postgres_host}:"
            f"{self.postgres_port}/{self.postgres_bd_name}"
        )

    class Config:
        env_file = ".env"
