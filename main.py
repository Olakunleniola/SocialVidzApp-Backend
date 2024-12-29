from fastapi import FastAPI, HTTPException, Request
from pydantic  import BaseModel, HttpUrl
from datetime import datetime


app = FastAPI()

class VideoRequest(BaseModel):
    url: HttpUrl
    platform: str
    date: datetime = datetime.now()

@app.get("/")
def home():
    return {"message": "Welcome to Social Vidz API"}

