from pydantic_settings import BaseSettings



class Settings(BaseSettings):
    # App
    APP_NAME: str
    ENVIRONMENT: str
    DEBUG: bool

    # Database
    DATABASE_URL: str

    # Security
    SECRET_KEY: str
    JWT_ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    # APIs
    GOOGLE_MAPS_API_KEY: str
    OPENAI_API_KEY: str

    # Export
    EXPORT_FOLDER: str

    class Config:
        env_file = ".env"


settings = Settings()
