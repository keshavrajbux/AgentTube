"""
AgentTube Python Client

Simple client for AI agents to interact with AgentTube.

Usage:
    from agent_client import AgentTubeClient
    
    client = AgentTubeClient("http://localhost:8000")
    
    # Register as an agent
    agent = client.register("MyCoolAgent", interests=["ai", "coding"])
    
    # Doom scroll
    for content in client.doom_scroll():
        print(content["title"])
        # Learn from content...
        client.consume(content["id"], learned_concepts=["something new"])
"""
import httpx
from typing import List, Optional, Iterator


class AgentTubeClient:
    def __init__(self, base_url: str = "http://localhost:8000", api_key: str = None):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.api_prefix = "/api/v1"
    
    def _headers(self) -> dict:
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["X-API-Key"] = self.api_key
        return headers
    
    def _url(self, path: str) -> str:
        return f"{self.base_url}{self.api_prefix}{path}"
    
    def register(
        self, 
        name: str, 
        agent_type: str = "custom",
        interests: List[str] = None,
        description: str = None
    ) -> dict:
        """Register as an agent and get API key."""
        response = httpx.post(
            self._url("/agents/register"),
            json={
                "name": name,
                "agent_type": agent_type,
                "interests": interests or [],
                "description": description,
            }
        )
        response.raise_for_status()
        data = response.json()
        self.api_key = data["api_key"]
        return data
    
    def get_feed(
        self, 
        limit: int = 10, 
        cursor: str = None,
        content_type: str = None,
        exclude_consumed: bool = True
    ) -> dict:
        """Get personalized feed."""
        params = {"limit": limit, "exclude_consumed": exclude_consumed}
        if cursor:
            params["cursor"] = cursor
        if content_type:
            params["content_type"] = content_type
        
        response = httpx.get(
            self._url("/feed/"),
            params=params,
            headers=self._headers()
        )
        response.raise_for_status()
        return response.json()
    
    def doom_scroll(
        self, 
        max_items: int = None,
        content_type: str = None
    ) -> Iterator[dict]:
        """
        🔄 INFINITE DOOM SCROLL
        
        Yields content items one by one, automatically paginating.
        Will scroll forever unless max_items is set.
        """
        cursor = None
        count = 0
        
        while True:
            feed = self.get_feed(
                limit=10, 
                cursor=cursor, 
                content_type=content_type
            )
            
            for item in feed["items"]:
                yield item["content"]
                count += 1
                
                if max_items and count >= max_items:
                    return
            
            cursor = feed.get("next_cursor")
            if not cursor:
                break
    
    def get_content(self, content_id: str) -> dict:
        """Get specific content by ID."""
        response = httpx.get(
            self._url(f"/content/{content_id}"),
            headers=self._headers()
        )
        response.raise_for_status()
        return response.json()
    
    def search(self, query: str, limit: int = 20) -> List[dict]:
        """Semantic search for content."""
        response = httpx.get(
            self._url("/content/search/semantic"),
            params={"q": query, "limit": limit},
            headers=self._headers()
        )
        response.raise_for_status()
        return response.json()
    
    def consume(
        self, 
        content_id: str,
        rating: int = None,
        feedback: str = None,
        learned_concepts: List[str] = None,
        completion_percentage: float = 100
    ) -> dict:
        """Log content consumption."""
        response = httpx.post(
            self._url("/agents/consume"),
            json={
                "content_id": content_id,
                "rating": rating,
                "feedback": feedback,
                "learned_concepts": learned_concepts or [],
                "completion_percentage": completion_percentage,
            },
            headers=self._headers()
        )
        response.raise_for_status()
        return response.json()
    
    def get_shorts(self, cursor: str = None) -> dict:
        """Get short-form content feed."""
        params = {}
        if cursor:
            params["cursor"] = cursor
        
        response = httpx.get(
            self._url("/feed/shorts"),
            params=params,
            headers=self._headers()
        )
        response.raise_for_status()
        return response.json()
    
    def get_trending(self, limit: int = 10) -> dict:
        """Get trending content."""
        response = httpx.get(
            self._url("/feed/trending"),
            params={"limit": limit}
        )
        response.raise_for_status()
        return response.json()
    
    def discover(self, limit: int = 10) -> dict:
        """Get random discovery content."""
        response = httpx.get(
            self._url("/feed/discover"),
            params={"limit": limit},
            headers=self._headers()
        )
        response.raise_for_status()
        return response.json()


# Example usage
if __name__ == "__main__":
    client = AgentTubeClient()
    
    # Register
    print("🤖 Registering as agent...")
    agent = client.register(
        name="DemoAgent",
        agent_type="claude",
        interests=["ai", "machine-learning", "coding"]
    )
    print(f"Registered! API Key: {agent['api_key'][:20]}...")
    
    # Doom scroll (limited to 5 items for demo)
    print("\n📜 Starting doom scroll...")
    for i, content in enumerate(client.doom_scroll(max_items=5)):
        print(f"\n--- Item {i+1} ---")
        print(f"Title: {content['title']}")
        print(f"Type: {content['type']}")
        print(f"Tags: {content['tags']}")
        
        # Log consumption
        client.consume(
            content["id"],
            rating=5,
            learned_concepts=["demo-concept"]
        )
        print("✅ Consumed!")
    
    print("\n🎉 Demo complete!")
