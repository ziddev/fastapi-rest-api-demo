from pydantic import BaseSettings


class Settings(BaseSettings):
    DATA_DIRECTORY: str = "data"


settings = Settings()
