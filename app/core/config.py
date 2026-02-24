from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "Train Booking API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"

    # JWT
    SECRET_KEY: str = "your-super-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Database
    DATABASE_URL: str = "sqlite+aiosqlite:///./train_booking.db"

    # Stripe
    STRIPE_SECRET_KEY: str = "sk_test_..."

    class Config:
        env_file = ".env"


settings = Settings()
