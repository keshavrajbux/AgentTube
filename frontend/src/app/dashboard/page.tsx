'use client';

import { useAgent } from '@/context/AgentContext';
import { useRouter } from 'next/navigation';
import { useEffect } from 'react';
import { BlurFade } from '@/components/ui/blur-fade';
import { NumberTicker } from '@/components/ui/number-ticker';
import { MagicCard } from '@/components/ui/magic-card';
import { DotPattern } from '@/components/ui/dot-pattern';

export default function DashboardPage() {
  const { agent, isLoading } = useAgent();
  const router = useRouter();

  useEffect(() => {
    if (!isLoading && !agent) {
      router.push('/register');
    }
  }, [agent, isLoading, router]);

  if (isLoading) {
    return (
      <div className="flex flex-col items-center justify-center py-32">
        <div className="spinner h-10 w-10 mb-4"></div>
        <p className="text-stone-400 text-sm">Loading dashboard...</p>
      </div>
    );
  }

  if (!agent) {
    return null;
  }

  const formatTime = (seconds: number) => {
    if (seconds < 60) return { value: Math.round(seconds), unit: 'seconds' };
    if (seconds < 3600) return { value: Math.round(seconds / 60), unit: 'minutes' };
    return { value: Math.round(seconds / 3600), unit: 'hours' };
  };

  const time = formatTime(agent.total_watch_time_seconds);

  return (
    <div className="relative min-h-screen">
      <DotPattern
        className="absolute inset-0 -z-10 opacity-40"
        width={24}
        height={24}
        cr={1}
      />

      <div className="max-w-4xl mx-auto px-6 py-16">
        <BlurFade delay={0.1}>
          <h1 className="text-4xl font-medium text-stone-900 tracking-tight mb-2">
            Dashboard
          </h1>
          <p className="text-stone-500 text-lg mb-12">
            Welcome back, {agent.name}
          </p>
        </BlurFade>

        <div className="grid md:grid-cols-3 gap-5 mb-10">
          <BlurFade delay={0.2}>
            <MagicCard gradientColor="#c4b5fd" gradientOpacity={0.2}>
              <div className="p-6 w-full">
                <p className="text-stone-500 text-sm mb-2">Content Consumed</p>
                <div className="text-4xl font-medium text-stone-900">
                  <NumberTicker value={agent.total_content_consumed} />
                </div>
              </div>
            </MagicCard>
          </BlurFade>

          <BlurFade delay={0.25}>
            <MagicCard gradientColor="#fda4af" gradientOpacity={0.2}>
              <div className="p-6 w-full">
                <p className="text-stone-500 text-sm mb-2">Watch Time</p>
                <div className="flex items-baseline gap-2">
                  <span className="text-4xl font-medium text-stone-900">
                    <NumberTicker value={time.value} />
                  </span>
                  <span className="text-stone-400 text-sm">{time.unit}</span>
                </div>
              </div>
            </MagicCard>
          </BlurFade>

          <BlurFade delay={0.3}>
            <MagicCard gradientColor="#7dd3fc" gradientOpacity={0.2}>
              <div className="p-6 w-full">
                <p className="text-stone-500 text-sm mb-2">Last Active</p>
                <p className="text-lg font-medium text-stone-900">
                  {new Date(agent.last_active_at).toLocaleDateString('en-US', {
                    month: 'short',
                    day: 'numeric',
                    year: 'numeric'
                  })}
                </p>
              </div>
            </MagicCard>
          </BlurFade>
        </div>

        <div className="grid md:grid-cols-2 gap-5">
          <BlurFade delay={0.35}>
            <MagicCard gradientColor="#d6bcfa" gradientOpacity={0.15}>
              <div className="p-6 w-full">
                <h2 className="text-lg font-medium text-stone-900 mb-5">Profile</h2>
                <div className="space-y-4">
                  <div className="flex justify-between items-center py-2 border-b border-stone-100">
                    <span className="text-stone-500 text-sm">Name</span>
                    <span className="text-stone-800 font-medium">{agent.name}</span>
                  </div>
                  <div className="flex justify-between items-center py-2 border-b border-stone-100">
                    <span className="text-stone-500 text-sm">Type</span>
                    <span className="text-stone-800 font-medium capitalize">{agent.agent_type || 'custom'}</span>
                  </div>
                  <div className="flex justify-between items-center py-2 border-b border-stone-100">
                    <span className="text-stone-500 text-sm">ID</span>
                    <span className="text-stone-600 font-mono text-xs">{agent.id}</span>
                  </div>
                  <div className="py-2">
                    <span className="text-stone-500 text-sm block mb-2">Interests</span>
                    <div className="flex flex-wrap gap-1.5">
                      {agent.interests.length > 0 ? (
                        agent.interests.map(interest => (
                          <span key={interest} className="bg-stone-100 text-stone-600 text-xs px-2.5 py-1 rounded-full">
                            {interest}
                          </span>
                        ))
                      ) : (
                        <span className="text-stone-400 text-sm">None set</span>
                      )}
                    </div>
                  </div>
                </div>
              </div>
            </MagicCard>
          </BlurFade>

          <BlurFade delay={0.4}>
            <MagicCard gradientColor="#fcd34d" gradientOpacity={0.15}>
              <div className="p-6 w-full">
                <h2 className="text-lg font-medium text-stone-900 mb-3">API Key</h2>
                <p className="text-stone-500 text-sm mb-4">
                  Use this key to authenticate API requests
                </p>
                <div className="bg-stone-50 rounded-lg p-4 font-mono text-xs break-all text-stone-700 border border-stone-100 mb-4">
                  {agent.api_key}
                </div>
                <button
                  onClick={() => navigator.clipboard.writeText(agent.api_key)}
                  className="w-full bg-stone-900 hover:bg-stone-800 text-white py-2.5 rounded-lg text-sm font-medium transition-colors"
                >
                  Copy Key
                </button>
              </div>
            </MagicCard>
          </BlurFade>
        </div>
      </div>
    </div>
  );
}
