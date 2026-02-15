import React from 'react';
import { SparklesIcon, DocumentTextIcon, FolderIcon, PencilSquareIcon } from '@heroicons/react/24/outline';
import { useApp } from '../context/AppContext';
import { useNavigate } from 'react-router-dom';

export const Dashboard = () => {
  const { user, profile } = useApp();
  const navigate = useNavigate();

  const features = [
    {
      icon: DocumentTextIcon,
      title: 'AI Resume Builder',
      description: 'Create professional resumes with AI-powered optimization',
      action: () => navigate('/resume'),
      color: 'blue',
    },
    {
      icon: FolderIcon,
      title: 'Portfolio Generator',
      description: 'Build stunning portfolios to showcase your projects',
      action: () => navigate('/portfolio'),
      color: 'purple',
    },
    {
      icon: PencilSquareIcon,
      title: 'Cover Letter',
      description: 'Generate tailored cover letters for any position',
      action: () => navigate('/cover-letter'),
      color: 'green',
    },
    {
      icon: SparklesIcon,
      title: 'AI Enhancement',
      description: 'Let AI optimize your content for maximum impact',
      action: () => navigate('/enhance'),
      color: 'yellow',
    },
  ];

  const colorClasses = {
    blue: 'bg-blue-100 text-blue-600',
    purple: 'bg-purple-100 text-purple-600',
    green: 'bg-green-100 text-green-600',
    yellow: 'bg-yellow-100 text-yellow-600',
  };

  return (
    <div className="container mx-auto px-4 py-12">
      {/* Welcome Section */}
      <div className="mb-12 text-center">
        <h1 className="text-4xl md:text-5xl font-bold text-gray-900 mb-4">
          Welcome, {user?.name || 'User'}! 👋
        </h1>
        <p className="text-xl text-gray-600">
          Build your professional presence with AI-powered tools
        </p>
      </div>

      {/* Profile Status */}
      {profile && (
        <div className="mb-12 p-6 bg-gradient-to-r from-blue-50 to-purple-50 rounded-lg border border-blue-200">
          <h2 className="text-lg font-semibold text-gray-800 mb-2">Profile Status</h2>
          <p className="text-gray-600">
            Your profile is {profile.updated_at ? 'up to date' : 'incomplete'}. Complete your profile for better AI suggestions.
          </p>
        </div>
      )}

      {/* Feature Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {features.map((feature, index) => {
          const IconComponent = feature.icon;
          return (
            <button
              key={index}
              onClick={feature.action}
              className="p-6 bg-white rounded-lg border border-gray-200 hover:border-blue-500 hover:shadow-lg transition text-left"
            >
              <div className={`w-12 h-12 rounded-lg ${colorClasses[feature.color]} flex items-center justify-center mb-4`}>
                <IconComponent className="w-6 h-6" />
              </div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">{feature.title}</h3>
              <p className="text-gray-600 mb-4">{feature.description}</p>
              <span className="inline-block text-sm font-semibold text-blue-600 hover:text-blue-700">
                Get Started →
              </span>
            </button>
          );
        })}
      </div>

      {/* Stats Section */}
      <div className="mt-12 grid grid-cols-1 md:grid-cols-3 gap-6">
        {[
          { label: 'Resumes Created', value: '0', color: 'blue' },
          { label: 'Portfolios Built', value: '0', color: 'purple' },
          { label: 'Cover Letters', value: '0', color: 'green' },
        ].map((stat, index) => (
          <div key={index} className="p-6 bg-white rounded-lg border border-gray-200 text-center">
            <p className={`text-3xl font-bold text-${stat.color}-600 mb-2`}>{stat.value}</p>
            <p className="text-gray-600">{stat.label}</p>
          </div>
        ))}
      </div>
    </div>
  );
};
