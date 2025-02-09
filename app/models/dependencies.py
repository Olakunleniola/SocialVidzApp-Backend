from app.core.config import settings 

async def get_sql_db():
    from .database import async_session
    async with async_session() as session: 
        try:
            yield session
        finally:
            await session.close()

def get_mongo_db():
    from .database import mongo_db
    return mongo_db

async def get_db():
    if settings.DEBUG:
        async for session in get_sql_db():
            yield session
    else:
        yield get_mongo_db() 