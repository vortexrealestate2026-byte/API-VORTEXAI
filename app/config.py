import os


class Settings:

    PROJECT_NAME = "Vortex AI Platform"

    DATABASE_URL = os.getenv(
        "DATABASE_URL",
        "postgresql://postgres:postgres@localhost:5432/vortex"
    )

    REDIS_URL = os.getenv(
        "REDIS_URL",
        "redis://localhost:6379"
    )

    JWT_SECRET = os.getenv(
        "JWT_SECRET",
        "super-secret-key"
    )

    PIPELINE_INTERVAL = int(
        os.getenv("PIPELINE_INTERVAL", 1800)
    )


settings = Settings()
