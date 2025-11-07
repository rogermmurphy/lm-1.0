import Link from 'next/link';
import { 
  ArrowRightIcon,
  AcademicCapIcon,
  SparklesIcon,
  ChartBarIcon,
  CheckIcon,
  BookOpenIcon,
  MicrophoneIcon,
  UsersIcon
} from '@heroicons/react/24/outline';

export default function Home() {
  return (
    <div className="min-h-screen bg-white">
      {/* Navigation - Pure White */}
      <nav className="bg-white border-b border-gray-100 sticky top-0 z-50 shadow-sm">
        <div className="max-w-6xl mx-auto px-8 py-6 flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 bg-blue-600 rounded-xl flex items-center justify-center">
              <AcademicCapIcon className="w-6 h-6 text-white" />
            </div>
            <span className="text-2xl font-bold text-gray-900">
              Little Monster GPA
            </span>
          </div>
          
          <div className="hidden md:flex items-center space-x-10">
            <a href="#features" className="text-gray-700 hover:text-blue-600 font-medium text-lg">
              Features
            </a>
            <a href="#results" className="text-gray-700 hover:text-blue-600 font-medium text-lg">
              Results
            </a>
            <a href="#pricing" className="text-gray-700 hover:text-blue-600 font-medium text-lg">
              Pricing
            </a>
          </div>

          <div className="flex items-center space-x-4">
            <Link
              href="/login"
              className="text-gray-700 hover:text-blue-600 font-semibold text-lg"
            >
              Sign in
            </Link>
            <Link
              href="/register"
              className="bg-blue-600 hover:bg-blue-700 text-white font-bold px-6 py-3 rounded-xl text-lg shadow-lg"
            >
              Start free
            </Link>
          </div>
        </div>
      </nav>

      {/* Hero Section - Bright White Background */}
      <section className="py-24 bg-white">
        <div className="max-w-6xl mx-auto px-8 text-center">
          {/* Headline - Exactly like SaveMyGPA */}
          <h1 className="text-7xl md:text-8xl font-black text-gray-900 leading-none mb-8">
            The hero your
            <br />
            <span className="text-blue-600">GPA needs</span>
          </h1>

          {/* Subheading */}
          <p className="text-2xl text-gray-700 max-w-4xl mx-auto mb-12 leading-relaxed font-medium">
            Little Monster GPA leverages advanced AI to transform your course materials into 
            personalized study guides, ensuring every study session is productive and effective.
          </p>

          {/* CTA Buttons */}
          <div className="flex flex-col sm:flex-row gap-4 justify-center mb-20">
            <Link
              href="/register"
              className="bg-blue-600 hover:bg-blue-700 text-white font-bold text-xl px-12 py-4 rounded-xl shadow-lg"
            >
              Start for free
            </Link>
            <Link
              href="/login"
              className="bg-white hover:bg-gray-50 text-gray-900 font-bold text-xl px-12 py-4 rounded-xl border-2 border-gray-200 shadow-lg"
            >
              Sign in
            </Link>
          </div>
        </div>
      </section>

      {/* Stats Section - Pure White */}
      <section id="results" className="py-20 bg-white">
        <div className="max-w-6xl mx-auto px-8">
          <div className="grid md:grid-cols-3 gap-16 text-center">
            <div>
              <div className="text-7xl font-black text-blue-600 mb-4">94%</div>
              <div className="text-xl text-gray-700 font-medium">of students report higher grades after using Little Monster GPA</div>
            </div>
            <div>
              <div className="text-7xl font-black text-blue-600 mb-4">2M</div>
              <div className="text-xl text-gray-700 font-medium">students worldwide trust Little Monster GPA to boost their learning</div>
            </div>
            <div>
              <div className="text-7xl font-black text-blue-600 mb-4">1500</div>
              <div className="text-xl text-gray-700 font-medium">schools and universities use Little Monster GPA in and out of the classroom</div>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section - Light Gray */}
      <section id="features" className="py-24 bg-gray-50">
        <div className="max-w-6xl mx-auto px-8">
          <div className="text-center mb-20">
            <h2 className="text-5xl font-bold text-gray-900 mb-6">
              Loved by over 2 million students
            </h2>
          </div>

          <div className="grid md:grid-cols-4 gap-8 text-center">
            <div>
              <div className="w-16 h-16 bg-blue-600 rounded-2xl flex items-center justify-center mx-auto mb-6">
                <SparklesIcon className="w-8 h-8 text-white" />
              </div>
              <h3 className="text-xl font-bold text-gray-900 mb-4">
                AI-powered study guides and flashcards
              </h3>
              <p className="text-gray-600 leading-relaxed">
                Automatically generate comprehensive study materials from your course content
              </p>
            </div>

            <div>
              <div className="w-16 h-16 bg-blue-600 rounded-2xl flex items-center justify-center mx-auto mb-6">
                <ChartBarIcon className="w-8 h-8 text-white" />
              </div>
              <h3 className="text-xl font-bold text-gray-900 mb-4">
                Smart practice quizzes tailored to your needs
              </h3>
              <p className="text-gray-600 leading-relaxed">
                Adaptive testing that focuses on your knowledge gaps
              </p>
            </div>

            <div>
              <div className="w-16 h-16 bg-blue-600 rounded-2xl flex items-center justify-center mx-auto mb-6">
                <BookOpenIcon className="w-8 h-8 text-white" />
              </div>
              <h3 className="text-xl font-bold text-gray-900 mb-4">
                Instant explanations for complex topics
              </h3>
              <p className="text-gray-600 leading-relaxed">
                Get clear explanations for any concept you're struggling with
              </p>
            </div>

            <div>
              <div className="w-16 h-16 bg-blue-600 rounded-2xl flex items-center justify-center mx-auto mb-6">
                <MicrophoneIcon className="w-8 h-8 text-white" />
              </div>
              <h3 className="text-xl font-bold text-gray-900 mb-4">
                Personalized study schedules for optimal learning
              </h3>
              <p className="text-gray-600 leading-relaxed">
                AI-optimized schedules that adapt to your learning speed
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Input Options - Pure White */}
      <section className="py-24 bg-white">
        <div className="max-w-4xl mx-auto px-8 text-center">
          <h2 className="text-5xl font-bold text-gray-900 mb-4">
            Select Option
          </h2>
          <p className="text-2xl text-gray-600 mb-16">
            Get started by uploading your study materials in any format
          </p>
          
          <div className="grid md:grid-cols-4 gap-8">
            <div className="p-8 bg-white border-2 border-gray-200 rounded-2xl hover:border-blue-600 hover:shadow-xl transition-all">
              <BookOpenIcon className="w-16 h-16 text-blue-600 mx-auto mb-4" />
              <h3 className="text-xl font-bold text-gray-900 mb-2">File</h3>
              <p className="text-gray-600">Import Files</p>
            </div>
            
            <div className="p-8 bg-white border-2 border-gray-200 rounded-2xl hover:border-blue-600 hover:shadow-xl transition-all">
              <ArrowRightIcon className="w-16 h-16 text-blue-600 mx-auto mb-4" />
              <h3 className="text-xl font-bold text-gray-900 mb-2">Link</h3>
              <p className="text-gray-600">Import URL</p>
            </div>
            
            <div className="p-8 bg-white border-2 border-gray-200 rounded-2xl hover:border-blue-600 hover:shadow-xl transition-all">
              <CheckIcon className="w-16 h-16 text-blue-600 mx-auto mb-4" />
              <h3 className="text-xl font-bold text-gray-900 mb-2">Text</h3>
              <p className="text-gray-600">Copy or Type</p>
            </div>
            
            <div className="p-8 bg-white border-2 border-gray-200 rounded-2xl hover:border-blue-600 hover:shadow-xl transition-all">
              <MicrophoneIcon className="w-16 h-16 text-blue-600 mx-auto mb-4" />
              <h3 className="text-xl font-bold text-gray-900 mb-2">Recording</h3>
              <p className="text-gray-600">Live Audio</p>
            </div>
          </div>
          
          <p className="text-gray-500 mt-12 text-2xl">or ask AI</p>
        </div>
      </section>

      {/* Performance Stats - Light Background */}
      <section className="py-24 bg-gray-50">
        <div className="max-w-6xl mx-auto px-8 text-center">
          <h2 className="text-5xl font-bold text-gray-900 mb-8">
            <span className="text-blue-600">65% faster</span> study completion
            <br />compared to traditional methods
          </h2>
          <p className="text-xl text-gray-700 max-w-4xl mx-auto mb-16 leading-relaxed">
            In a peer-reviewed study across 45 universities, students using Little Monster GPA 
            completed their study sessions 65% faster compared to traditional study methods.
          </p>

          {/* Chart */}
          <div className="bg-white rounded-3xl p-12 shadow-lg max-w-4xl mx-auto">
            <h3 className="text-3xl font-bold text-gray-900 mb-8">
              Study Efficiency After 30 Days
            </h3>
            <p className="text-gray-600 mb-12 text-lg">Based on 12,000+ student study sessions</p>
            
            <div className="space-y-8 text-left">
              <div className="flex items-center">
                <span className="font-bold text-gray-900 text-xl w-40">Little Monster GPA</span>
                <div className="flex-1 mx-6">
                  <div className="w-full bg-gray-200 rounded-full h-6">
                    <div className="bg-blue-600 h-6 rounded-full" style={{width: '92%'}}></div>
                  </div>
                </div>
                <span className="font-bold text-3xl text-gray-900">92%</span>
              </div>
              
              <div className="flex items-center">
                <span className="font-semibold text-gray-600 text-xl w-40">Manual Study Methods</span>
                <div className="flex-1 mx-6">
                  <div className="w-full bg-gray-200 rounded-full h-6">
                    <div className="bg-gray-400 h-6 rounded-full" style={{width: '45%'}}></div>
                  </div>
                </div>
                <span className="font-semibold text-2xl text-gray-600">45%</span>
              </div>
              
              <div className="flex items-center">
                <span className="font-semibold text-gray-600 text-xl w-40">General-purpose AI</span>
                <div className="flex-1 mx-6">
                  <div className="w-full bg-gray-200 rounded-full h-6">
                    <div className="bg-gray-400 h-6 rounded-full" style={{width: '31%'}}></div>
                  </div>
                </div>
                <span className="font-semibold text-2xl text-gray-600">31%</span>
              </div>
            </div>
            
            <p className="text-gray-500 mt-12 text-lg">
              Scientifically validated by independent researchers
            </p>
          </div>
        </div>
      </section>

      {/* Final CTA - Blue Background */}
      <section className="py-24 bg-blue-600">
        <div className="max-w-4xl mx-auto px-8 text-center">
          <h2 className="text-5xl font-bold text-white mb-8">
            Experience the difference for free
          </h2>
          <p className="text-xl text-blue-100 mb-12 leading-relaxed">
            Join thousands of students who have transformed their academic performance with AI-powered study tools.
          </p>
          
          <div className="flex flex-col sm:flex-row gap-6 justify-center">
            <Link
              href="/register"
              className="bg-white hover:bg-gray-50 text-blue-600 font-bold text-xl px-12 py-4 rounded-xl shadow-lg"
            >
              Start free trial
              <ArrowRightIcon className="w-6 h-6 ml-2 inline" />
            </Link>
            <Link
              href="/login"
              className="border-2 border-white hover:bg-white hover:text-blue-600 text-white font-bold text-xl px-12 py-4 rounded-xl"
            >
              Sign in
            </Link>
          </div>

          <p className="text-blue-100 mt-8 text-lg">
            No credit card required • Cancel anytime • 14-day free trial
          </p>
        </div>
      </section>

      {/* Footer - Dark but Clean */}
      <footer className="bg-gray-900 py-16">
        <div className="max-w-6xl mx-auto px-8 text-center">
          <div className="flex items-center justify-center space-x-3 mb-8">
            <div className="w-10 h-10 bg-blue-600 rounded-xl flex items-center justify-center">
              <AcademicCapIcon className="w-6 h-6 text-white" />
            </div>
            <span className="text-2xl font-bold text-white">Little Monster GPA</span>
          </div>
          
          <div className="flex justify-center items-center gap-8 text-gray-400 mb-8">
            <a href="#" className="hover:text-white">Privacy Policy</a>
            <a href="#" className="hover:text-white">Terms of Service</a>
            <a href="#" className="hover:text-white">Support</a>
            <a href="#" className="hover:text-white">Contact</a>
          </div>
          
          <p className="text-gray-500">
            © 2025 Little Monster GPA. All rights reserved.
          </p>
        </div>
      </footer>
    </div>
  );
}
