import os

class Config:
    # General settings
    APP_NAME = os.environ.get("APP_NAME", "Social Vidz")
    ENVIRONMENT = os.environ.get("ENVIRONMENT", "development")
    DEBUG = bool(int(os.environ.get("DEBUG", 0)))
    PORT = int(os.environ.get("PORT", 8000))

    # Database settings
    DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite+aiosqlite:///./social_vidz.db")
    DATABASE_ECHO = os.environ.get("DATABASE_ECHO", "false").lower() == "true"

    # CORS settings
    print(DEBUG)
    ALLOWED_ORIGINS = os.environ.get("ALLOWED_ORIGINS", "").split(",") if not DEBUG else ["http://localhost:5173"]

    # API settings
    API_VERSION = os.environ.get("API_VERSION", "v1")
    BASE_PATH = f"/social_vidz/api/{API_VERSION}"

    # App Settings 
    MAX_FILE_SIZE_MB = os.environ.get("MAX_FILE_SIZE_MB", 500)
    SUPPORTED_FORMATS = ["video/mp4", "video/webm", "video/ogg"] + os.environ.get("SUPPORTED_FORMATS", "").split()
    PROXY_URL = os.getenv('PROXY_URL', None)
    COOKIES_DATA = os.getenv('COOKIES_DATA', "")
    # Logging settings
    
    LOG_LEVEL =  "INFO" if DEBUG else "ERROR"

settings = Config()