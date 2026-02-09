from typing import List, Optional
import numpy as np
from openai import AsyncOpenAI

from app.core.config import settings


class EmbeddingService:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.openai_api_key) if settings.openai_api_key else None
        self.model = settings.embedding_model
        self.dimensions = settings.embedding_dimensions
    
    async def generate_embedding(self, text: str) -> Optional[List[float]]:
        """Generate embedding for a piece of text."""
        if not self.client or not text:
            return None
        
        try:
            # Truncate text if too long (roughly 8k tokens max)
            text = text[:30000]
            
            response = await self.client.embeddings.create(
                model=self.model,
                input=text,
                dimensions=self.dimensions
            )
            return response.data[0].embedding
        except Exception as e:
            print(f"Error generating embedding: {e}")
            return None
    
    async def generate_embeddings_batch(self, texts: List[str]) -> List[Optional[List[float]]]:
        """Generate embeddings for multiple texts."""
        if not self.client:
            return [None] * len(texts)
        
        try:
            truncated = [t[:30000] for t in texts]
            response = await self.client.embeddings.create(
                model=self.model,
                input=truncated,
                dimensions=self.dimensions
            )
            return [item.embedding for item in response.data]
        except Exception as e:
            print(f"Error generating batch embeddings: {e}")
            return [None] * len(texts)
    
    def cosine_similarity(self, a: List[float], b: List[float]) -> float:
        """Calculate cosine similarity between two embeddings."""
        a_arr = np.array(a)
        b_arr = np.array(b)
        return float(np.dot(a_arr, b_arr) / (np.linalg.norm(a_arr) * np.linalg.norm(b_arr)))


embedding_service = EmbeddingService()
