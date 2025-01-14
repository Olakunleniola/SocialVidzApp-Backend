from fastapi import APIRouter, HTTPException, Query, Depends, Request
from sqlalchemy.orm import Session
from app.models.dependencies import get_db
from app.models.helpers import log_video_download
from app.services.video_services import get_video_info, stream_response, get_video_size, verify_video_metadata
from app.utils.validation import validate_url, validate_platform
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field, HttpUrl
from app.core.middleware import logger
from app.core.config import settings

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
        
        validate_url(url)
        
        video_info = await get_video_info(url)
        
        return {"status": "success", "data": video_info}
    
    except Exception as e:
        raise e

@router.post("/download")
async def download_video(
    request: VideoRequest, 
    db: Session = Depends(get_db), 
    client_request: Request = None
):
    """
    Download a video by providing the URL, platform, and title.
    """
    try:
        # Extract request data
        url = str(request.url)
        title = request.title
        platform = request.platform

        # Validate the platform
        validate_platform(platform)
        print("verfying")
        await verify_video_metadata(url)
        print("verified")

        # Fetch video size
        print("getting video size")
        file_size = await get_video_size(url)
        print(f"Got video size {file_size}")
        
        if int(file_size) > settings.MAX_FILE_SIZE_MB * 1024 * 1024:
            raise HTTPException(
                status_code=413,
                detail=f"File size exceeds the limit of {settings.MAX_FILE_SIZE_MB} MB."
            )
        


        # Log the video download
        user_ip = client_request.client.host if client_request else "unknown"
        print("Logging to database")
        await log_video_download(db, title, platform, file_size, url, user_ip)

        # Set headers for the streaming response
        headers = {
            "Content-Disposition": f"attachment; filename={title}.mp4",
            "Content-Type": "video/mp4",
            "Content-Length": str(file_size),
        }

        logger.info("Streaming video.....")
        print("Streaming video.....")

        # return {"message": "sucess"}

        # Stream the video file
        return StreamingResponse(stream_response(url), headers=headers)
    
    
    except Exception as e:
        # logger.exception(f"Unexpected Error: {str(e)}")
        raise e