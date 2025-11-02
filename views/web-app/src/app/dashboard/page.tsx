'use client';

import Link from 'next/link';
import { useAuth } from '@/contexts/AuthContext';

export default function DashboardPage() {
  const { user } = useAuth();

  const features = [
    {
      title: 'AI Chat',
      description: 'Chat with your AI tutor powered by local LLM',
      icon: '💬',
      href: '/dashboard/chat',
      color: 'bg-blue-500',
    },
    {
      title: 'Transcribe Audio',
      description: 'Convert audio to text with Whisper AI',
      icon: '🎤',
      href: '/dashboard/transcribe',
      color: 'bg-green-500',
    },
    {
      title: 'Text-to-Speech',
      description: 'Generate natural speech from text',
      icon: '🔊',
      href: '/dashboard/tts',
      color: 'bg-purple-500',
    },
    {
      title: 'Study Materials',
      description: 'Manage your learning resources',
      icon: '📚',
      href: '/dashboard/materials',
      color: 'bg-orange-500',
    },
  ];

  return (
    <div>
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">
          Welcome back, {user?.username || user?.email?.split('@')[0]}!
        </h1>
        <p className="mt-2 text-gray-600">
          Choose a feature to get started with your AI-powered learning experience.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {features.map((feature) => (
          <Link
            key={feature.href}
            href={feature.href}
            className="block p-6 bg-white rounded-lg shadow-md hover:shadow-lg transition-shadow"
          >
            <div className="flex items-start">
              <div className={`${feature.color} p-3 rounded-lg text-white text-2xl`}>
                {feature.icon}
              </div>
              <div className="ml-4">
                <h3 className="text-lg font-semibold text-gray-900">
                  {feature.title}
                </h3>
                <p className="mt-1 text-sm text-gray-600">
                  {feature.description}
                </p>
              </div>
            </div>
          </Link>
        ))}
      </div>

      <div className="mt-8 bg-blue-50 border border-blue-200 rounded-lg p-6">
        <h3 className="text-lg font-semibold text-blue-900 mb-2">
          🚀 Quick Start Guide
        </h3>
        <ul className="space-y-2 text-sm text-blue-800">
          <li>• Start a conversation with the AI tutor to get help with any subject</li>
          <li>• Upload audio recordings to get automatic transcriptions</li>
          <li>• Convert study notes to speech for on-the-go learning</li>
          <li>• Upload study materials to enable RAG-powered tutoring</li>
        </ul>
      </div>

      <div className="mt-6 grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-white p-4 rounded-lg shadow">
          <div className="text-2xl font-bold text-blue-600">0</div>
          <div className="text-sm text-gray-600">Conversations</div>
        </div>
        <div className="bg-white p-4 rounded-lg shadow">
          <div className="text-2xl font-bold text-green-600">0</div>
          <div className="text-sm text-gray-600">Transcriptions</div>
        </div>
        <div className="bg-white p-4 rounded-lg shadow">
          <div className="text-2xl font-bold text-orange-600">0</div>
          <div className="text-sm text-gray-600">Study Materials</div>
        </div>
      </div>
    </div>
  );
}
