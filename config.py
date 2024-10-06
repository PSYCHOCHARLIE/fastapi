from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_hostname: str 
    database_port    : str  
    secret_key       : str
    database_password: str
    database_username: str
    database_name    : str
    algorithm        : str
    access_token_expire_minutes: int

    class Config:
        env_file = ".env"


settings = Settings()
print(settings.database_password, settings.database_username, settings.database_password)
