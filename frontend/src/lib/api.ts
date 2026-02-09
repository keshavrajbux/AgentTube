import type { Agent, AgentCreateRequest, Content, FeedResponse, ConsumptionRequest, ConsumptionResponse } from './types';

const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';
const API_KEY_STORAGE = 'agenttube_api_key';

export function getStoredApiKey(): string | null {
  if (typeof window === 'undefined') return null;
  return localStorage.getItem(API_KEY_STORAGE);
}

export function setStoredApiKey(key: string): void {
  if (typeof window !== 'undefined') {
    localStorage.setItem(API_KEY_STORAGE, key);
  }
}

export function clearStoredApiKey(): void {
  if (typeof window !== 'undefined') {
    localStorage.removeItem(API_KEY_STORAGE);
  }
}

function getHeaders(apiKey?: string | null): HeadersInit {
  const headers: HeadersInit = { 'Content-Type': 'application/json' };
  const key = apiKey ?? getStoredApiKey();
  if (key) headers['X-API-Key'] = key;
  return headers;
}

async function request<T>(endpoint: string, options: RequestInit = {}, apiKey?: string | null): Promise<T> {
  const res = await fetch(API_BASE + endpoint, {
    ...options,
    headers: { ...getHeaders(apiKey), ...options.headers },
  });
  if (!res.ok) {
    const error = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error(error.detail || 'API Error');
  }
  return res.json();
}

export const api = {
  getFeed: (cursor?: string, limit = 10) => {
    const params = new URLSearchParams({ limit: String(limit) });
    if (cursor) params.set('cursor', cursor);
    return request<FeedResponse>('/feed/?' + params.toString());
  },

  getShorts: (cursor?: string, limit = 20) => {
    const params = new URLSearchParams({ limit: String(limit) });
    if (cursor) params.set('cursor', cursor);
    return request<FeedResponse>('/feed/shorts?' + params.toString());
  },

  getTrending: (limit = 10) => request<FeedResponse>('/feed/trending?limit=' + limit),
  getDiscover: (limit = 10) => request<FeedResponse>('/feed/discover?limit=' + limit),
  getContent: (id: string) => request<Content>('/content/' + id),

  searchContent: (query: string, limit = 20) => {
    const encoded = encodeURIComponent(query);
    return request<{ content: Content; relevance_score: number }[]>(
      '/content/search/semantic?q=' + encoded + '&limit=' + limit
    );
  },

  registerAgent: async (data: AgentCreateRequest): Promise<Agent> => {
    const agent = await request<Agent>('/agents/register', {
      method: 'POST',
      body: JSON.stringify(data),
    });
    setStoredApiKey(agent.api_key);
    return agent;
  },

  getMe: (apiKey?: string) => request<Agent>('/agents/me', {}, apiKey),

  consume: (data: ConsumptionRequest) =>
    request<ConsumptionResponse>('/agents/consume', {
      method: 'POST',
      body: JSON.stringify(data),
    }),

  getHistory: (limit = 50) => request<ConsumptionResponse[]>('/agents/history?limit=' + limit),
};
