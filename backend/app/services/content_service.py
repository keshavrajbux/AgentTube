from typing import List, Optional
from uuid import UUID
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, func
from sqlalchemy.orm import selectinload
from pgvector.sqlalchemy import Vector

from app.models.content import Content, ContentType
from app.schemas.content import ContentCreate, ContentAgentView
from app.services.embedding_service import embedding_service


class ContentService:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create(self, content_data: ContentCreate) -> Content:
        """Create new content and generate embeddings."""
        content = Content(
            title=content_data.title,
            description=content_data.description,
            content_type=ContentType(content_data.content_type.value),
            source_url=content_data.source_url,
            raw_text=content_data.raw_text,
            tags=content_data.tags,
            extra_data=content_data.metadata,
        )
        
        # Generate embedding from available text
        text_for_embedding = self._get_text_for_embedding(content_data)
        if text_for_embedding:
            embedding = await embedding_service.generate_embedding(text_for_embedding)
            if embedding:
                content.embedding = embedding
        
        self.db.add(content)
        await self.db.commit()
        await self.db.refresh(content)
        return content
    
    def _get_text_for_embedding(self, content: ContentCreate) -> str:
        """Extract text for embedding generation."""
        parts = [content.title]
        if content.description:
            parts.append(content.description)
        if content.raw_text:
            parts.append(content.raw_text)
        if content.tags:
            parts.append(" ".join(content.tags))
        return " ".join(parts)
    
    async def get_by_id(self, content_id: UUID) -> Optional[Content]:
        """Get content by ID."""
        result = await self.db.execute(
            select(Content).where(Content.id == content_id)
        )
        return result.scalar_one_or_none()
    
    async def get_all(
        self, 
        skip: int = 0, 
        limit: int = 50,
        content_type: Optional[ContentType] = None
    ) -> List[Content]:
        """Get all content with pagination."""
        query = select(Content)
        if content_type:
            query = query.where(Content.content_type == content_type)
        query = query.order_by(Content.created_at.desc()).offset(skip).limit(limit)
        result = await self.db.execute(query)
        return list(result.scalars().all())
    
    async def search_semantic(
        self, 
        query: str, 
        limit: int = 20,
        content_type: Optional[ContentType] = None
    ) -> List[tuple[Content, float]]:
        """Search content using semantic similarity."""
        query_embedding = await embedding_service.generate_embedding(query)
        if not query_embedding:
            return []
        
        # Use pgvector's cosine distance
        stmt = select(
            Content,
            Content.embedding.cosine_distance(query_embedding).label("distance")
        ).where(
            Content.embedding.isnot(None)
        )
        
        if content_type:
            stmt = stmt.where(Content.content_type == content_type)
        
        stmt = stmt.order_by("distance").limit(limit)
        result = await self.db.execute(stmt)
        
        # Convert distance to similarity score
        return [(row[0], 1 - row[1]) for row in result.all()]
    
    async def search_by_tags(self, tags: List[str], limit: int = 20) -> List[Content]:
        """Search content by tags."""
        query = select(Content).where(
            Content.tags.overlap(tags)
        ).order_by(Content.created_at.desc()).limit(limit)
        result = await self.db.execute(query)
        return list(result.scalars().all())
    
    async def update_content(
        self, 
        content_id: UUID, 
        **kwargs
    ) -> Optional[Content]:
        """Update content fields."""
        content = await self.get_by_id(content_id)
        if not content:
            return None
        
        for key, value in kwargs.items():
            if hasattr(content, key):
                setattr(content, key, value)
        
        content.updated_at = datetime.utcnow()
        await self.db.commit()
        await self.db.refresh(content)
        return content
    
    async def increment_view(self, content_id: UUID) -> None:
        """Increment view count."""
        await self.db.execute(
            update(Content)
            .where(Content.id == content_id)
            .values(view_count=Content.view_count + 1)
        )
        await self.db.commit()
    
    async def increment_consumption(self, content_id: UUID) -> None:
        """Increment agent consumption count."""
        await self.db.execute(
            update(Content)
            .where(Content.id == content_id)
            .values(agent_consumption_count=Content.agent_consumption_count + 1)
        )
        await self.db.commit()
    
    async def get_total_count(self) -> int:
        """Get total content count."""
        result = await self.db.execute(select(func.count(Content.id)))
        return result.scalar() or 0
    
    def to_agent_view(self, content: Content, relevance_score: float = None) -> ContentAgentView:
        """Convert content to agent-friendly view."""
        return ContentAgentView(
            id=str(content.id),
            type=content.content_type.value,
            title=content.title,
            description=content.description,
            transcript=content.transcript,
            raw_text=content.raw_text,
            summary=content.summary,
            duration_seconds=content.duration_seconds,
            tags=content.tags or [],
            metadata=content.extra_data or {},
            created_at=content.created_at.isoformat() if content.created_at else None,
            relevance_score=relevance_score,
        )
