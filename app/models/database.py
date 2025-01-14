from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Database URL (For SQLite, change to your DB URI in production)
DATABASE_URL = settings.DATABASE_URL

# Setup SQLAlchemy engine and session
engine = create_async_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {},
    echo=settings.DATABASE_ECHO
)

async_session = sessionmaker(
    autocommit=False, 
    autoflush=False, 
    class_=AsyncSession, 
    bind=engine
)

