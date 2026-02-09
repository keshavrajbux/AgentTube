-- Enable pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- This script runs on first database initialization
-- Tables are created by SQLAlchemy, this is for any custom setup
