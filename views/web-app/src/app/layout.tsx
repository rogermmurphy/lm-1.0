import "./globals.css";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Little Monster",
  description: "Your AI-powered learning sidekick",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className="min-h-screen bg-lmCream text-lmGray font-lm">
        <header className="sticky top-0 z-10 bg-lmPink/90 backdrop-blur text-center py-4 text-2xl font-bold shadow">
          Little Monster 🩷
        </header>
        <main className="max-w-5xl mx-auto p-6">{children}</main>
      </body>
    </html>
  );
}
