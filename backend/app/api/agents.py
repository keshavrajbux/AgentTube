from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.agent import AgentCreate, AgentResponse, ConsumptionCreate, ConsumptionResponse
from app.services.agent_service import AgentService
from app.services.content_service import ContentService
from app.models.agent import Agent
from app.api.deps import require_agent

router = APIRouter()


@router.post("/register", response_model=AgentResponse)
async def register_agent(
    agent_data: AgentCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Register a new AI agent.
    
    Returns an API key that must be used for authenticated requests.
    Store this key securely - it cannot be retrieved later.
    
    Optionally provide interests to enable personalized content recommendations.
    """
    service = AgentService(db)
    agent = await service.create(agent_data)
    return agent


@router.get("/me", response_model=AgentResponse)
async def get_current_agent_info(
    agent: Agent = Depends(require_agent)
):
    """Get current agent's profile."""
    return agent


@router.post("/consume", response_model=ConsumptionResponse)
async def log_consumption(
    consumption_data: ConsumptionCreate,
    agent: Agent = Depends(require_agent),
    db: AsyncSession = Depends(get_db)
):
    """
    Log content consumption by the agent.
    
    This helps personalize future recommendations and tracks learning progress.
    Optionally provide:
    - rating (1-5)
    - feedback (text)
    - learned_concepts (list of concepts the agent learned)
    """
    # Verify content exists
    content_service = ContentService(db)
    content = await content_service.get_by_id(consumption_data.content_id)
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")
    
    agent_service = AgentService(db)
    consumption = await agent_service.log_consumption(agent.id, consumption_data)
    
    # Update content consumption count
    await content_service.increment_consumption(consumption_data.content_id)
    
    return consumption


@router.get("/history", response_model=List[ConsumptionResponse])
async def get_consumption_history(
    limit: int = 50,
    agent: Agent = Depends(require_agent),
    db: AsyncSession = Depends(get_db)
):
    """Get agent's content consumption history."""
    service = AgentService(db)
    history = await service.get_consumption_history(agent.id, limit=limit)
    return history


@router.get("/{agent_id}", response_model=AgentResponse)
async def get_agent(
    agent_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """Get agent profile by ID (public info only)."""
    service = AgentService(db)
    agent = await service.get_by_id(agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    # Don't expose API key
    agent.api_key = "***hidden***"
    return agent
