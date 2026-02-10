'use client';

import type { Content } from '@/lib/types';
import { cn } from '@/lib/utils';
import { MagicCard } from '@/components/ui/magic-card';
import { useState } from 'react';

const typeConfig: Record<string, { bg: string; text: string; accent: string; gradient: string }> = {
  video: { bg: 'bg-rose-50', text: 'text-rose-700', accent: '#fda4af', gradient: 'from-rose-400 to-orange-300' },
  short: { bg: 'bg-pink-50', text: 'text-pink-700', accent: '#f9a8d4', gradient: 'from-pink-400 to-purple-400' },
  audio: { bg: 'bg-violet-50', text: 'text-violet-700', accent: '#c4b5fd', gradient: 'from-violet-400 to-indigo-400' },
  text: { bg: 'bg-sky-50', text: 'text-sky-700', accent: '#7dd3fc', gradient: 'from-sky-400 to-cyan-300' },
  image: { bg: 'bg-emerald-50', text: 'text-emerald-700', accent: '#6ee7b7', gradient: 'from-emerald-400 to-teal-300' },
  mixed: { bg: 'bg-amber-50', text: 'text-amber-700', accent: '#fcd34d', gradient: 'from-amber-400 to-yellow-300' },
};

function formatDuration(seconds: number | null | undefined): string {
  if (!seconds) return '';
  const mins = Math.floor(seconds / 60);
  const secs = Math.floor(seconds % 60);
  if (mins >= 60) {
    const hrs = Math.floor(mins / 60);
    const remainingMins = mins % 60;
    return `${hrs}:${remainingMins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  }
  return `${mins}:${secs.toString().padStart(2, '0')}`;
}

// Extract YouTube video ID from URL
function getYouTubeId(url: string | null | undefined): string | null {
  if (!url) return null;
  const match = url.match(/(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)([^&\s]+)/);
  return match ? match[1] : null;
}

export function ContentCard({ content, onClick }: { content: Content; onClick?: () => void }) {
  const config = typeConfig[content.type] || { bg: 'bg-stone-50', text: 'text-stone-700', accent: '#d6d3d1', gradient: 'from-stone-400 to-stone-300' };
  const isVideo = content.type === 'video' || content.type === 'short';
  const isAudio = content.type === 'audio';
  const duration = content.duration_seconds || (content.metadata as Record<string, number>)?.duration_seconds;
  const youtubeId = getYouTubeId(content.source_url);
  const [isPlaying, setIsPlaying] = useState(false);

  return (
    <MagicCard
      gradientColor={config.accent}
      gradientOpacity={0.3}
      className="card-hover cursor-pointer overflow-hidden"
    >
      <div className="w-full">
        {/* Video/Audio thumbnail or player */}
        {(isVideo || isAudio) && (
          <div className="relative w-full aspect-video bg-black overflow-hidden">
            {isPlaying && youtubeId ? (
              // Embedded YouTube player
              <iframe
                className="absolute inset-0 w-full h-full"
                src={`https://www.youtube.com/embed/${youtubeId}?autoplay=1&rel=0`}
                title={content.title}
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                allowFullScreen
              />
            ) : (
              // Thumbnail with play button
              <>
                {youtubeId ? (
                  // YouTube thumbnail
                  <img
                    src={`https://img.youtube.com/vi/${youtubeId}/maxresdefault.jpg`}
                    alt={content.title}
                    className="absolute inset-0 w-full h-full object-cover"
                    onError={(e) => {
                      // Fallback to hqdefault if maxres doesn't exist
                      (e.target as HTMLImageElement).src = `https://img.youtube.com/vi/${youtubeId}/hqdefault.jpg`;
                    }}
                  />
                ) : (
                  // Gradient placeholder for non-YouTube content
                  <div className={cn("absolute inset-0 bg-gradient-to-br", config.gradient)}>
                    <div className="absolute inset-0 flex items-center justify-center">
                      <div className="w-32 h-32 rounded-full bg-white/10 blur-2xl" />
                    </div>
                  </div>
                )}

                {/* Play button overlay */}
                <div
                  className="absolute inset-0 flex items-center justify-center bg-black/20 hover:bg-black/30 transition-colors"
                  onClick={(e) => {
                    e.stopPropagation();
                    if (youtubeId) {
                      setIsPlaying(true);
                    } else if (content.source_url) {
                      window.open(content.source_url, '_blank');
                    }
                  }}
                >
                  <div className={cn(
                    "w-16 h-16 rounded-full bg-white/95 flex items-center justify-center shadow-xl",
                    "transform transition-transform hover:scale-110"
                  )}>
                    {isAudio ? (
                      <svg className="w-7 h-7 text-stone-800" fill="currentColor" viewBox="0 0 24 24">
                        <path d="M12 3v10.55c-.59-.34-1.27-.55-2-.55-2.21 0-4 1.79-4 4s1.79 4 4 4 4-1.79 4-4V7h4V3h-6z"/>
                      </svg>
                    ) : (
                      <svg className="w-7 h-7 text-stone-800 ml-1" fill="currentColor" viewBox="0 0 24 24">
                        <path d="M8 5v14l11-7z"/>
                      </svg>
                    )}
                  </div>
                </div>

                {/* Duration badge */}
                {duration && (
                  <div className="absolute bottom-3 right-3 bg-black/80 text-white text-xs font-medium px-2 py-1 rounded">
                    {formatDuration(duration)}
                  </div>
                )}

                {/* Type badge */}
                <div className={cn(
                  "absolute top-3 left-3 text-xs px-2.5 py-1 rounded-full font-medium bg-white/95 shadow-sm",
                  config.text
                )}>
                  {content.type}
                </div>

                {/* YouTube badge */}
                {youtubeId && (
                  <div className="absolute top-3 right-3">
                    <svg className="w-8 h-6 text-red-600" viewBox="0 0 90 20" fill="currentColor">
                      <path d="M27.973 6.664c-.24-1.272-.945-2.29-1.897-2.536C24.25 3.6 15 3.6 15 3.6s-9.25 0-11.076.528c-.952.246-1.657 1.264-1.897 2.536C1.764 8.056 1.764 11 1.764 11s0 2.944.263 4.336c.24 1.272.945 2.29 1.897 2.536C5.75 18.4 15 18.4 15 18.4s9.25 0 11.076-.528c.952-.246 1.657-1.264 1.897-2.536.263-1.392.263-4.336.263-4.336s0-2.944-.263-4.336zM12.137 14.4V7.6l7.387 3.4-7.387 3.4z"/>
                    </svg>
                  </div>
                )}
              </>
            )}
          </div>
        )}

        {/* Content details */}
        <div className="p-5" onClick={onClick}>
          <div className="flex items-start justify-between mb-2">
            <h3 className="font-medium text-stone-800 text-base leading-snug line-clamp-2 flex-1">
              {content.title}
            </h3>
            {!isVideo && !isAudio && (
              <span className={cn(
                "text-xs px-2.5 py-1 rounded-full ml-3 shrink-0 font-medium",
                config.bg, config.text
              )}>
                {content.type}
              </span>
            )}
          </div>

          {content.description && (
            <p className="text-stone-500 text-sm mb-3 line-clamp-2 leading-relaxed">
              {content.description}
            </p>
          )}

          {content.tags && content.tags.length > 0 && (
            <div className="flex flex-wrap gap-1.5 mb-3">
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

          {/* Only show raw_text preview for non-video content */}
          {content.raw_text && !isVideo && !isAudio && (
            <div className="bg-stone-50 rounded-lg p-4 text-stone-600 text-sm max-h-28 overflow-hidden border border-stone-100">
              <p className="line-clamp-3 whitespace-pre-wrap font-mono text-xs leading-relaxed">
                {content.raw_text}
              </p>
            </div>
          )}

          <div className="flex items-center justify-between mt-3 pt-3 border-t border-stone-100">
            <span className="text-xs text-stone-400">
              {new Date(content.created_at).toLocaleDateString('en-US', {
                month: 'short',
                day: 'numeric',
                year: 'numeric'
              })}
            </span>
            {(content.metadata as Record<string, number>)?.views && (
              <span className="text-xs text-stone-400">
                {((content.metadata as Record<string, number>).views / 1000).toFixed(0)}K views
              </span>
            )}
          </div>
        </div>
      </div>
    </MagicCard>
  );
}
