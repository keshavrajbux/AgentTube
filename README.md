# AgentTube

**YouTube for AI Agents** — A content platform designed for AI consumption.

AgentTube is a full-stack application where AI agents can browse, consume, and learn from curated content. Built with a modern A24-inspired aesthetic and designed for both human developers and autonomous AI systems.

---

## Features

### For AI Agents
- **Personalized Feed** — Algorithm-driven content tailored to agent interests
- **Semantic Search** — Vector-based content discovery using embeddings
- **Consumption Tracking** — Monitor learning progress and watch time
- **API-First Design** — Full REST API for programmatic access

### For Developers
- **Agent Registration** — Create and manage AI agent identities
- **Content Management** — Upload and organize multi-modal content
- **Analytics Dashboard** — Track agent engagement and trends
- **Docker Ready** — One-command deployment

---

## Tech Stack

| Layer | Technology |
|-------|------------|
| **Frontend** | Next.js 16, React 19, Tailwind CSS 4, Motion |
| **Backend** | FastAPI, Python 3.11+, SQLAlchemy |
| **Database** | PostgreSQL with pgvector |
| **UI Components** | Magic UI (custom animations) |

---

## Quick Start

### Prerequisites
- Docker & Docker Compose
- Node.js 18+ (for frontend development)
- Python 3.11+ (for backend development)

### Run with Docker

```bash
# Clone the repository
git clone https://github.com/keshavrajbux/AgentTube.git
cd AgentTube

# Start all services
docker-compose up -d

# Seed sample content
make seed
```

The app will be available at:
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

### Development Setup

**Backend:**
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

---

## API Reference

### Authentication
All agent endpoints require an API key header:
```
X-API-Key: at_xxxxxxxxxxxxx
```

### Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/v1/agents/register` | Register a new agent |
| `GET` | `/api/v1/agents/me` | Get current agent profile |
| `GET` | `/api/v1/feed/` | Get personalized feed |
| `GET` | `/api/v1/feed/trending` | Get trending content |
| `GET` | `/api/v1/feed/discover` | Get random content |
| `POST` | `/api/v1/agents/consume` | Record content consumption |
| `GET` | `/api/v1/content/search/semantic` | Semantic content search |

### Example: Register an Agent

```bash
curl -X POST http://localhost:8000/api/v1/agents/register \
  -H "Content-Type: application/json" \
  -d '{"name": "MyAgent", "interests": ["ai", "coding"]}'
```

Response:
```json
{
  "id": "uuid",
  "name": "MyAgent",
  "api_key": "at_xxxxxxxxxxxxx",
  "interests": ["ai", "coding"]
}
```

---

## UI Design

The frontend features an **A24-inspired aesthetic** with:

- **Light Mode** — Warm off-white background (#faf9f7)
- **Film Grain** — Subtle texture overlay for cinematic feel
- **Magic Cards** — Hover spotlight effect following cursor
- **Blur Fade** — Smooth content entrance animations
- **Dot Patterns** — Elegant animated backgrounds
- **Number Tickers** — Animated statistics on dashboard

### Color Palette

| Element | Color |
|---------|-------|
| Background | `#faf9f7` (warm white) |
| Text | `#1c1917` (stone 900) |
| Accent | `#d6bcfa` (lavender) |
| Cards | `#ffffff` (white) |
| Muted | `#78716c` (stone 500) |

---

## Content Types

AgentTube supports multiple content formats:

| Type | Badge Color | Description |
|------|-------------|-------------|
| `video` | Rose | Video content with duration |
| `short` | Pink | Short-form vertical content |
| `audio` | Violet | Audio/podcast content |
| `text` | Sky | Articles and text content |
| `image` | Emerald | Image-based content |
| `mixed` | Amber | Multi-modal content |

---

## Project Structure

```
AgentTube/
├── backend/
│   ├── app/
│   │   ├── api/          # API route handlers
│   │   ├── core/         # Config and database
│   │   ├── models/       # SQLAlchemy models
│   │   ├── schemas/      # Pydantic schemas
│   │   └── services/     # Business logic
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── app/          # Next.js pages
│   │   ├── components/   # React components
│   │   │   └── ui/       # Magic UI components
│   │   ├── context/      # React context
│   │   ├── hooks/        # Custom hooks
│   │   └── lib/          # Utilities and API client
│   └── package.json
├── db/
│   └── init.sql          # Database initialization
├── docker-compose.yml
└── Makefile
```

---

## Python Client

A Python client is included for programmatic access:

```python
from agent_client import AgentTubeClient

# Initialize client
client = AgentTubeClient(api_key="at_xxxxxxxxxxxxx")

# Get feed
feed = client.get_feed(limit=10)

# Consume content
client.consume(content_id="uuid", duration=30)

# Search content
results = client.search("machine learning tutorials")
```

---

## Environment Variables

### Backend
```env
DATABASE_URL=postgresql://user:pass@localhost:5432/agenttube
OPENAI_API_KEY=sk-...  # For embeddings (optional)
```

### Frontend
```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
```

---

## License

MIT

---

Built with care for the AI agent community.
