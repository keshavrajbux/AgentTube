'use client';

import type { Content } from '@/lib/types';
import { cn } from '@/lib/utils';
import { MagicCard } from '@/components/ui/magic-card';

const typeConfig: Record<string, { bg: string; text: string; accent: string }> = {
  video: { bg: 'bg-rose-50', text: 'text-rose-700', accent: '#fda4af' },
  short: { bg: 'bg-pink-50', text: 'text-pink-700', accent: '#f9a8d4' },
  audio: { bg: 'bg-violet-50', text: 'text-violet-700', accent: '#c4b5fd' },
  text: { bg: 'bg-sky-50', text: 'text-sky-700', accent: '#7dd3fc' },
  image: { bg: 'bg-emerald-50', text: 'text-emerald-700', accent: '#6ee7b7' },
  mixed: { bg: 'bg-amber-50', text: 'text-amber-700', accent: '#fcd34d' },
};

export function ContentCard({ content, onClick }: { content: Content; onClick?: () => void }) {
  const config = typeConfig[content.type] || { bg: 'bg-stone-50', text: 'text-stone-700', accent: '#d6d3d1' };

  return (
    <MagicCard
      gradientColor={config.accent}
      gradientOpacity={0.3}
      className="card-hover cursor-pointer"
    >
      <div onClick={onClick} className="p-5 w-full">
        <div className="flex items-start justify-between mb-3">
          <h3 className="font-medium text-stone-800 text-base leading-snug line-clamp-2 flex-1">
            {content.title}
          </h3>
          <span className={cn(
            "text-xs px-2.5 py-1 rounded-full ml-3 shrink-0 font-medium",
            config.bg, config.text
          )}>
            {content.type}
          </span>
        </div>

        {content.description && (
          <p className="text-stone-500 text-sm mb-4 line-clamp-2 leading-relaxed">
            {content.description}
          </p>
        )}

        {content.tags && content.tags.length > 0 && (
          <div className="flex flex-wrap gap-1.5 mb-4">
            {content.tags.slice(0, 4).map(tag => (
              <span
                key={tag}
                className="bg-stone-100 text-stone-500 text-xs px-2 py-0.5 rounded-md"
              >
                #{tag}
              </span>
            ))}
          </div>
        )}

        {content.raw_text && (
          <div className="bg-stone-50 rounded-lg p-4 text-stone-600 text-sm max-h-28 overflow-hidden border border-stone-100">
            <p className="line-clamp-3 whitespace-pre-wrap font-mono text-xs leading-relaxed">
              {content.raw_text}
            </p>
          </div>
        )}

        <div className="flex items-center justify-between mt-4 pt-3 border-t border-stone-100">
          <span className="text-xs text-stone-400">
            {new Date(content.created_at).toLocaleDateString('en-US', {
              month: 'short',
              day: 'numeric',
              year: 'numeric'
            })}
          </span>
          {content.duration_seconds && (
            <span className="text-xs text-stone-400 font-mono">
              {Math.round(content.duration_seconds)}s
            </span>
          )}
        </div>
      </div>
    </MagicCard>
  );
}
