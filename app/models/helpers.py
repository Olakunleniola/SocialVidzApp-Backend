from sqlalchemy.ext.asyncio import AsyncSession
from .video_download import VideoDownload
from app.core.middleware import logger
from sqlalchemy.exc import SQLAlchemyError

async def log_video_download(db: AsyncSession, title: str, platform: str, size: float, url: str, ip_address: str):
    try:
        log_entry = VideoDownload(
            title=title.strip(),
            platform=platform.strip().lower(),
            size=size,
            url=url.strip(),
            ip_address=ip_address.strip(),
        )
        db.add(log_entry)
        await db.commit()
        await db.refresh(log_entry)
        return log_entry
    except SQLAlchemyError as e:
        await db.rollback()
        logger.error(f"Database error while logging video download: {e}")
        raise RuntimeError(f"Database error: {e}")
    except Exception as e:
        logger.error(f"Unexpected error while logging video download: {e}")
        raise RuntimeError(f"Unexpected error: {e}")