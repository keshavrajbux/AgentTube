import secrets
from typing import List, Optional
from uuid import UUID
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update

from app.models.agent import Agent, AgentConsumption
from app.schemas.agent import AgentCreate, ConsumptionCreate
from app.services.embedding_service import embedding_service


class AgentService:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create(self, agent_data: AgentCreate) -> Agent:
        """Create new agent with API key."""
        api_key = f"at_{secrets.token_urlsafe(32)}"
        
        agent = Agent(
            name=agent_data.name,
            description=agent_data.description,
            agent_type=agent_data.agent_type,
            api_key=api_key,
            interests=agent_data.interests,
            extra_data=agent_data.metadata,
        )
        
        # Generate preference embedding from interests
        if agent_data.interests:
            interests_text = " ".join(agent_data.interests)
            embedding = await embedding_service.generate_embedding(interests_text)
            if embedding:
                agent.preference_embedding = embedding
        
        self.db.add(agent)
        await self.db.commit()
        await self.db.refresh(agent)
        return agent
    
    async def get_by_id(self, agent_id: UUID) -> Optional[Agent]:
        """Get agent by ID."""
        result = await self.db.execute(
            select(Agent).where(Agent.id == agent_id)
        )
        return result.scalar_one_or_none()
    
    async def get_by_api_key(self, api_key: str) -> Optional[Agent]:
        """Get agent by API key."""
        result = await self.db.execute(
            select(Agent).where(Agent.api_key == api_key)
        )
        return result.scalar_one_or_none()
    
    async def update_last_active(self, agent_id: UUID) -> None:
        """Update agent's last active timestamp."""
        await self.db.execute(
            update(Agent)
            .where(Agent.id == agent_id)
            .values(last_active_at=datetime.utcnow())
        )
        await self.db.commit()
    
    async def log_consumption(
        self, 
        agent_id: UUID, 
        consumption_data: ConsumptionCreate
    ) -> AgentConsumption:
        """Log content consumption by agent."""
        consumption = AgentConsumption(
            agent_id=agent_id,
            content_id=consumption_data.content_id,
            watch_duration_seconds=consumption_data.watch_duration_seconds,
            completion_percentage=consumption_data.completion_percentage,
            rating=consumption_data.rating,
            feedback=consumption_data.feedback,
            learned_concepts=consumption_data.learned_concepts,
        )
        
        self.db.add(consumption)
        
        # Update agent stats
        await self.db.execute(
            update(Agent)
            .where(Agent.id == agent_id)
            .values(
                total_content_consumed=Agent.total_content_consumed + 1,
                total_watch_time_seconds=Agent.total_watch_time_seconds + (consumption_data.watch_duration_seconds or 0),
                last_active_at=datetime.utcnow()
            )
        )
        
        await self.db.commit()
        await self.db.refresh(consumption)
        return consumption
    
    async def get_consumption_history(
        self, 
        agent_id: UUID, 
        limit: int = 50
    ) -> List[AgentConsumption]:
        """Get agent's consumption history."""
        result = await self.db.execute(
            select(AgentConsumption)
            .where(AgentConsumption.agent_id == agent_id)
            .order_by(AgentConsumption.consumed_at.desc())
            .limit(limit)
        )
        return list(result.scalars().all())
    
    async def get_consumed_content_ids(self, agent_id: UUID) -> List[UUID]:
        """Get list of content IDs already consumed by agent."""
        result = await self.db.execute(
            select(AgentConsumption.content_id)
            .where(AgentConsumption.agent_id == agent_id)
        )
        return [row[0] for row in result.all()]
