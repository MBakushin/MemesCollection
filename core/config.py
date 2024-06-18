from pydantic_settings import BaseSettings



class Settings(BaseSettings):
    SQLALCHEMY_DATABASE_URL: str
    S3_ENDPOINT_URL: str
    S3_ACCESS_KEY: str
    S3_SECRET_KEY: str
    S3_BUCKET_NAME: str

    class Config:
        env_file = ".env"


settings = Settings()
