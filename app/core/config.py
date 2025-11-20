from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Celery
    CELERY_BROKER_URL: str
    CELERY_BACKEND_URL: str

    # SMTP
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: str
    MAIL_PORT: int = 465
    MAIL_SERVER: str = "smtp.mail.ru"
    MAIL_TLS: bool = False
    MAIL_SSL: bool = True

    # Внешнее API
    external_api_base: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
