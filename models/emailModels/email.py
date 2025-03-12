from pydantic_settings import BaseSettings


class EmailSettings(BaseSettings):
    OAUTH_KEY: str
    EMAIL_SENDER: str
    EMAIL_PASSWORD: str
    EMAIL_HOST: str
    EMAIL_PORT: int

    class Config:
        orm_mode = True