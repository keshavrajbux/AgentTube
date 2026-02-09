from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from uuid import UUID


class AgentCreate(BaseModel):
    name: str = Field(..., max_length=200)
    description: Optional[str] = None
    agent_type: Optional[str] = None  # claude, gpt-4, custom, etc.
    interests: List[str] = []
    metadata: dict = {}


class AgentResponse(BaseModel):
    id: UUID
    name: str
    description: Optional[str]
    agent_type: Optional[str]
    api_key: str
    interests: List[str]
    total_content_consumed: int
    total_watch_time_seconds: float
    created_at: datetime
    last_active_at: datetime
    
    class Config:
        from_attributes = True


class ConsumptionCreate(BaseModel):
    content_id: UUID
    watch_duration_seconds: Optional[float] = None
    completion_percentage: float = Field(default=100, ge=0, le=100)
    rating: Optional[int] = Field(default=None, ge=1, le=5)
    feedback: Optional[str] = None
    learned_concepts: List[str] = []


class ConsumptionResponse(BaseModel):
    id: UUID
    agent_id: UUID
    content_id: UUID
    consumed_at: datetime
    watch_duration_seconds: Optional[float]
    completion_percentage: float
    rating: Optional[int]
    feedback: Optional[str]
    learned_concepts: List[str]
    
    class Config:
        from_attributes = True
