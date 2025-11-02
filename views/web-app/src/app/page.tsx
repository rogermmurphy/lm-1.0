import Link from 'next/link';

export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      {/* Header */}
      <nav className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center">
              <h1 className="text-2xl font-bold text-blue-600">Little Monster</h1>
            </div>
            <div className="flex items-center space-x-4">
              <Link
                href="/login"
                className="text-gray-700 hover:text-blue-600 px-3 py-2 rounded-md text-sm font-medium"
              >
                Sign in
              </Link>
              <Link
                href="/register"
                className="bg-blue-600 text-white hover:bg-blue-700 px-4 py-2 rounded-md text-sm font-medium"
              >
                Get Started
              </Link>
            </div>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
        <div className="text-center">
          <h1 className="text-5xl font-bold text-gray-900 mb-6">
            Your AI-Powered Learning Companion
          </h1>
          <p className="text-xl text-gray-600 mb-8 max-w-2xl mx-auto">
            Get 24/7 tutoring, automatic transcription, and study material generation 
            powered by cutting-edge AI technology.
          </p>
          <div className="flex justify-center space-x-4">
            <Link
              href="/register"
              className="bg-blue-600 text-white hover:bg-blue-700 px-8 py-3 rounded-lg text-lg font-medium shadow-lg"
            >
              Start Learning Free
            </Link>
            <Link
              href="/login"
              className="bg-white text-blue-600 hover:bg-gray-50 px-8 py-3 rounded-lg text-lg font-medium shadow-lg border-2 border-blue-600"
            >
              Sign In
            </Link>
          </div>
        </div>

        {/* Features */}
        <div className="mt-20 grid grid-cols-1 md:grid-cols-3 gap-8">
          <div className="bg-white p-6 rounded-lg shadow-md">
            <div className="text-blue-600 text-3xl mb-4">💬</div>
            <h3 className="text-xl font-semibold mb-2">AI Tutoring</h3>
            <p className="text-gray-600">
              Chat with an AI tutor that understands your study materials and provides personalized help 24/7.
            </p>
          </div>

          <div className="bg-white p-6 rounded-lg shadow-md">
            <div className="text-blue-600 text-3xl mb-4">🎤</div>
            <h3 className="text-xl font-semibold mb-2">Audio Transcription</h3>
            <p className="text-gray-600">
              Record lectures and get automatic transcriptions with over 90% accuracy using AI technology.
            </p>
          </div>

          <div className="bg-white p-6 rounded-lg shadow-md">
            <div className="text-blue-600 text-3xl mb-4">🔊</div>
            <h3 className="text-xl font-semibold mb-2">Text-to-Speech</h3>
            <p className="text-gray-600">
              Convert any text to natural-sounding speech for better accessibility and on-the-go learning.
            </p>
          </div>
        </div>

        {/* CTA */}
        <div className="mt-20 bg-blue-600 rounded-2xl p-12 text-center text-white">
          <h2 className="text-3xl font-bold mb-4">Ready to transform your learning?</h2>
          <p className="text-xl mb-8 opacity-90">
            Join thousands of students already using AI to succeed.
          </p>
          <Link
            href="/register"
            className="bg-white text-blue-600 hover:bg-gray-100 px-8 py-3 rounded-lg text-lg font-medium inline-block"
          >
            Create Your Free Account
          </Link>
        </div>
      </div>
    </div>
  );
}
