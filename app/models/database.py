from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Database URL
DATABASE_URL = settings.DATABASE_URL

# Setup SQLAlchemy engine and session
if "sqlite" not in DATABASE_URL:
    engine = create_async_engine(
        DATABASE_URL, 
        echo=settings.DATABASE_ECHO,
        pool_size=10 if not settings.DEBUG else None, 
        max_overflow=20 if not settings.DEBUG else 0
    )
else:
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