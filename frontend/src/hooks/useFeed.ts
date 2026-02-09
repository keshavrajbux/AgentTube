'use client';

import { useState, useCallback, useRef, useEffect } from 'react';
import { api } from '@/lib/api';
import type { FeedItem } from '@/lib/types';

export function useFeed(autoFetch = true) {
  const [items, setItems] = useState<FeedItem[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [isLoadingMore, setIsLoadingMore] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [hasMore, setHasMore] = useState(true);
  const cursorRef = useRef<string | null>(null);

  const fetchFeed = useCallback(async (cursor?: string, isRefresh = false) => {
    if (isRefresh || !cursor) setIsLoading(true);
    else setIsLoadingMore(true);
    setError(null);

    try {
      const res = await api.getFeed(cursor, 10);
      if (isRefresh || !cursor) setItems(res.items);
      else setItems(prev => [...prev, ...res.items]);
      setHasMore(res.next_cursor !== null);
      cursorRef.current = res.next_cursor;
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Failed to load feed');
    } finally {
      setIsLoading(false);
      setIsLoadingMore(false);
    }
  }, []);

  const loadMore = useCallback(() => {
    if (!hasMore || isLoadingMore || !cursorRef.current) return;
    fetchFeed(cursorRef.current);
  }, [hasMore, isLoadingMore, fetchFeed]);

  const refresh = useCallback(() => {
    cursorRef.current = null;
    setHasMore(true);
    fetchFeed(undefined, true);
  }, [fetchFeed]);

  useEffect(() => {
    if (autoFetch) fetchFeed();
  }, [autoFetch, fetchFeed]);

  return { items, isLoading, isLoadingMore, error, hasMore, loadMore, refresh };
}
