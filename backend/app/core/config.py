"""
核心配置模块 - 生产版
"""

import os
from pydantic_settings import BaseSettings
from typing import Optional
import secrets


class Settings(BaseSettings):
    """应用配置"""
    
    APP_NAME: str = "悬赏任务平台"
    APP_VERSION: str = "3.0.0"
    DEBUG: bool = False
    
    DATABASE_URL: str = "sqlite:///./reward_task.db"
    
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    API_PREFIX: str = "/api"
    
    ALLOWED_ORIGINS: list = ["*"]
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
