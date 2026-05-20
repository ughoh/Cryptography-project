from pydantic import BaseModel
from pydantic_settings import BaseSettings


class CorsSettings(BaseModel):
    allow_origins: list[str] = (
        [
            "http://localhost:5173",
            "http://127.0.0.1:5173",
        ],
    )
    allow_credentials: bool = (True,)
    allow_methods: list[str] = ["POST"]
    allow_headers: list[str] = ["*"]


class AppSettings(BaseModel):
    title: str = "Cryptography Project API"
    description: str = (
        "Secure asynchronous API for file encryption using AES-256-GCM algorithm"
    )
    version: str = "1.0.0"


class AppRunSettings(BaseModel):
    app: str = "app.main:app"
    host: str = ("127.0.0.1",)
    port: int = (8000,)
    reload: bool = True


class Settings(BaseSettings):
    cors: CorsSettings = CorsSettings()
    app_settings: AppSettings = AppSettings()
    app_run: AppRunSettings = AppRunSettings()


settings = Settings()
