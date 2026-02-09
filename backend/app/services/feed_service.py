import uuid
import random
from typing import List, Optional
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, not_

from app.models.content import Content
from app.models.agent import Agent
from app.schemas.content import ContentAgentView, FeedItem, FeedResponse
from app.services.content_service import ContentService
from app.services.agent_service import AgentService


class FeedService:
    """The doom scroll engine for AI agents."""
    
    def __init__(self, db: AsyncSession):
        self.db = db
        self.content_service = ContentService(db)
        self.agent_service = AgentService(db)
    
    async def get_feed(
        self,
        agent_id: Optional[UUID] = None,
        cursor: Optional[str] = None,
        limit: int = 10,
        content_type: Optional[str] = None,
        exclude_consumed: bool = True,
    ) -> FeedResponse:
        """
        Generate personalized doom scroll feed for an agent.
        
        The algorithm:
        1. If agent has preference embedding, use semantic similarity
        2. Mix in trending content (high consumption count)
        3. Add some random discovery content
        4. Exclude already consumed content if requested
        """
        feed_id = str(uuid.uuid4())
        items: List[FeedItem] = []
        
        # Parse cursor for pagination
        offset = 0
        if cursor:
            try:
                offset = int(cursor)
            except:
                offset = 0
        
        # Get excluded content IDs
        excluded_ids = []
        if agent_id and exclude_consumed:
            excluded_ids = await self.agent_service.get_consumed_content_ids(agent_id)
        
        # Build query
        query = select(Content)
        
        if content_type:
            from app.models.content import ContentType
            query = query.where(Content.content_type == ContentType(content_type))
        
        if excluded_ids:
            query = query.where(not_(Content.id.in_(excluded_ids)))
        
        # Get personalized content if agent has preferences
        agent = None
        if agent_id:
            agent = await self.agent_service.get_by_id(agent_id)
        
        if agent and agent.preference_embedding:
            # Semantic search based on agent preferences
            query = query.where(Content.embedding.isnot(None))
            query = query.order_by(
                Content.embedding.cosine_distance(agent.preference_embedding)
            )
        else:
            # Default: mix of popular and recent
            # 70% ordered by consumption, 30% by recency
            if random.random() < 0.7:
                query = query.order_by(Content.agent_consumption_count.desc())
            else:
                query = query.order_by(Content.created_at.desc())
        
        query = query.offset(offset).limit(limit)
        result = await self.db.execute(query)
        contents = list(result.scalars().all())
        
        # Convert to feed items
        for i, content in enumerate(contents):
            agent_view = self.content_service.to_agent_view(content)
            feed_item = FeedItem(
                content=agent_view,
                position=offset + i,
                feed_context={
                    "recommendation_type": "personalized" if agent else "trending",
                    "feed_session": feed_id,
                }
            )
            items.append(feed_item)
        
        # Calculate next cursor
        next_cursor = str(offset + limit) if len(contents) == limit else None
        
        # Get total count
        total = await self.content_service.get_total_count()
        
        return FeedResponse(
            items=items,
            next_cursor=next_cursor,
            total_available=total - len(excluded_ids),
            feed_id=feed_id,
        )
    
    async def get_shorts_feed(
        self,
        agent_id: Optional[UUID] = None,
        cursor: Optional[str] = None,
        limit: int = 20,
    ) -> FeedResponse:
        """Get feed of short-form content only (like Reels/TikTok)."""
        return await self.get_feed(
            agent_id=agent_id,
            cursor=cursor,
            limit=limit,
            content_type="short",
        )
    
    async def get_related_content(
        self,
        content_id: UUID,
        limit: int = 10,
    ) -> List[ContentAgentView]:
        """Get content similar to a specific piece."""
        content = await self.content_service.get_by_id(content_id)
        if not content or not content.embedding:
            return []
        
        # Find similar content
        query = select(Content).where(
            Content.id != content_id,
            Content.embedding.isnot(None)
        ).order_by(
            Content.embedding.cosine_distance(content.embedding)
        ).limit(limit)
        
        result = await self.db.execute(query)
        similar = list(result.scalars().all())
        
        return [self.content_service.to_agent_view(c) for c in similar]
