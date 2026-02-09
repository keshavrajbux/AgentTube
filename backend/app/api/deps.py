from typing import Optional
from fastapi import Depends, HTTPException, Header
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.agent import Agent
from app.services.agent_service import AgentService


async def get_current_agent(
    x_api_key: Optional[str] = Header(None, alias="X-API-Key"),
    db: AsyncSession = Depends(get_db)
) -> Optional[Agent]:
    """Get current agent from API key (optional)."""
    if not x_api_key:
        return None
    
    agent_service = AgentService(db)
    agent = await agent_service.get_by_api_key(x_api_key)
    return agent


async def require_agent(
    agent: Optional[Agent] = Depends(get_current_agent)
) -> Agent:
    """Require valid agent API key."""
    if not agent:
        raise HTTPException(
            status_code=401,
            detail="Invalid or missing API key. Register as an agent first."
        )
    return agent
