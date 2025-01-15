import sys
import os

# Add the project root to PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from app.models.database import engine
from app.models.video_download import VideoDownload

# Initialize the database
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(VideoDownload.metadata.create_all)
    print("Database initialized successfully!")

# Entry point for the script
if __name__ == "__main__":
    import asyncio
    asyncio.run(init_db())
