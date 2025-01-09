import yt_dlp
from yt_dlp.utils import DownloadError, ExtractorError
from io import BytesIO
import httpx
from fastapi import HTTPException

async def get_video_size(url: str):
    """ Fetch video size from URL (HTTP HEAD request) """
    async with httpx.AsyncClient() as client:
        response = await client.head(url)
        return int(response.headers.get('Content-Length', 0))

async def get_video_info(url):
    try:
        ydl_opts = {'quiet': True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            url = info.get("url")
            content_length = await get_video_size(url)
            if not content_length:
                raise HTTPException(status_code=400, detail=" Invalid Url.. Copy the URL again and try again ")

            return {
                'title': info.get('title', 'Unknown'),
                'url': url,
                'platform': info.get('extractor', 'Unknown'),
                'duration': info.get('duration', 'Unknown'),
                'uploader': info.get('uploader', 'Unknown'),
                'size': int(content_length) if content_length else 'Unknown'
            }
    except DownloadError as e:
        raise DownloadError("The platform may not be supported or the URL may be invalid. Please re-check the URL and try again.")
    except ExtractorError as e:
        raise ExtractorError(f"Failed to extract video information. Check the URL and try again:")

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
    headers = {
        "Connection": "keep-alive",
        "Accept-Encoding": "gzip, deflate, br",
        "User-Agent": "PostmanRuntime/7.43.0",
        "Cache-Control": "no-cache",
    }
    async with httpx.AsyncClient(timeout=httpx.Timeout(60.0)) as client:
        # Stream the response from the external server
        async with client.stream("GET", url, headers=headers) as response:
            if response.status_code != 200:
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"Failed to fetch video: {response.status_code}",
                )
            
            # Ensure the response is video
            if "video" not in response.headers.get("content-type", ""):
                raise HTTPException(status_code=400, detail="URL does not point to a video file.")
            
            # Yield data chunks one by one as they arrive
            async for chunk in response.aiter_bytes():
                yield chunk  # Yield each chunk of video data as it arrives
