import uuid
from datetime import datetime
from enum import Enum
from sqlalchemy import Column, String, Text, DateTime, Integer, Float, Enum as SQLEnum, JSON
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from pgvector.sqlalchemy import Vector

from app.core.database import Base
from app.core.config import settings


class ContentType(str, Enum):
    VIDEO = "video"
    SHORT = "short"  # Reels/shorts format
    AUDIO = "audio"
    TEXT = "text"
    IMAGE = "image"
    MIXED = "mixed"


class Content(Base):
    __tablename__ = "content"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Basic metadata
    title = Column(String(500), nullable=False)
    description = Column(Text, nullable=True)
    content_type = Column(SQLEnum(ContentType), nullable=False)
    
    # Source and storage
    source_url = Column(String(2000), nullable=True)  # Original URL if imported
    storage_path = Column(String(2000), nullable=True)  # Local/S3 path
    thumbnail_path = Column(String(2000), nullable=True)
    
    # AI-friendly content (what agents consume)
    transcript = Column(Text, nullable=True)  # Full transcript for video/audio
    raw_text = Column(Text, nullable=True)  # For text content
    summary = Column(Text, nullable=True)  # AI-generated summary
    
    # Embeddings for semantic search
    embedding = Column(Vector(settings.embedding_dimensions), nullable=True)
    
    # Extra data
    duration_seconds = Column(Float, nullable=True)
    tags = Column(ARRAY(String), default=[])
    extra_data = Column(JSON, default={})  # Flexible additional data
    
    # Stats
    view_count = Column(Integer, default=0)
    agent_consumption_count = Column(Integer, default=0)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    processed_at = Column(DateTime, nullable=True)  # When AI processing completed
    
    def to_agent_format(self) -> dict:
        """Return content in agent-consumable format."""
        return {
            "id": str(self.id),
            "type": self.content_type.value,
            "title": self.title,
            "description": self.description,
            "transcript": self.transcript,
            "raw_text": self.raw_text,
            "summary": self.summary,
            "duration_seconds": self.duration_seconds,
            "tags": self.tags or [],
            "metadata": self.extra_data or {},
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
