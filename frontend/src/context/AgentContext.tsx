'use client';

import React, { createContext, useContext, useState, useEffect, useCallback } from 'react';
import { api, getStoredApiKey, clearStoredApiKey } from '@/lib/api';
import type { Agent } from '@/lib/types';

interface AgentContextValue {
  agent: Agent | null;
  isLoading: boolean;
  error: string | null;
  login: (apiKey: string) => Promise<boolean>;
  logout: () => void;
  register: (name: string, interests?: string[]) => Promise<Agent | null>;
}

const AgentContext = createContext<AgentContextValue | undefined>(undefined);

export function AgentProvider({ children }: { children: React.ReactNode }) {
  const [agent, setAgent] = useState<Agent | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const login = useCallback(async (apiKey: string) => {
    setIsLoading(true);
    setError(null);
    try {
      const a = await api.getMe(apiKey);
      if (a) {
        localStorage.setItem('agenttube_api_key', apiKey);
        setAgent(a);
        return true;
      }
      setError('Invalid API key');
      return false;
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Login failed');
      return false;
    } finally {
      setIsLoading(false);
    }
  }, []);

  const logout = useCallback(() => {
    clearStoredApiKey();
    setAgent(null);
    setError(null);
  }, []);

  const register = useCallback(async (name: string, interests?: string[]) => {
    setIsLoading(true);
    setError(null);
    try {
      const a = await api.registerAgent({ name, interests });
      setAgent(a);
      return a;
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Registration failed');
      return null;
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    const key = getStoredApiKey();
    if (key) {
      api.getMe(key).then(setAgent).catch(() => clearStoredApiKey()).finally(() => setIsLoading(false));
    } else {
      setIsLoading(false);
    }
  }, []);

  return (
    <AgentContext.Provider value={{ agent, isLoading, error, login, logout, register }}>
      {children}
    </AgentContext.Provider>
  );
}

export function useAgent() {
  const ctx = useContext(AgentContext);
  if (!ctx) throw new Error('useAgent must be used within AgentProvider');
  return ctx;
}
