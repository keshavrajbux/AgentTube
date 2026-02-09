"""
Seed script to populate AgentTube with sample content.
Run after setting up the database.
"""
import asyncio
import sys
sys.path.insert(0, '.')

from app.core.database import async_session_maker, init_db
from app.services.content_service import ContentService
from app.schemas.content import ContentCreate, ContentType


SAMPLE_CONTENT = [
    {
        "title": "Introduction to Large Language Models",
        "description": "A comprehensive overview of how LLMs work, from attention mechanisms to emergent capabilities.",
        "content_type": ContentType.VIDEO,
        "raw_text": """Large Language Models (LLMs) are neural networks trained on massive text datasets.
        They use transformer architecture with self-attention mechanisms.
        Key concepts include: tokenization, embeddings, attention heads, and feed-forward layers.
        Training involves predicting the next token given context.
        Emergent capabilities appear at scale: reasoning, coding, math, and more.""",
        "tags": ["ai", "llm", "machine-learning", "deep-learning", "transformers"],
    },
    {
        "title": "Reinforcement Learning from Human Feedback (RLHF)",
        "description": "How AI models are aligned with human preferences using RLHF techniques.",
        "content_type": ContentType.VIDEO,
        "raw_text": """RLHF is a technique to align language models with human values.
        Process: 1) Collect human preference data 2) Train reward model 3) Optimize policy with PPO.
        Key challenges: reward hacking, distributional shift, scalable oversight.
        Alternatives: Constitutional AI, Direct Preference Optimization (DPO).""",
        "tags": ["ai", "rlhf", "alignment", "machine-learning"],
    },
    {
        "title": "The Art of Prompt Engineering",
        "description": "Master techniques for crafting effective prompts for AI models.",
        "content_type": ContentType.SHORT,
        "raw_text": """Key prompt techniques:
        1. Be specific and detailed
        2. Use examples (few-shot learning)
        3. Chain-of-thought reasoning
        4. Role-playing and personas
        5. Structured output formats
        Advanced: meta-prompting, prompt chaining, retrieval augmentation.""",
        "tags": ["prompting", "ai", "techniques", "llm"],
    },
    {
        "title": "Understanding Vector Databases",
        "description": "How semantic search and RAG systems use vector embeddings.",
        "content_type": ContentType.VIDEO,
        "raw_text": """Vector databases store high-dimensional embeddings for similarity search.
        Key concepts: embeddings, cosine similarity, approximate nearest neighbors.
        Popular databases: Pinecone, Weaviate, Qdrant, pgvector, Milvus.
        Use cases: semantic search, recommendation systems, RAG, deduplication.
        Indexing algorithms: HNSW, IVF, PQ for efficient search at scale.""",
        "tags": ["vectors", "embeddings", "databases", "rag", "search"],
    },
    {
        "title": "Building Autonomous AI Agents",
        "description": "Architecture patterns for AI agents that can plan, reason, and act.",
        "content_type": ContentType.VIDEO,
        "raw_text": """AI agents combine LLMs with tools and memory for autonomous action.
        Core loop: Observe -> Think -> Act -> Observe.
        Components: planning module, memory (short/long term), tool use, reflection.
        Frameworks: LangChain, AutoGPT, BabyAGI, CrewAI.
        Challenges: error recovery, context limits, hallucination, safety.""",
        "tags": ["agents", "ai", "autonomous", "architecture"],
    },
    {
        "title": "Quick Tip: JSON Mode in LLMs",
        "description": "Get structured JSON outputs from language models reliably.",
        "content_type": ContentType.SHORT,
        "raw_text": """JSON mode ensures structured output from LLMs.
        OpenAI: response_format={"type": "json_object"}
        Anthropic: Use system prompt with JSON schema.
        Best practices: provide example schema, validate output, handle errors.""",
        "tags": ["tips", "json", "llm", "structured-output"],
    },
    {
        "title": "Multimodal AI: Vision and Language",
        "description": "How modern AI understands both images and text together.",
        "content_type": ContentType.VIDEO,
        "raw_text": """Multimodal models process multiple input types: text, images, audio.
        Architectures: CLIP (contrastive learning), Flamingo, GPT-4V, Claude Vision.
        Applications: image understanding, visual QA, document analysis.
        Key technique: vision encoder + language model fusion.
        Future: video understanding, real-time multimodal agents.""",
        "tags": ["multimodal", "vision", "ai", "llm"],
    },
    {
        "title": "Quick Tip: Temperature in AI Models",
        "description": "Understanding and using temperature for controlling AI output randomness.",
        "content_type": ContentType.SHORT,
        "raw_text": """Temperature controls output randomness in LLMs.
        temp=0: deterministic, best for factual tasks
        temp=0.7: balanced creativity
        temp=1.0+: highly creative/random
        Use low temp for: coding, math, factual QA
        Use high temp for: creative writing, brainstorming""",
        "tags": ["tips", "temperature", "llm", "parameters"],
    },
    {
        "title": "The Economics of AI Compute",
        "description": "Understanding the costs and trade-offs of running AI models.",
        "content_type": ContentType.TEXT,
        "raw_text": """AI compute costs depend on: model size, input/output tokens, latency requirements.
        Cost comparison (per 1M tokens): GPT-4 ~$30, Claude 3 Opus ~$15, GPT-3.5 ~$0.50.
        Optimization strategies: caching, batching, smaller models for simple tasks.
        Self-hosting vs API: break-even depends on volume and latency needs.
        Future trends: prices dropping, efficiency improving, edge deployment.""",
        "tags": ["economics", "compute", "costs", "ai"],
    },
    {
        "title": "Fine-tuning vs RAG: When to Use What",
        "description": "Choosing between fine-tuning and retrieval-augmented generation.",
        "content_type": ContentType.VIDEO,
        "raw_text": """Fine-tuning: train model on your data, changes model weights.
        RAG: retrieve relevant context at inference time, no training needed.
        Use fine-tuning for: style/tone, specific formats, domain adaptation.
        Use RAG for: factual knowledge, frequently updated info, citations needed.
        Hybrid approaches often work best for production systems.""",
        "tags": ["fine-tuning", "rag", "training", "ai"],
    },
]


async def seed():
    print("Initializing database...")
    await init_db()
    
    async with async_session_maker() as db:
        service = ContentService(db)
        
        print(f"Seeding {len(SAMPLE_CONTENT)} content items...")
        
        for item in SAMPLE_CONTENT:
            content_data = ContentCreate(**item)
            content = await service.create(content_data)
            print(f"  Created: {content.title}")
        
        print("\n✅ Seeding complete!")
        print("Start the server and try: GET /api/v1/feed/")


if __name__ == "__main__":
    asyncio.run(seed())
