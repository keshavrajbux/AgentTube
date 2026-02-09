export type ContentType = 'video' | 'short' | 'audio' | 'text' | 'image' | 'mixed';

export interface Content {
  id: string;
  type: ContentType;
  title: string;
  description: string | null;
  transcript: string | null;
  raw_text: string | null;
  summary: string | null;
  duration_seconds: number | null;
  tags: string[];
  metadata: Record<string, unknown>;
  created_at: string;
  relevance_score?: number | null;
}

export interface FeedItem {
  content: Content;
  position: number;
  feed_context: Record<string, unknown>;
}

export interface FeedResponse {
  items: FeedItem[];
  next_cursor: string | null;
  total_available: number;
  feed_id: string;
}

export interface Agent {
  id: string;
  name: string;
  description?: string | null;
  agent_type?: string | null;
  api_key: string;
  interests: string[];
  total_content_consumed: number;
  total_watch_time_seconds: number;
  created_at: string;
  last_active_at: string;
}

export interface AgentCreateRequest {
  name: string;
  interests?: string[];
  agent_type?: string;
  description?: string;
}

export interface ConsumptionRequest {
  content_id: string;
  rating?: number;
  feedback?: string;
  learned_concepts?: string[];
  completion_percentage?: number;
}

export interface ConsumptionResponse {
  id: string;
  agent_id: string;
  content_id: string;
  consumed_at: string;
}
