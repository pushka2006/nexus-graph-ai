import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "NEXUS GRAPH AI | Autonomous Company Intelligence & Multi-Agent Mesh",
  description: "Enterprise knowledge graph reasoning, persistent memory, and multi-agent coordination powered by FalkorDB.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="dark h-full antialiased">
      <body className="min-h-full flex flex-col bg-[#080c14] text-slate-100">{children}</body>
    </html>
  );
}
