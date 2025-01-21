import yt_dlp
from yt_dlp.utils import DownloadError, ExtractorError
from io import BytesIO
import httpx
from fastapi import HTTPException
from app.core.config import settings
from app.utils.helpers import timeout_wrapper
from app.core.middleware import logger
import asyncio

@timeout_wrapper(30.0)
async def get_video_size(url: str):
    """ Fetch video size from URL (HTTP HEAD request) """
    async with httpx.AsyncClient() as client:
        logger.info(f"Getting video size ......")
        try:
            response = await client.head(url)
            file_size = response.headers.get('Content-Length', 0)
            if not file_size.isdigit() or int(file_size) <= 0:
                raise HTTPException(
                    status_code=400,
                    detail="Unable to determine video file size: Invalid Url.. Copy the URL again and try again",
                )
            
            logger.info(f"Get video size successfully, video_size: {file_size} ......")
            
            return int(file_size)
        
        except httpx.ConnectTimeout as e:
            raise httpx.ConnectTimeout(f"Connection timed out while accessing the URL: {url}")
       
        except Exception as e:      
            raise Exception(f"An unexpected error occurred: {str(e)}")

@timeout_wrapper(60.0)
async def get_video_info(url):
    try:
        ydl_opts = {
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'quiet': True,
            'retries': 1,
            'extract_flat': True,
            'noplaylist': True,
            'prefer_ffmpeg': False,
            'logger': None,  # Suppress all yt-dlp logs
            'socket_timeout': 60,
            'proxy': settings.PROXY_URL,
            'cookiefile': settings.COOKIES_DATA
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            url = info.get("url")
            content_length = await get_video_size(url)
            title = info.get("title", 'Unknown')
            if title == 'Unknown':
                raise ExtractorError("Invalid or Malformed URk")
            return {
                'title': title,
                'url': url,
                'platform': info.get('extractor', 'Unknown'),
                'duration': info.get('duration', 'Unknown'),
                'uploader': info.get('uploader', 'Unknown'),
                'size': int(content_length),
                'view_count': info.get('view_count', 0),
                'like_count': info.get('like_count', 0),
                'is_live': info.get('is_live', False),
            }
        
    except (DownloadError, ExtractorError) as e:
        if "Sign in" in str(e):
            raise HTTPException(
                status_code=403,
                detail="This video requires authentication. Please try another video."
            )
        raise HTTPException(
            status_code=400,
            detail="Unable to process the provided URL. Ensure the link is valid and from a supported platform."
        )
    
    except Exception as e:
        raise e

@timeout_wrapper(60.0)
async def fetch_video_stream(url):
    ydl_opts = {
        "format": "best",
        "outtmpl": "-",
        'quiet': True,
    }
    buffer = BytesIO()
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        buffer.write(ydl.urlopen(info["url"]).read())
        buffer.seek(0)
        filename = f"{info.get('title', 'video')}.mp4"
    return buffer, filename

async def stream_response(url: str):
    logger.info(f"Initiating streaming for URL: {url}")
    headers = {
        "Connection": "keep-alive",
        "Accept-Encoding": "gzip, deflate, br",
        "User-Agent": "PostmanRuntime/7.43.0",
        "Cache-Control": "no-cache",
    }
    try:
        async with httpx.AsyncClient(timeout=httpx.Timeout(60.0)) as client:
            # Stream the response from the external server
            async with client.stream("GET", url, headers=headers) as response:
                # Yield data chunks one by one as they arrive
                async for chunk in response.aiter_bytes():
                    yield chunk  # Yield each chunk of video data as it arrives
    except (httpx.ConnectTimeout, asyncio.TimeoutError) as e:
        raise httpx.ConnectTimeout(f"Timeout while streaming video")

@timeout_wrapper(30.0)
async def verify_video_metadata(video_url): 
    try:
        logger.info(f"Getting video metadata ......")
        async with httpx.AsyncClient(timeout=httpx.Timeout(10.0)) as client:
            response = await client.head(video_url)
            
            if response.status_code != 200:
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"Failed to fetch video metadata: {response.status_code}",
                )
                
            # Check content type for video
            content_type = response.headers.get("content-type", "")
            if "video" not in content_type or content_type not in settings.SUPPORTED_FORMATS:
                raise HTTPException(
                    status_code=400,
                    detail=f"Unsupported video format: {content_type}. Supported formats: {', '.join(settings.SUPPORTED_FORMATS)}"
                )
                
    except httpx.ConnectTimeout as e:
        raise httpx.ConnectTimeout(f"Connection timed out while accessing the URL: {video_url}")   

    except Exception as e:
        raise e                