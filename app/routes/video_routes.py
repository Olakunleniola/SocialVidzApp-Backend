from fastapi import APIRouter, HTTPException, Query, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.dependencies import get_db
from app.models.helpers import log_video_download
from app.services.video_services import get_video_info, stream_response, get_video_size, verify_video_metadata
from app.utils.validation import validate_url, validate_platform
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field, HttpUrl
from app.core.middleware import logger
from app.core.config import settings
import unicodedata

router = APIRouter()

class VideoRequest(BaseModel):
    url: HttpUrl
    platform: str = Field(..., description="Platform, e.g., 'youtube'")
    title: str

@router.get("/info")
async def get_info(url: str = Query(...)):
    """
    Get video information by URL.
    """
    try:

        logger.info(f"Geting info of the URL {str(url)}")
        
        platform = validate_url(url)
        
        video_info = await get_video_info(url, platform)
        
        return {"status": "success", "data": video_info}
    
    except Exception as e:
        raise e

@router.post("/download")
async def download_video(
    request: VideoRequest, 
    db: AsyncSession = Depends(get_db), 
    client_request: Request = None
):
    """
    Download a video by providing the URL, platform, and title.
    """
    try:
        # Extract request data
        url = str(request.url)
        title = unicodedata.normalize('NFKD', request.title).encode('ascii', 'ignore').decode('ascii')
        platform = request.platform

        # Validate the platform
        validate_platform(platform)
        await verify_video_metadata(url)
 
        # Fetch video size
        file_size = await get_video_size(url)
        
        if int(file_size) > settings.MAX_FILE_SIZE_MB * 1024 * 1024:
            raise HTTPException(
                status_code=413,
                detail=f"File size exceeds the limit of {settings.MAX_FILE_SIZE_MB} MB."
            )
        
        # Log the video download
        user_ip = client_request.client.host if client_request else "unknown"
        await log_video_download(db, title, platform, float(file_size), url, user_ip)

        # Set headers for the streaming response
        headers = {
            "Content-Disposition": f"attachment; filename={title}.mp4",
            "Content-Type": "video/mp4",
            "Content-Length": str(file_size),
        }

        logger.info("Streaming video.....")
        # Stream the video file
        return StreamingResponse(stream_response(url), headers=headers)
    
    
    except Exception as e:
        # logger.exception(f"Unexpected Error: {str(e)}")
        raise e