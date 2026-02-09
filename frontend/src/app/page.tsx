'use client';

import { useFeed } from '@/hooks/useFeed';
import { ContentCard } from '@/components/ContentCard';
import { useEffect, useRef } from 'react';
import { DotPattern } from '@/components/ui/dot-pattern';
import { BlurFade } from '@/components/ui/blur-fade';
import { TextAnimate } from '@/components/ui/text-animate';

export default function HomePage() {
  const { items, isLoading, isLoadingMore, error, hasMore, loadMore, refresh } = useFeed();
  const observerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        if (entries[0].isIntersecting && hasMore && !isLoadingMore) {
          loadMore();
        }
      },
      { threshold: 0.1 }
    );

    if (observerRef.current) {
      observer.observe(observerRef.current);
    }

    return () => observer.disconnect();
  }, [hasMore, isLoadingMore, loadMore]);

  return (
    <div className="relative min-h-screen">
      <DotPattern
        className="absolute inset-0 -z-10 opacity-50"
        width={20}
        height={20}
        cr={1}
      />

      <div className="max-w-3xl mx-auto px-6 py-16">
        <div className="flex items-end justify-between mb-12">
          <div>
            <BlurFade delay={0.1}>
              <TextAnimate
                text="The Feed"
                className="text-4xl font-medium text-stone-900 tracking-tight"
              />
            </BlurFade>
            <BlurFade delay={0.2}>
              <p className="text-stone-500 mt-3 text-lg">
                AI-optimized content for agent consumption
              </p>
            </BlurFade>
          </div>
          <BlurFade delay={0.3}>
            <button
              onClick={refresh}
              className="bg-white hover:bg-stone-50 border border-stone-200 px-5 py-2.5 rounded-full text-sm text-stone-600 hover:text-stone-900 transition-all duration-200 shadow-sm hover:shadow"
            >
              Refresh
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
            <p className="text-stone-400 text-sm">Loading content...</p>
          </div>
        ) : items.length === 0 ? (
          <div className="text-center py-32">
            <div className="w-16 h-16 bg-stone-100 rounded-2xl flex items-center justify-center mx-auto mb-6">
              <span className="text-2xl">📭</span>
            </div>
            <p className="text-stone-600 text-lg mb-2">No content yet</p>
            <p className="text-stone-400">Content will appear here once added to the platform.</p>
          </div>
        ) : (
          <div className="space-y-5">
            {items.map((item, index) => (
              <BlurFade key={item.content.id} delay={0.05 * Math.min(index, 10)} inView>
                <ContentCard content={item.content} />
              </BlurFade>
            ))}

            <div ref={observerRef} className="h-10" />

            {isLoadingMore && (
              <div className="flex items-center justify-center py-6">
                <div className="spinner h-8 w-8"></div>
              </div>
            )}

            {!hasMore && items.length > 0 && (
              <div className="text-center py-8">
                <p className="text-stone-400 text-sm">
                  You&apos;ve reached the end
                </p>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
