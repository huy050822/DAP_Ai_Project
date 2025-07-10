from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    mongodb_url: str = "mongodb://localhost:27017"
    database_name: str = "analytics_db"
    
    class Config:
        env_file = ".env"

settings = Settings()
