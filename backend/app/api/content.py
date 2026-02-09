from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.content import ContentCreate, ContentResponse, ContentAgentView
from app.services.content_service import ContentService
from app.services.feed_service import FeedService
from app.models.agent import Agent
from app.api.deps import get_current_agent

router = APIRouter()


@router.post("/", response_model=ContentResponse)
async def create_content(
    content_data: ContentCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Create new content.
    
    Content can be video, short (reels), audio, text, image, or mixed.
    Embeddings are automatically generated for semantic search.
    """
    service = ContentService(db)
    content = await service.create(content_data)
    return content


@router.get("/", response_model=List[ContentResponse])
async def list_content(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    content_type: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    """List all content with pagination."""
    service = ContentService(db)
    from app.models.content import ContentType
    ct = ContentType(content_type) if content_type else None
    contents = await service.get_all(skip=skip, limit=limit, content_type=ct)
    return contents


@router.get("/{content_id}", response_model=ContentAgentView)
async def get_content(
    content_id: UUID,
    db: AsyncSession = Depends(get_db),
    agent: Optional[Agent] = Depends(get_current_agent)
):
    """
    Get content by ID in agent-friendly format.
    
    Returns all content data optimized for AI consumption including:
    - Full transcript
    - Raw text
    - AI-generated summary
    - Tags and metadata
    """
    service = ContentService(db)
    content = await service.get_by_id(content_id)
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")
    
    # Track view
    await service.increment_view(content_id)
    
    return service.to_agent_view(content)


@router.get("/{content_id}/related", response_model=List[ContentAgentView])
async def get_related_content(
    content_id: UUID,
    limit: int = Query(10, ge=1, le=50),
    db: AsyncSession = Depends(get_db)
):
    """Get semantically similar content."""
    feed_service = FeedService(db)
    related = await feed_service.get_related_content(content_id, limit=limit)
    return related


@router.get("/search/semantic")
async def semantic_search(
    q: str = Query(..., min_length=1, description="Search query"),
    limit: int = Query(20, ge=1, le=100),
    content_type: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    """
    Semantic search for content.
    
    Uses vector similarity to find content matching the query meaning,
    not just keywords.
    """
    service = ContentService(db)
    from app.models.content import ContentType
    ct = ContentType(content_type) if content_type else None
    
    results = await service.search_semantic(q, limit=limit, content_type=ct)
    
    return [
        {
            "content": service.to_agent_view(content, relevance_score=score),
            "relevance_score": score
        }
        for content, score in results
    ]


@router.get("/search/tags")
async def search_by_tags(
    tags: str = Query(..., description="Comma-separated tags"),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):
    """Search content by tags."""
    service = ContentService(db)
    tag_list = [t.strip() for t in tags.split(",") if t.strip()]
    
    if not tag_list:
        raise HTTPException(status_code=400, detail="At least one tag required")
    
    contents = await service.search_by_tags(tag_list, limit=limit)
    return [service.to_agent_view(c) for c in contents]
