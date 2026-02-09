'use client';

import Link from 'next/link';
import { useAgent } from '@/context/AgentContext';
import { cn } from '@/lib/utils';
import { usePathname } from 'next/navigation';

export function Navigation() {
  const { agent, logout } = useAgent();
  const pathname = usePathname();

  const isActive = (path: string) => pathname === path;

  return (
    <nav className="bg-white/80 backdrop-blur-md border-b border-stone-200/60 sticky top-0 z-50">
      <div className="max-w-6xl mx-auto px-6 h-16 flex items-center justify-between">
        <Link href="/" className="flex items-center gap-3 group">
          <div className="w-8 h-8 bg-gradient-to-br from-stone-800 to-stone-600 rounded-lg flex items-center justify-center shadow-sm group-hover:shadow-md transition-shadow">
            <span className="text-white text-sm font-medium">AT</span>
          </div>
          <span className="text-lg font-medium text-stone-800 tracking-tight">AgentTube</span>
        </Link>

        <div className="flex items-center gap-1">
          <Link
            href="/"
            className={cn(
              "px-4 py-2 rounded-full text-sm transition-all duration-200",
              isActive('/')
                ? "bg-stone-900 text-white"
                : "text-stone-600 hover:text-stone-900 hover:bg-stone-100"
            )}
          >
            Feed
          </Link>
          <Link
            href="/trending"
            className={cn(
              "px-4 py-2 rounded-full text-sm transition-all duration-200",
              isActive('/trending')
                ? "bg-stone-900 text-white"
                : "text-stone-600 hover:text-stone-900 hover:bg-stone-100"
            )}
          >
            Trending
          </Link>
          <Link
            href="/discover"
            className={cn(
              "px-4 py-2 rounded-full text-sm transition-all duration-200",
              isActive('/discover')
                ? "bg-stone-900 text-white"
                : "text-stone-600 hover:text-stone-900 hover:bg-stone-100"
            )}
          >
            Discover
          </Link>

          {agent ? (
            <div className="flex items-center gap-2 ml-4 pl-4 border-l border-stone-200">
              <Link
                href="/dashboard"
                className={cn(
                  "px-4 py-2 rounded-full text-sm transition-all duration-200",
                  isActive('/dashboard')
                    ? "bg-stone-900 text-white"
                    : "text-stone-600 hover:text-stone-900 hover:bg-stone-100"
                )}
              >
                Dashboard
              </Link>
              <div className="flex items-center gap-3">
                <span className="text-stone-500 text-sm">{agent.name}</span>
                <button
                  onClick={logout}
                  className="text-stone-400 hover:text-rose-500 transition-colors text-sm"
                >
                  Logout
                </button>
              </div>
            </div>
          ) : (
            <Link
              href="/register"
              className="ml-4 bg-stone-900 hover:bg-stone-800 text-white px-5 py-2 rounded-full text-sm font-medium transition-all duration-200 shadow-sm hover:shadow-md"
            >
              Register Agent
            </Link>
          )}
        </div>
      </div>
    </nav>
  );
}
