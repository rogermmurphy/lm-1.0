'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';
import { useAuth } from '@/contexts/AuthContext';
import DashboardWidget from '@/components/DashboardWidget';
import axios from 'axios';

interface DashboardStats {
  conversations: number;
  classes: number;
  assignments: number;
  upcomingAssignments: number;
  studyPoints: number;
  studyStreak: number;
}

export default function DashboardPage() {
  const { user } = useAuth();
  const [stats, setStats] = useState<DashboardStats>({
    conversations: 0,
    classes: 0,
    assignments: 0,
    upcomingAssignments: 0,
    studyPoints: 0,
    studyStreak: 0
  });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadDashboardStats();
  }, []);

  const loadDashboardStats = async () => {
    try {
      // Load stats from various APIs (simplified - would need proper API endpoints)
      // For now using placeholder values that could be replaced with real API calls
      setStats({
        conversations: 5,
        classes: 8,
        assignments: 12,
        upcomingAssignments: 3,
        studyPoints: 245,
        studyStreak: 7
      });
    } catch (error) {
      console.error('Failed to load dashboard stats:', error);
    } finally {
      setLoading(false);
    }
  };

  const quickActions = [
    {
      title: 'Start AI Chat',
      description: 'Get help with your studies',
      icon: '💬',
      href: '/dashboard/chat',
      color: 'bg-blue-500',
    },
    {
      title: 'View Classes',
      description: 'Manage your courses',
      icon: '📚',
      href: '/dashboard/classes',
      color: 'bg-purple-500',
    },
    {
      title: 'Study Tools',
      description: 'Flashcards & practice tests',
      icon: '📝',
      href: '/dashboard/flashcards',
      color: 'bg-green-500',
    },
    {
      title: 'Study Groups',
      description: 'Collaborate with peers',
      icon: '👥',
      href: '/dashboard/groups',
      color: 'bg-orange-500',
    },
  ];

  return (
    <div className="space-y-8">
      {/* Welcome Header */}
      <div>
        <h1 className="text-3xl font-bold text-gray-900">
          Welcome back, {user?.username || user?.email?.split('@')[0]}!
        </h1>
        <p className="mt-2 text-gray-600">
          Here's your study overview for today
        </p>
      </div>

      {/* Key Metrics */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <DashboardWidget
          title="Study Streak"
          value={stats.studyStreak}
          subtitle="days in a row"
          icon="🔥"
          color="bg-red-500"
          trend={{ value: 12, isPositive: true }}
        />
        <DashboardWidget
          title="Study Points"
          value={stats.studyPoints}
          subtitle="total earned"
          icon="⭐"
          color="bg-yellow-500"
          trend={{ value: 8, isPositive: true }}
        />
        <DashboardWidget
          title="Active Classes"
          value={stats.classes}
          subtitle="this semester"
          icon="📚"
          color="bg-blue-500"
          href="/dashboard/classes"
        />
        <DashboardWidget
          title="Due Soon"
          value={stats.upcomingAssignments}
          subtitle="assignments"
          icon="⏰"
          color="bg-orange-500"
          href="/dashboard/assignments"
        />
      </div>

      {/* Quick Actions */}
      <div>
        <h2 className="text-xl font-semibold text-gray-900 mb-4">Quick Actions</h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          {quickActions.map((action) => (
            <Link
              key={action.href}
              href={action.href}
              className="block p-6 bg-white rounded-lg shadow-md hover:shadow-lg transition-all"
            >
              <div className={`${action.color} p-3 rounded-lg text-white text-3xl inline-block mb-3`}>
                {action.icon}
              </div>
              <h3 className="text-lg font-semibold text-gray-900">
                {action.title}
              </h3>
              <p className="mt-1 text-sm text-gray-600">
                {action.description}
              </p>
            </Link>
          ))}
        </div>
      </div>

      {/* Recent Activity & Upcoming */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Upcoming Assignments */}
        <div className="bg-white rounded-lg shadow-md p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">📅 Upcoming Assignments</h3>
          <div className="space-y-3">
            {[1, 2, 3].map((i) => (
              <div key={i} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                <div className="flex-1">
                  <div className="font-medium text-gray-900">Assignment {i}</div>
                  <div className="text-sm text-gray-500">Due in {i + 1} days</div>
                </div>
                <span className="px-3 py-1 bg-orange-100 text-orange-700 text-xs font-medium rounded-full">
                  Pending
                </span>
              </div>
            ))}
          </div>
          <Link href="/dashboard/assignments" className="mt-4 block text-center text-blue-600 hover:text-blue-700 text-sm font-medium">
            View All Assignments →
          </Link>
        </div>

        {/* Recent Achievements */}
        <div className="bg-white rounded-lg shadow-md p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">🏆 Recent Achievements</h3>
          <div className="space-y-3">
            <div className="flex items-center p-3 bg-gradient-to-r from-yellow-50 to-yellow-100 rounded-lg">
              <span className="text-3xl mr-3">🎯</span>
              <div>
                <div className="font-medium text-gray-900">First Study Session</div>
                <div className="text-sm text-gray-500">Completed today</div>
              </div>
            </div>
            <div className="flex items-center p-3 bg-gradient-to-r from-blue-50 to-blue-100 rounded-lg">
              <span className="text-3xl mr-3">📚</span>
              <div>
                <div className="font-medium text-gray-900">Study Streak 7 Days</div>
                <div className="text-sm text-gray-500">Keep it up!</div>
              </div>
            </div>
            <div className="flex items-center p-3 bg-gradient-to-r from-green-50 to-green-100 rounded-lg">
              <span className="text-3xl mr-3">⭐</span>
              <div>
                <div className="font-medium text-gray-900">100 Flashcards Reviewed</div>
                <div className="text-sm text-gray-500">Great progress!</div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Study Tips */}
      <div className="bg-gradient-to-r from-blue-50 to-indigo-50 border border-blue-200 rounded-lg p-6">
        <h3 className="text-lg font-semibold text-blue-900 mb-3 flex items-center">
          <span className="text-2xl mr-2">💡</span>
          Today's Study Tip
        </h3>
        <p className="text-blue-800">
          Break your study sessions into 25-minute focused intervals followed by 5-minute breaks. 
          This technique, known as the Pomodoro method, helps maintain concentration and prevents burnout.
        </p>
      </div>
    </div>
  );
}
