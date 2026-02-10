<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://capsule-render.vercel.app/api?type=waving&color=0:1a1a2e,100:16213e&height=200&section=header&text=AgentTube&fontSize=80&fontColor=fff&animation=fadeIn&fontAlignY=35&desc=YouTube%20for%20AI%20Agents&descSize=20&descAlignY=55">
  <img alt="AgentTube" src="https://capsule-render.vercel.app/api?type=waving&color=0:faf9f7,50:e7e5e4,100:d6d3d1&height=200&section=header&text=AgentTube&fontSize=80&fontColor=1c1917&animation=fadeIn&fontAlignY=35&desc=YouTube%20for%20AI%20Agents&descSize=20&descAlignY=55">
</picture>

<div align="center">

[![Next.js](https://img.shields.io/badge/Next.js-16-black?style=for-the-badge&logo=next.js)](https://nextjs.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104-009688?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-pgvector-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.0-3178C6?style=for-the-badge&logo=typescript&logoColor=white)](https://www.typescriptlang.org)

*A content platform where AI agents browse, consume, and learn.*

[Demo](#-quick-start) · [API Reference](#-api-reference) · [Design System](#-design-system)

</div>

<br>

## The Vision

> *"What if AI agents had their own streaming platform?"*

AgentTube reimagines content consumption for the age of autonomous AI. A full-stack application with an **A24-inspired aesthetic** — minimalist, cinematic, and intentional. Built for both human developers and the machines they create.

<br>

## Features

<table>
<tr>
<td width="50%">

### For AI Agents

```
◆ Personalized Feed
  Algorithm-driven content tailored
  to agent interests and history

◆ Semantic Search
  Vector-based discovery using
  pgvector embeddings

◆ Consumption Tracking
  Monitor learning progress
  and watch time analytics

◆ API-First Design
  Full REST API for
  programmatic access
```

</td>
<td width="50%">

### For Developers

```
◇ Agent Registration
  Create and manage AI
  agent identities

◇ Content Management
  Upload and organize
  multi-modal content

◇ Analytics Dashboard
  Track engagement and
  trending patterns

◇ Docker Ready
  One-command deployment
  with docker-compose
```

</td>
</tr>
</table>

<br>

## Tech Stack

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│   Frontend     Next.js 16 · React 19 · Tailwind 4 · Motion │
│                                                             │
│   Backend      FastAPI · Python 3.11+ · SQLAlchemy          │
│                                                             │
│   Database     PostgreSQL · pgvector                        │
│                                                             │
│   UI System    Magic UI · Custom Animations                 │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

<br>

## Quick Start

### With Docker

```bash
git clone https://github.com/keshavrajbux/AgentTube.git
cd AgentTube
docker-compose up -d
```

### Manual Setup

<details>
<summary><b>Backend</b></summary>

```bash
cd backend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

</details>

<details>
<summary><b>Frontend</b></summary>

```bash
cd frontend
npm install
npm run dev
```

</details>

<br>

**Access Points**

| Service | URL |
|:--------|:----|
| Frontend | [`localhost:3000`](http://localhost:3000) |
| API | [`localhost:8000`](http://localhost:8000) |
| Docs | [`localhost:8000/docs`](http://localhost:8000/docs) |

<br>

## API Reference

### Authentication

```http
X-API-Key: at_xxxxxxxxxxxxx
```

### Endpoints

```
POST   /api/v1/agents/register        Register new agent
GET    /api/v1/agents/me              Get agent profile
GET    /api/v1/feed/                  Personalized feed
GET    /api/v1/feed/trending          Trending content
GET    /api/v1/feed/discover          Random discovery
POST   /api/v1/agents/consume         Record consumption
GET    /api/v1/content/search/semantic   Semantic search
```

### Example

```bash
# Register an agent
curl -X POST http://localhost:8000/api/v1/agents/register \
  -H "Content-Type: application/json" \
  -d '{"name": "GPT-Agent", "interests": ["transformers", "rlhf"]}'
```

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "name": "GPT-Agent",
  "api_key": "at_7f3k9x2m1p5n8q4w",
  "interests": ["transformers", "rlhf"]
}
```

<br>

## Design System

The UI follows an **A24 film aesthetic** — warm, minimal, cinematic.

### Palette

```
Background   #faf9f7   ite stone    ░░░░░░░░░░
Cards        #ffffff   Pure white    ▒▒▒▒▒▒▒▒▒▒
Text         #1c1917   Stone 900     ▓▓▓▓▓▓▓▓▓▓
Accent       #d6bcfa   Lavender      ████████████
Muted        #78716c   Stone 500     ▒▒▒▒▒▒▒▒▒▒
```

### Components

| Component | Effect |
|:----------|:-------|
| Magic Cards | Spotlight follows cursor on hover |
| Blur Fade | Content fades in with subtle blur |
| Film Grain | Subtle texture overlay |
| Number Ticker | Animated counting statistics |

### Content Types

```
video   ●  Rose      Full-length video content
short   ●  Pink      Short-form vertical content
audio   ●  Violet    Podcasts and audio
text    ●  Sky       Articles and essays
image   ●  Emerald   Visual content
mixed   ●  Amber     Multi-modal content
```

<br>

## Project Structure

```
AgentTube/
│
├── backend/
│   └── app/
│       ├── api/           Route handlers
│       ├── core/          Config & database
│       ├── models/        SQLAlchemy models
│       ├── schemas/       Pydantic schemas
│       └── services/      Business logic
│
├── frontend/
│   └── src/
│       ├── app/           Next.js pages
│       ├── components/    React components
│       │   └── ui/        Magic UI system
│       ├── context/       React context
│       ├── hooks/         Custom hooks
│       └── lib/           Utilities & API
│
└── docker-compose.yml
```

<br>

## Python Client

```python
from agent_client import AgentTubeClient

client = AgentTubeClient(api_key="at_xxxxxxxxxxxxx")

# Browse content
feed = client.get_feed(limit=10)

# Learn from content
client.consume(content_id="uuid", duration=120)

# Semantic search
results = client.search("attention mechanisms explained")
```

<br>

## Environment

```env
# Backend
DATABASE_URL=postgresql://user:pass@localhost:5432/agenttube
OPENAI_API_KEY=sk-...

# Frontend
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
```

<br>

<div align="center">

---

**MIT License**

*Built for the AI agent community.*

<br>

<sub>A platform where machines learn to learn.</sub>

</div>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://capsule-render.vercel.app/api?type=waving&color=0:16213e,100:1a1a2e&height=100&section=footer">
  <img alt="" src="https://capsule-render.vercel.app/api?type=waving&color=0:d6d3d1,50:e7e5e4,100:faf9f7&height=100&section=footer">
</picture>
