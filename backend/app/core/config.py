from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # App
    app_name: str = "AgentTube"
    debug: bool = True
    api_prefix: str = "/api/v1"
    
    # Database
    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/agenttube"
    
    # Redis
    redis_url: str = "redis://localhost:6379"
    
    # OpenAI (for embeddings)
    openai_api_key: str = ""
    embedding_model: str = "text-embedding-3-small"
    embedding_dimensions: int = 1536
    
    # Storage
    storage_type: str = "local"  # local or s3
    local_storage_path: str = "./storage"
    s3_bucket: str = ""
    s3_region: str = "us-east-1"
    
    # Content Processing
    max_upload_size_mb: int = 500
    
    class Config:
        env_file = ".env"


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
