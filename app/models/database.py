from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings


# Database URL
DATABASE_URL = settings.DATABASE_URL

if not settings.DEBUG:
    # Create MongoDB client
    mongo_client = AsyncIOMotorClient(settings.DATABASE_URL)
    mongo_db = mongo_client[settings.MONGO_DB_NAME]
else:
    # Setup SQLite engine and session
    engine = create_async_engine(
        DATABASE_URL, 
        connect_args={"check_same_thread": False},
        echo=settings.DATABASE_ECHO
    )

    async_session = sessionmaker(
        autocommit=False, 
        autoflush=False, 
        class_=AsyncSession, 
        bind=engine
    )