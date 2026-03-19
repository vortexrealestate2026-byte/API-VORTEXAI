from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # Database
    DATABASE_URL: str
    REDIS_URL: str = "redis://localhost:6379/0"

    # JWT
    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # BatchData
    BATCHDATA_TOKEN: str = ""

    # HouseCanary
    HOUSECANARY_API_KEY: str = ""
    HOUSECANARY_API_SECRET: str = ""

    # DocuSign
    DOCUSIGN_ACCOUNT_ID: str = ""
    DOCUSIGN_INTEGRATION_KEY: str = ""
    DOCUSIGN_SECRET_KEY: str = ""
    DOCUSIGN_REDIRECT_URI: str = ""
    DOCUSIGN_BASE_URL: str = "https://www.docusign.net/restapi"

    # Twilio
    TWILIO_ACCOUNT_SID: str = ""
    TWILIO_AUTH_TOKEN: str = ""
    TWILIO_PHONE_NUMBER: str = ""

    # SendGrid
    SENDGRID_API_KEY: str = ""
    SENDGRID_FROM_EMAIL: str = ""

    # Stripe
    STRIPE_SECRET_KEY: str = ""
    STRIPE_WEBHOOK_SECRET: str = ""

    # Make.com
    MAKE_WEBHOOK_URL: str = ""

    # App
    ENVIRONMENT: str = "production"
    ALLOWED_ORIGINS: str = "*"

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
