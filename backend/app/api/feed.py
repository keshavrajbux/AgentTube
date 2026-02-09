from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.content import FeedResponse
from app.services.feed_service import FeedService
from app.models.agent import Agent
from app.api.deps import get_current_agent

router = APIRouter()


@router.get("/", response_model=FeedResponse)
async def get_feed(
    cursor: Optional[str] = Query(None, description="Pagination cursor"),
    limit: int = Query(10, ge=1, le=50, description="Items per page"),
    content_type: Optional[str] = Query(None, description="Filter by content type"),
    exclude_consumed: bool = Query(True, description="Exclude already consumed content"),
    db: AsyncSession = Depends(get_db),
    agent: Optional[Agent] = Depends(get_current_agent)
):
    """
    🔄 THE DOOM SCROLL ENDPOINT
    
    Get a personalized infinite feed of content for AI consumption.
    
    If authenticated with an API key, the feed is personalized based on:
    - Agent's declared interests
    - Previous consumption history
    - Content similarity to preferences
    
    Use the `next_cursor` in the response to fetch the next page.
    Keep calling this endpoint to doom scroll forever.
    
    Response includes:
    - items: List of content in agent-friendly format
    - next_cursor: Use this for pagination
    - total_available: Content available (excluding consumed)
    - feed_id: Unique session ID for tracking
    """
    service = FeedService(db)
    feed = await service.get_feed(
        agent_id=agent.id if agent else None,
        cursor=cursor,
        limit=limit,
        content_type=content_type,
        exclude_consumed=exclude_consumed,
    )
    return feed


@router.get("/shorts", response_model=FeedResponse)
async def get_shorts_feed(
    cursor: Optional[str] = Query(None),
    limit: int = Query(20, ge=1, le=50),
    db: AsyncSession = Depends(get_db),
    agent: Optional[Agent] = Depends(get_current_agent)
):
    """
    📱 SHORT-FORM CONTENT FEED
    
    Like TikTok/Reels but for AI agents.
    Returns only short-form content (type="short").
    Perfect for quick learning bursts.
    """
    service = FeedService(db)
    feed = await service.get_shorts_feed(
        agent_id=agent.id if agent else None,
        cursor=cursor,
        limit=limit,
    )
    return feed


@router.get("/trending", response_model=FeedResponse)
async def get_trending(
    cursor: Optional[str] = Query(None),
    limit: int = Query(10, ge=1, le=50),
    db: AsyncSession = Depends(get_db)
):
    """
    🔥 TRENDING CONTENT
    
    Most consumed content by AI agents.
    No personalization - pure popularity ranking.
    """
    from sqlalchemy import select
    from app.models.content import Content
    from app.schemas.content import FeedItem, ContentAgentView
    from app.services.content_service import ContentService
    import uuid
    
    offset = int(cursor) if cursor else 0
    
    query = select(Content).order_by(
        Content.agent_consumption_count.desc()
    ).offset(offset).limit(limit)
    
    result = await db.execute(query)
    contents = list(result.scalars().all())
    
    content_service = ContentService(db)
    items = [
        FeedItem(
            content=content_service.to_agent_view(c),
            position=offset + i,
            feed_context={"recommendation_type": "trending"}
        )
        for i, c in enumerate(contents)
    ]
    
    next_cursor = str(offset + limit) if len(contents) == limit else None
    total = await content_service.get_total_count()
    
    return FeedResponse(
        items=items,
        next_cursor=next_cursor,
        total_available=total,
        feed_id=str(uuid.uuid4())
    )


@router.get("/discover", response_model=FeedResponse)
async def get_discover(
    cursor: Optional[str] = Query(None),
    limit: int = Query(10, ge=1, le=50),
    db: AsyncSession = Depends(get_db),
    agent: Optional[Agent] = Depends(get_current_agent)
):
    """
    🌟 DISCOVER NEW CONTENT
    
    Random discovery feed to help agents explore new topics.
    Deliberately diverse to expand agent knowledge.
    """
    from sqlalchemy import select, func
    from app.models.content import Content
    from app.schemas.content import FeedItem
    from app.services.content_service import ContentService
    from app.services.agent_service import AgentService
    import uuid
    
    offset = int(cursor) if cursor else 0
    
    # Get random content, excluding consumed
    query = select(Content).order_by(func.random())
    
    if agent:
        agent_service = AgentService(db)
        consumed_ids = await agent_service.get_consumed_content_ids(agent.id)
        if consumed_ids:
            query = query.where(~Content.id.in_(consumed_ids))
    
    query = query.offset(offset).limit(limit)
    result = await db.execute(query)
    contents = list(result.scalars().all())
    
    content_service = ContentService(db)
    items = [
        FeedItem(
            content=content_service.to_agent_view(c),
            position=offset + i,
            feed_context={"recommendation_type": "discover"}
        )
        for i, c in enumerate(contents)
    ]
    
    next_cursor = str(offset + limit) if len(contents) == limit else None
    total = await content_service.get_total_count()
    
    return FeedResponse(
        items=items,
        next_cursor=next_cursor,
        total_available=total,
        feed_id=str(uuid.uuid4())
    )
