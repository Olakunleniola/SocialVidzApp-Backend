from fastapi import FastAPI, HTTPException
from app.core.middleware import setup_cors
from app.routes.video_routes import router as video_router
from app.models.video_download import VideoDownload
from app.core.error_handlers import validation_exception_handler, httpx_timeout_handler, exception_handler, value_error_handler, httpexceptions_handler
from fastapi.exceptions import RequestValidationError
import httpx
from app.core.config import settings




app = FastAPI()

# Apply middleware
setup_cors(app)

app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(httpx.ConnectTimeout, httpx_timeout_handler)
app.add_exception_handler(ValueError, value_error_handler)
app.add_exception_handler(HTTPException, httpexceptions_handler)
app.add_exception_handler(Exception, exception_handler) 

if settings.DEBUG:
    from app.models.database import engine
    @app.on_event('startup')
    async def initailize_database():
        async with engine.begin() as conn:
            await conn.run_sync(VideoDownload.metadata.create_all)

# Include routes
app.include_router(video_router, prefix="/social_vidz/api")

@app.get("/")
def home():
    return {"message": "Welcome to Social Vidz API"}

