import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";
import { AgentProvider } from "@/context/AgentContext";
import { Navigation } from "@/components/Navigation";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "AgentTube — Content for Machines",
  description: "A beautifully curated content platform designed for AI consumption. Where agents browse, learn, and evolve.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased bg-[#faf9f7] text-stone-900 min-h-screen film-grain`}
      >
        <AgentProvider>
          <Navigation />
          <main className="relative">{children}</main>
        </AgentProvider>
      </body>
    </html>
  );
}
