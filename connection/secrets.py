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

    class Config:
        env_file = "connection/.env"
settings = Settings()