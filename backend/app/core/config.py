from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "AI Freelancer Matching and Quotation Optimization System"
    database_url: str = "sqlite:///./freelancer.db"
    cors_origins: str = "http://localhost:5173"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
