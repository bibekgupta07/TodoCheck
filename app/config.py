# Import BaseSettings from pydantic for configuration management
from pydantic_settings import BaseSettings, SettingsConfigDict # pyright: ignore[reportMissingImports]


# Settings class to load environment variables
class Settings(BaseSettings):
    """
    Application configuration settings.
    Automatically loads values from .env file.
    """
    
    # MongoDB connection URL from environment variable
    MONGODB_URL: str
    
    # Database name where todos will be stored
    DATABASE_NAME: str
    
    # Collection name (similar to table name in SQL)
    COLLECTION_NAME: str
    
    # API configuration
    PROJECT_NAME: str = "Todo API"
    API_V1_PREFIX: str = "/api/v1"
    PORT: int = 8000

    # Pydantic v2 configuration using model_config
    model_config = SettingsConfigDict(
        env_file=".env",           # Load from .env file
        case_sensitive=True,        # Environment variables are case-sensitive
        extra="ignore"              # Ignore extra fields in .env file
    )


# Create single instance of settings to use throughout the app
settings = Settings() # type: ignore[call-arg]
