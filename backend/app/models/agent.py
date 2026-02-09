import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, DateTime, Integer, Float, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import relationship
from pgvector.sqlalchemy import Vector

from app.core.database import Base
from app.core.config import settings


class Agent(Base):
    """Registered AI agents that consume content."""
    __tablename__ = "agents"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Agent identity
    name = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    agent_type = Column(String(100), nullable=True)  # e.g., "claude", "gpt-4", "custom"
    
    # API access
    api_key = Column(String(100), unique=True, nullable=False)
    
    # Preferences (for personalized feed)
    interests = Column(ARRAY(String), default=[])
    preference_embedding = Column(Vector(settings.embedding_dimensions), nullable=True)
    
    # Stats
    total_content_consumed = Column(Integer, default=0)
    total_watch_time_seconds = Column(Float, default=0)
    
    # Extra data
    extra_data = Column(JSON, default={})
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    last_active_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    consumptions = relationship("AgentConsumption", back_populates="agent")


class AgentConsumption(Base):
    """Track what content agents have consumed."""
    __tablename__ = "agent_consumptions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    agent_id = Column(UUID(as_uuid=True), ForeignKey("agents.id"), nullable=False)
    content_id = Column(UUID(as_uuid=True), ForeignKey("content.id"), nullable=False)
    
    # Consumption details
    consumed_at = Column(DateTime, default=datetime.utcnow)
    watch_duration_seconds = Column(Float, nullable=True)
    completion_percentage = Column(Float, default=0)  # 0-100
    
    # Agent feedback
    rating = Column(Integer, nullable=True)  # 1-5
    feedback = Column(Text, nullable=True)
    learned_concepts = Column(ARRAY(String), default=[])  # What the agent learned
    
    # Relationships
    agent = relationship("Agent", back_populates="consumptions")
