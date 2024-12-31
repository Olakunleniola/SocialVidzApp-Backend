from fastapi import FastAPI, HTTPException, Query
from pydantic  import BaseModel, HttpUrl, Field
from fastapi.responses import StreamingResponse
from datetime import datetime
from services.video_services import get_video_info, stream_response
from utils.validation import validate_platform, validate_url
from fastapi.middleware.cors import CORSMiddleware
import httpx

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)


class VideoRequest(BaseModel):
    url: str
    platform: str = Field(..., description="Platform, e.g., 'youtube'")
    date: datetime = Field(default_factory=datetime.now)


@app.get("/")
def home():
    return {"message": "Welcome to Social Vidz API"}

@app.get("/social_vidz/api/get_info")
async def get_info_endpoint(url: str = Query(...)):
    try:
        validate_url(url)
        video_info = await get_video_info(url)
        return {'status': "sucess", "data": video_info}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e) )
    except Exception as e:
         raise HTTPException(status_code=500, detail=str(e))
      
 
@app.post("/social_vidz/api/download")
async def download_video_endpoint(request:VideoRequest):
    try:
        url = request.url
        validate_platform(request.platform)
        if not url:
            raise HTTPException(status_code=400, detail="URL is required.")
        
        # Use StreamingResponse with the async generator that yields data
        headers = {
            "Content-Disposition": "attachment; filename=video.mp4",
            "Content-Type": "video/mp4",
        }
        return StreamingResponse(stream_response(url), headers=headers)

    except httpx.TimeoutException:
        raise HTTPException(status_code=408, detail="Request timed out.")
    except httpx.StreamClosed:
        raise HTTPException(status_code=500, detail="The video stream was unexpectedly closed.")
    except httpx.RequestError as e:
        raise HTTPException(status_code=500, detail=f"HTTP request error: {str(e)}")
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal server error.")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

