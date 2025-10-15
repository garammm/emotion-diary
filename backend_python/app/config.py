from decouple import config

class Settings:
    DATABASE_URL: str = config("DATABASE_URL", default="sqlite:///./emotion_diary.db")
    SECRET_KEY: str = config("SECRET_KEY", default="your-secret-key-here")
    ALGORITHM: str = config("ALGORITHM", default="HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = config("ACCESS_TOKEN_EXPIRE_MINUTES", default=30, cast=int)
    DEBUG: bool = config("DEBUG", default=True, cast=bool)

settings = Settings()