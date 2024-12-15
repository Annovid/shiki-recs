import os

from pydantic_settings import BaseSettings

ENV_PATH = os.path.join(os.getcwd(), "resources", ".env")


class Settings(BaseSettings):
    DB_URL: str = ""
    DEBUG: bool = False

    DEFAULT_USERS_CNT: int = 1_500_000
    SCORE_EXACT_USER_CNT: bool = False
    SLEEP_TIME: float = 0.03
    USERS_COUNT: int = 1000

    class Config:
        env_file = ENV_PATH


settings = Settings()
