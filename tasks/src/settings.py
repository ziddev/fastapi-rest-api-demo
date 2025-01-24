from pydantic import BaseSettings


class Settings(BaseSettings):
    DATA_DIRECTORY_PATH: str = "data"


settings = Settings()
