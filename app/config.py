from pydantic_settings import BaseSettings
from typing import Optional
import os
from datetime import timedelta


class Settings(BaseSettings):
    SECRET_KEY: str = "a9f7e8c1b2d3g4h5i6j7k8l9m0n1o2p3q4r5s6t7u8v9w0x1y2z3"  
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    DATABASE_URL: str = "sqlite:///./parking_management.db"
    
    # For testing
    TEST_DATABASE_URL: Optional[str] = "sqlite:///./test_parking_management.db"
    
    class Config:
        env_file = ".env"


settings = Settings()