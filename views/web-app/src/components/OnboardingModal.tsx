'use client';

import { useState, useEffect } from 'react';

export default function OnboardingModal() {
  const [isOpen, setIsOpen] = useState(false);
  const [currentStep, setCurrentStep] = useState(0);

  useEffect(() => {
    // DISABLED FOR TESTING: Auto-set onboarding as seen
    localStorage.setItem('hasSeenOnboarding', 'true');
    setIsOpen(false);
  }, []);

  const steps = [
    {
      title: 'Welcome to Little Monster GPA! 🎓',
      description: 'Your AI-powered study companion is ready to help you succeed.',
      icon: '🎉',
    },
    {
      title: 'AI Tutor Chat 💬',
      description: 'Get instant help with any subject. Ask questions, solve problems, and learn faster.',
      icon: '💬',
    },
    {
      title: 'Study Tools 📝',
      description: 'Create flashcards, take practice tests, and generate study notes automatically.',
      icon: '📝',
    },
    {
      title: 'Track Your Progress 📊',
      description: 'Monitor your study sessions, earn achievements, and compete on leaderboards.',
      icon: '📊',
    },
  ];

  const handleClose = () => {
    localStorage.setItem('hasSeenOnboarding', 'true');
    setIsOpen(false);
  };

  const handleNext = () => {
    if (currentStep < steps.length - 1) {
      setCurrentStep(currentStep + 1);
    } else {
      handleClose();
    }
  };

  const handlePrevious = () => {
    if (currentStep > 0) {
      setCurrentStep(currentStep - 1);
    }
  };

  if (!isOpen) return null;

  const step = steps[currentStep];

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-lg shadow-xl max-w-md w-full p-8 relative">
        {/* Close button */}
        <button
          onClick={handleClose}
          className="absolute top-4 right-4 text-gray-400 hover:text-gray-600"
        >
          <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>

        {/* Content */}
        <div className="text-center">
          <div className="text-6xl mb-4">{step.icon}</div>
          <h2 className="text-2xl font-bold text-gray-900 mb-3">{step.title}</h2>
          <p className="text-gray-600 mb-6">{step.description}</p>

          {/* Progress indicators */}
          <div className="flex justify-center gap-2 mb-6">
            {steps.map((_, index) => (
              <div
                key={index}
                className={`h-2 w-2 rounded-full transition-all ${
                  index === currentStep ? 'bg-blue-600 w-8' : 'bg-gray-300'
                }`}
              />
            ))}
          </div>

          {/* Navigation buttons */}
          <div className="flex gap-3">
            {currentStep > 0 && (
              <button
                onClick={handlePrevious}
                className="flex-1 px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors"
              >
                Previous
              </button>
            )}
            <button
              onClick={handleNext}
              className="flex-1 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors font-medium"
            >
              {currentStep < steps.length - 1 ? 'Next' : 'Get Started'}
            </button>
          </div>

          <button
            onClick={handleClose}
            className="mt-4 text-sm text-gray-500 hover:text-gray-700"
          >
            Skip tutorial
          </button>
        </div>
      </div>
    </div>
  );
}
