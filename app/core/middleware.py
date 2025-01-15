from fastapi.middleware.cors import CORSMiddleware
from .config import settings
import logging

def setup_cors(app):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["GET", "POST"],
        allow_headers=["*"],
    )

logging.basicConfig(
    level= getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # Log message format
    handlers=[
        logging.StreamHandler(), # Logs to the console
        logging.FileHandler('socialvidz.log') 
    ] if settings.DEBUG else []
)

# Create a logger instance
logger = logging.getLogger(settings.APP_NAME)
