'use client';

import { useState, useEffect, useCallback } from 'react';
import { api } from '@/lib/api';
import { ContentCard } from '@/components/ContentCard';
import { BlurFade } from '@/components/ui/blur-fade';
import { DotPattern } from '@/components/ui/dot-pattern';
import { TextAnimate } from '@/components/ui/text-animate';
import type { FeedItem } from '@/lib/types';

export default function DiscoverPage() {
  const [items, setItems] = useState<FeedItem[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [shuffleKey, setShuffleKey] = useState(0);

  const loadDiscover = useCallback(() => {
    setIsLoading(true);
    setError(null);
    api.getDiscover(20)
      .then(res => {
        setItems(res.items);
        setShuffleKey(k => k + 1);
      })
      .catch(e => setError(e.message))
      .finally(() => setIsLoading(false));
  }, []);

  useEffect(() => {
    loadDiscover();
  }, [loadDiscover]);

  return (
    <div className="relative min-h-screen">
      <DotPattern
        className="absolute inset-0 -z-10 opacity-50"
        width={20}
        height={20}
        cr={1}
      />

      <div className="max-w-5xl mx-auto px-6 py-16">
        <div className="flex items-end justify-between mb-12">
          <div>
            <BlurFade delay={0.1}>
              <TextAnimate
                text="Discover"
                className="text-4xl font-medium text-stone-900 tracking-tight"
              />
            </BlurFade>
            <BlurFade delay={0.2}>
              <p className="text-stone-500 mt-3 text-lg">Random content to expand your knowledge</p>
            </BlurFade>
          </div>
          <BlurFade delay={0.3}>
            <button
              onClick={loadDiscover}
              disabled={isLoading}
              className="bg-white hover:bg-stone-50 border border-stone-200 px-5 py-2.5 rounded-full text-sm text-stone-600 hover:text-stone-900 transition-all duration-200 shadow-sm hover:shadow disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
            >
              <svg className={`w-4 h-4 ${isLoading ? 'animate-spin' : ''}`} fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
              </svg>
              Shuffle
            </button>
          </BlurFade>
        </div>

        {error && (
          <div className="bg-rose-50 border border-rose-200 text-rose-700 px-5 py-4 rounded-xl mb-8 text-sm">
            {error}
          </div>
        )}

        {isLoading ? (
          <div className="flex flex-col items-center justify-center py-32">
            <div className="spinner h-10 w-10 mb-4"></div>
            <p className="text-stone-400 text-sm">Discovering content...</p>
          </div>
        ) : (
          <div key={shuffleKey} className="grid md:grid-cols-2 lg:grid-cols-3 gap-5">
            {items.map((item, idx) => (
              <BlurFade key={item.content.id} delay={0.03 * Math.min(idx, 12)} inView>
                <ContentCard content={item.content} />
              </BlurFade>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
