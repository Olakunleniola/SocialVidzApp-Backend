from sqlalchemy.ext.asyncio import AsyncSession
from .video_download import VideoDownload
from app.core.middleware import logger
from sqlalchemy.exc import SQLAlchemyError
from app.core.config import settings
from datetime import datetime, timezone





async def log_video_download(db: AsyncSession, title: str, platform: str, size: float, url: str, ip_address: str):
    log_entry = {
        "title": title.strip(),
        "platform": platform.strip().lower(),
        "size": size,
        "url": url.strip(),
        "ip_address": ip_address.strip(),
        "date": datetime.now(timezone.utc),
    }
    if settings.DEBUG:
        try:
            log = VideoDownload(**log_entry)
            db.add(log)
            await db.commit()
            await db.refresh(log)
            return log
        except SQLAlchemyError as e:
            await db.rollback()
            logger.error(f"Database error while logging video download: {e}")
            raise RuntimeError(f"Database error: {e}")
        except Exception as e:
            logger.error(f"Unexpected error while logging video download: {e}")
            raise RuntimeError(f"Unexpected error: {e}")
    else:
        try:
            result = await db.video_downloads.insert_one(log_entry)
            logger.info(f"Video download logged to MongoDB: {log_entry}")
            return await db.video_downloads.find_one({"_id": result.inserted_id})
        except Exception as e:
            logger.error(f"MongoDB error while logging video download: {e}")
            raise RuntimeError(f"Unexpected error: {e}")