from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.database import init_db
from app.api import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await init_db()
    yield
    # Shutdown


app = FastAPI(
    title="AgentTube",
    description="""
    🤖 **AgentTube** - YouTube for AI Agents
    
    A content platform designed for AI consumption. AI agents can:
    
    - **Browse** personalized content feeds
    - **Doom scroll** through infinite content
    - **Search** semantically by meaning
    - **Learn** and track their consumption
    - **Discover** new topics and concepts
    
    ## Quick Start
    
    1. Register as an agent: `POST /api/v1/agents/register`
    2. Save your API key
    3. Start doom scrolling: `GET /api/v1/feed/`
    4. Log what you consumed: `POST /api/v1/agents/consume`
    
    ## Content Types
    
    - `video` - Long-form video content
    - `short` - Reels/TikTok style short content
    - `audio` - Podcasts, audio content
    - `text` - Articles, documents
    - `image` - Visual content
    - `mixed` - Multi-modal content
    
    ## For Agents
    
    All content is returned in agent-friendly format with:
    - Full transcripts
    - AI-generated summaries
    - Semantic embeddings for similarity
    - Rich metadata
    """,
    version="1.0.0",
    lifespan=lifespan,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(api_router, prefix=settings.api_prefix)


@app.get("/")
async def root():
    return {
        "name": "AgentTube",
        "tagline": "YouTube for AI Agents 🤖",
        "version": "1.0.0",
        "docs": "/docs",
        "api": settings.api_prefix,
        "endpoints": {
            "feed": f"{settings.api_prefix}/feed/",
            "shorts": f"{settings.api_prefix}/feed/shorts",
            "trending": f"{settings.api_prefix}/feed/trending",
            "discover": f"{settings.api_prefix}/feed/discover",
            "search": f"{settings.api_prefix}/content/search/semantic",
            "register": f"{settings.api_prefix}/agents/register",
        }
    }


@app.get("/health")
async def health():
    return {"status": "healthy", "service": "agenttube"}
