from sqlalchemy import Column, Integer, String, Float, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

# Database model base class
Base = declarative_base()

# Define VideoDownload model
class VideoDownload(Base):
    __tablename__ = "video_downloads"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    platform = Column(String, nullable=False)
    size = Column(Float, nullable=False)  # Size in MB
    url = Column(Text, nullable=False)
    date = Column(DateTime, default=datetime.utcnow)  # Auto-add timestamp
    ip_address = Column(String, nullable=False)

    def __repr__(self):
        return f"<VideoDownload(id={self.id}, title={self.title}, platform={self.platform}, size={self.size} MB)>"
