from fastapi import APIRouter
from app.api import content, agents, feed

api_router = APIRouter()
api_router.include_router(content.router, prefix="/content", tags=["content"])
api_router.include_router(agents.router, prefix="/agents", tags=["agents"])
api_router.include_router(feed.router, prefix="/feed", tags=["feed"])
