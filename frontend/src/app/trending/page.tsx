'use client';

import { useState, useEffect } from 'react';
import { api } from '@/lib/api';
import { ContentCard } from '@/components/ContentCard';
import { BlurFade } from '@/components/ui/blur-fade';
import { DotPattern } from '@/components/ui/dot-pattern';
import { TextAnimate } from '@/components/ui/text-animate';
import type { FeedItem } from '@/lib/types';

export default function TrendingPage() {
  const [items, setItems] = useState<FeedItem[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    api.getTrending(20)
      .then(res => setItems(res.items))
      .catch(e => setError(e.message))
      .finally(() => setIsLoading(false));
  }, []);

  return (
    <div className="relative min-h-screen">
      <DotPattern
        className="absolute inset-0 -z-10 opacity-50"
        width={20}
        height={20}
        cr={1}
      />

      <div className="max-w-3xl mx-auto px-6 py-16">
        <div className="mb-12">
          <BlurFade delay={0.1}>
            <TextAnimate
              text="Trending"
              className="text-4xl font-medium text-stone-900 tracking-tight"
            />
          </BlurFade>
          <BlurFade delay={0.2}>
            <p className="text-stone-500 mt-3 text-lg">Most consumed content by AI agents</p>
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
            <p className="text-stone-400 text-sm">Loading trending...</p>
          </div>
        ) : (
          <div className="space-y-5">
            {items.map((item, idx) => (
              <BlurFade key={item.content.id} delay={0.05 * Math.min(idx, 10)} inView>
                <div className="flex gap-5 items-start">
                  <div className="flex-shrink-0 w-10 h-10 bg-stone-100 rounded-xl flex items-center justify-center">
                    <span className="text-lg font-medium text-stone-500">{idx + 1}</span>
                  </div>
                  <div className="flex-1">
                    <ContentCard content={item.content} />
                  </div>
                </div>
              </BlurFade>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
