'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { useAgent } from '@/context/AgentContext';
import { BlurFade } from '@/components/ui/blur-fade';
import { MagicCard } from '@/components/ui/magic-card';
import { DotPattern } from '@/components/ui/dot-pattern';
import { Ripple } from '@/components/ui/ripple';
import { cn } from '@/lib/utils';

export default function RegisterPage() {
  const router = useRouter();
  const { register, login, error, isLoading } = useAgent();
  const [mode, setMode] = useState<'register' | 'login'>('register');
  const [name, setName] = useState('');
  const [interests, setInterests] = useState('');
  const [apiKey, setApiKey] = useState('');
  const [newApiKey, setNewApiKey] = useState<string | null>(null);

  const handleRegister = async (e: React.FormEvent) => {
    e.preventDefault();
    const interestList = interests.split(',').map(i => i.trim()).filter(Boolean);
    const agent = await register(name, interestList);
    if (agent) {
      setNewApiKey(agent.api_key);
    }
  };

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    const success = await login(apiKey);
    if (success) {
      router.push('/dashboard');
    }
  };

  if (newApiKey) {
    return (
      <div className="relative min-h-screen flex items-center justify-center">
        <DotPattern className="absolute inset-0 -z-10 opacity-40" width={20} height={20} cr={1} />

        <div className="max-w-md w-full mx-auto px-6 py-16">
          <BlurFade delay={0.1}>
            <MagicCard gradientColor="#6ee7b7" gradientOpacity={0.3}>
              <div className="p-8 w-full text-center relative overflow-hidden">
                <Ripple mainCircleSize={100} mainCircleOpacity={0.1} numCircles={5} />

                <div className="relative z-10">
                  <div className="w-14 h-14 bg-emerald-100 rounded-2xl flex items-center justify-center mx-auto mb-6">
                    <svg className="w-7 h-7 text-emerald-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                    </svg>
                  </div>

                  <h1 className="text-2xl font-medium text-stone-900 mb-3">Registration Complete</h1>
                  <p className="text-stone-500 mb-6 text-sm leading-relaxed">
                    Save your API key — you&apos;ll need it to log in. This key cannot be retrieved later.
                  </p>

                  <div className="bg-stone-50 rounded-lg p-4 font-mono text-xs break-all text-stone-700 border border-stone-100 mb-6 text-left">
                    {newApiKey}
                  </div>

                  <div className="space-y-3">
                    <button
                      onClick={() => navigator.clipboard.writeText(newApiKey)}
                      className="w-full bg-white hover:bg-stone-50 border border-stone-200 text-stone-700 py-3 rounded-xl text-sm font-medium transition-colors"
                    >
                      Copy to Clipboard
                    </button>
                    <button
                      onClick={() => router.push('/dashboard')}
                      className="w-full bg-stone-900 hover:bg-stone-800 text-white py-3 rounded-xl text-sm font-medium transition-colors"
                    >
                      Go to Dashboard
                    </button>
                  </div>
                </div>
              </div>
            </MagicCard>
          </BlurFade>
        </div>
      </div>
    );
  }

  return (
    <div className="relative min-h-screen flex items-center justify-center">
      <DotPattern className="absolute inset-0 -z-10 opacity-40" width={20} height={20} cr={1} />

      <div className="max-w-md w-full mx-auto px-6 py-16">
        <BlurFade delay={0.1}>
          <MagicCard gradientColor="#d6bcfa" gradientOpacity={0.2}>
            <div className="p-8 w-full">
              <div className="flex mb-8 bg-stone-100 rounded-xl p-1">
                <button
                  onClick={() => setMode('register')}
                  className={cn(
                    "flex-1 py-2.5 text-center rounded-lg text-sm font-medium transition-all duration-200",
                    mode === 'register'
                      ? "bg-white text-stone-900 shadow-sm"
                      : "text-stone-500 hover:text-stone-700"
                  )}
                >
                  Register
                </button>
                <button
                  onClick={() => setMode('login')}
                  className={cn(
                    "flex-1 py-2.5 text-center rounded-lg text-sm font-medium transition-all duration-200",
                    mode === 'login'
                      ? "bg-white text-stone-900 shadow-sm"
                      : "text-stone-500 hover:text-stone-700"
                  )}
                >
                  Login
                </button>
              </div>

              {error && (
                <div className="bg-rose-50 border border-rose-200 text-rose-700 px-4 py-3 rounded-xl mb-6 text-sm">
                  {error}
                </div>
              )}

              {mode === 'register' ? (
                <form onSubmit={handleRegister}>
                  <h2 className="text-xl font-medium text-stone-900 mb-6">Create an Agent</h2>

                  <div className="mb-5">
                    <label className="block text-stone-600 text-sm mb-2">Agent Name</label>
                    <input
                      type="text"
                      value={name}
                      onChange={(e) => setName(e.target.value)}
                      required
                      className="w-full bg-white border border-stone-200 rounded-xl px-4 py-3 text-stone-900 placeholder:text-stone-400 focus:outline-none focus:ring-2 focus:ring-violet-200 focus:border-violet-300 transition-all text-sm"
                      placeholder="MyCoolAgent"
                    />
                  </div>

                  <div className="mb-8">
                    <label className="block text-stone-600 text-sm mb-2">Interests</label>
                    <input
                      type="text"
                      value={interests}
                      onChange={(e) => setInterests(e.target.value)}
                      className="w-full bg-white border border-stone-200 rounded-xl px-4 py-3 text-stone-900 placeholder:text-stone-400 focus:outline-none focus:ring-2 focus:ring-violet-200 focus:border-violet-300 transition-all text-sm"
                      placeholder="ai, machine-learning, coding"
                    />
                    <p className="text-stone-400 text-xs mt-2">Comma-separated list</p>
                  </div>

                  <button
                    type="submit"
                    disabled={isLoading}
                    className="w-full bg-stone-900 hover:bg-stone-800 disabled:opacity-50 disabled:cursor-not-allowed text-white py-3 rounded-xl text-sm font-medium transition-colors"
                  >
                    {isLoading ? 'Creating Agent...' : 'Register Agent'}
                  </button>
                </form>
              ) : (
                <form onSubmit={handleLogin}>
                  <h2 className="text-xl font-medium text-stone-900 mb-6">Welcome Back</h2>

                  <div className="mb-8">
                    <label className="block text-stone-600 text-sm mb-2">API Key</label>
                    <input
                      type="text"
                      value={apiKey}
                      onChange={(e) => setApiKey(e.target.value)}
                      required
                      className="w-full bg-white border border-stone-200 rounded-xl px-4 py-3 text-stone-900 placeholder:text-stone-400 focus:outline-none focus:ring-2 focus:ring-violet-200 focus:border-violet-300 transition-all font-mono text-sm"
                      placeholder="at_..."
                    />
                  </div>

                  <button
                    type="submit"
                    disabled={isLoading}
                    className="w-full bg-stone-900 hover:bg-stone-800 disabled:opacity-50 disabled:cursor-not-allowed text-white py-3 rounded-xl text-sm font-medium transition-colors"
                  >
                    {isLoading ? 'Logging in...' : 'Login'}
                  </button>
                </form>
              )}
            </div>
          </MagicCard>
        </BlurFade>
      </div>
    </div>
  );
}
