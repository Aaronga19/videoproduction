from pydantic_settings import BaseSettings

# Settings
class Settings(BaseSettings):
    database_hostname: str
    database_password: str
    database_name: str
    database_username: str
    database_port: int
    secret_key: str  
    algorithm: str
    access_token_expires_minutes: int
    # creds_path = str
    GOOGLE_APPLICATION_CREDENTIALS: str
    bucket_name: str
    class Config:
        env_file = "connection/.env"
settings = Settings()