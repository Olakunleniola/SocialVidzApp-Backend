from sqlalchemy.ext.asyncio import AsyncSession
from .video_download import VideoDownload

async def log_video_download(
    db: AsyncSession, title: str, platform: str, size: float, url: str, ip_address: str
):
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
    except Exception as e:
        await db.rollback()
        raise RuntimeError(f"Failed to log video download: {e}")
