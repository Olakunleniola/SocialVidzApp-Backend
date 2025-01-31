import os
from pathlib import Path

class Config:
    # General settings
    BASE_DIR = Path(__file__).resolve().parent
    APP_NAME = os.environ.get("APP_NAME", "Social Vidz")
    ENVIRONMENT = os.environ.get("ENVIRONMENT", "development")
    DEBUG = bool(int(os.environ.get("DEBUG", 1)))
    PORT = int(os.environ.get("PORT", 8000))

    # Database settings
    DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite+aiosqlite:///./social_vidz.db")
    DATABASE_ECHO = os.environ.get("DATABASE_ECHO", "false").lower() == "true"
    # CORS settings
    ALLOWED_ORIGINS = os.environ.get("ALLOWED_ORIGINS", "").split(",") if not DEBUG else ["http://localhost:5173"]

    # API settings
    API_VERSION = os.environ.get("API_VERSION", "v1")
    BASE_PATH = f"/social_vidz/api/{API_VERSION}"

    # App Settings 
    MAX_FILE_SIZE_MB = os.environ.get("MAX_FILE_SIZE_MB", 500)
    SUPPORTED_FORMATS = ["video/mp4", "video/webm", "video/ogg"] + os.environ.get("SUPPORTED_FORMATS", "").split()
    PROXY_URL = os.getenv('PROXY_URL', None)
    COOKIES_PATH = os.path.abspath(os.path.join(BASE_DIR, "../../tmp/cookies.txt"))

    # Logging settings
    LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")

settings = Config()