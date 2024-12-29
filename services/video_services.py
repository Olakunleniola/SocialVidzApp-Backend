import yt_dlp
from io import BytesIO

async def get_video_info(url):
    ydl_opts = {'quiet': True}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        return {
            'title': info.get('title', 'Unknown'),
            'url': info.get('url'),
            'platform': info.get('extractor', 'Unknown'),
        }
    
async def fetch_video_stream(url):
    ydl_opts = {
        "format": "best",
        "outtmpl": "-",
    }
    buffer = BytesIO()
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        buffer.write(ydl.urlopen(info["url"]).read())
        buffer.seek(0)
        filename = f"{info.get('title', 'video')}.mp4"
    return buffer, filename