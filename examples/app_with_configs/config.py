from pydantic import BaseSettings

class Settings(BaseSettings):
    app_name: str = "example app"
    app_key: str = "secretkey"

    class Config:
        env_file = ".env"

settings = Settings()
