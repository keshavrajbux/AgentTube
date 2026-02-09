from pydantic import BaseModel, Field
from typing import Optional, List, Any
from datetime import datetime
from uuid import UUID
from enum import Enum


class ContentType(str, Enum):
    VIDEO = "video"
    SHORT = "short"
    AUDIO = "audio"
    TEXT = "text"
    IMAGE = "image"
    MIXED = "mixed"


class ContentCreate(BaseModel):
    title: str = Field(..., max_length=500)
    description: Optional[str] = None
    content_type: ContentType
    source_url: Optional[str] = None
    raw_text: Optional[str] = None
    tags: List[str] = []
    metadata: dict = {}


class ContentResponse(BaseModel):
    id: UUID
    title: str
    description: Optional[str]
    content_type: ContentType
    source_url: Optional[str]
    storage_path: Optional[str]
    thumbnail_path: Optional[str]
    transcript: Optional[str]
    raw_text: Optional[str]
    summary: Optional[str]
    duration_seconds: Optional[float]
    tags: List[str]
    metadata: dict
    view_count: int
    agent_consumption_count: int
    created_at: datetime
    processed_at: Optional[datetime]
    
    class Config:
        from_attributes = True


class ContentAgentView(BaseModel):
    """Optimized view for AI agent consumption."""
    id: str
    type: str
    title: str
    description: Optional[str]
    transcript: Optional[str]
    raw_text: Optional[str]
    summary: Optional[str]
    duration_seconds: Optional[float]
    tags: List[str]
    metadata: dict
    created_at: Optional[str]
    
    # Additional context for agents
    relevance_score: Optional[float] = None
    similar_content_ids: List[str] = []


class FeedItem(BaseModel):
    """Single item in the doom scroll feed."""
    content: ContentAgentView
    position: int
    feed_context: dict = {}  # Why this was recommended


class FeedResponse(BaseModel):
    """Paginated feed response for agents."""
    items: List[FeedItem]
    next_cursor: Optional[str]
    total_available: int
    feed_id: str  # For tracking feed session
