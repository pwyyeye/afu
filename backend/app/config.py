from pydantic_settings import BaseSettings
from typing import List
import json


class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./data/afu.db"
    JWT_SECRET_KEY: str = "dev-secret-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    DASHSCOPE_API_KEY: str = ""
    QWEN_MODEL: str = "qwen3.6-plus"
    QWEN_VL_MODEL: str = "qwen3-vl-max"

    SMS_ACCESS_KEY_ID: str = ""
    SMS_ACCESS_KEY_SECRET: str = ""
    SMS_SIGN_NAME: str = ""
    SMS_TEMPLATE_CODE: str = ""

    DEBUG: bool = True
    PORT: int = 8002
    CORS_ORIGINS: str = '["http://localhost:5173","http://localhost:3000","https://pwyyeye.github.io"]'

    @property
    def cors_origins_list(self) -> List[str]:
        if not self.CORS_ORIGINS:
            return []
        return json.loads(self.CORS_ORIGINS)

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
