import React, { useState } from 'react';
import { useApp } from '../context/AppContext';
import { resumeAPI } from '../services/api';
import toast from 'react-hot-toast';
import { ArrowDownTrayIcon } from '@heroicons/react/24/outline';

export const Resume = () => {
  const { profile, setLoading, loading } = useApp();
  const [template, setTemplate] = useState('professional');
  const [format, setFormat] = useState('pdf');
  const [resume, setResume] = useState(null);

  const templates = [
    { id: 'professional', name: 'Professional', description: 'Traditional formal resume' },
    { id: 'modern', name: 'Modern', description: 'Contemporary design' },
    { id: 'simple', name: 'Simple', description: 'Clean and minimal' },
    { id: 'technical', name: 'Technical', description: 'Tech-focused layout' },
  ];

  const formats = [
    { id: 'pdf', name: 'PDF', icon: '📄' },
    { id: 'docx', name: 'Word', icon: '📝' },
    { id: 'html', name: 'HTML', icon: '🌐' },
  ];

  const handleGenerateResume = async () => {
    if (!profile) {
      toast.error('Please complete your profile first');
      return;
    }

    setLoading(true);
    try {
      const response = await resumeAPI.generateResume(profile, template, format);
      setResume(response.data);
      toast.success('Resume generated successfully!');
    } catch (error) {
      toast.error('Failed to generate resume');
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const handleDownloadResume = async () => {
    if (!resume) return;

    try {
      const response = await resumeAPI.exportResume(resume, format, 'resume');
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `resume.${format === 'docx' ? 'docx' : format}`);
      document.body.appendChild(link);
      link.click();
      link.parentElement.removeChild(link);
      toast.success('Resume downloaded!');
    } catch (error) {
      toast.error('Download failed');
    }
  };

  return (
    <div className="container mx-auto px-4 py-12">
      <h1 className="text-4xl font-bold text-gray-900 mb-8">Resume Generator</h1>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Configuration Panel */}
        <div className="lg:col-span-1">
          <div className="bg-white rounded-lg border border-gray-200 p-6">
            <h2 className="text-xl font-semibold text-gray-900 mb-6">Template & Format</h2>

            {/* Template Selection */}
            <div className="mb-8">
              <label className="block text-sm font-semibold text-gray-700 mb-3">Select Template</label>
              <div className="space-y-2">
                {templates.map((tmpl) => (
                  <button
                    key={tmpl.id}
                    onClick={() => setTemplate(tmpl.id)}
                    className={`w-full p-3 rounded-lg border-2 text-left transition ${
                      template === tmpl.id
                        ? 'border-blue-600 bg-blue-50'
                        : 'border-gray-200 hover:border-blue-300'
                    }`}
                  >
                    <p className="font-semibold text-gray-900">{tmpl.name}</p>
                    <p className="text-sm text-gray-600">{tmpl.description}</p>
                  </button>
                ))}
              </div>
            </div>

            {/* Format Selection */}
            <div className="mb-8">
              <label className="block text-sm font-semibold text-gray-700 mb-3">Export Format</label>
              <div className="flex gap-2">
                {formats.map((fmt) => (
                  <button
                    key={fmt.id}
                    onClick={() => setFormat(fmt.id)}
                    className={`flex-1 p-3 rounded-lg border-2 text-center transition ${
                      format === fmt.id
                        ? 'border-blue-600 bg-blue-50'
                        : 'border-gray-200 hover:border-blue-300'
                    }`}
                  >
                    <span className="text-xl">{fmt.icon}</span>
                    <p className="text-xs font-semibold text-gray-700">{fmt.name}</p>
                  </button>
                ))}
              </div>
            </div>

            {/* Action Buttons */}
            <div className="space-y-3">
              <button
                onClick={handleGenerateResume}
                disabled={loading}
                className="w-full px-6 py-3 bg-gradient-to-r from-blue-600 to-purple-600 text-white font-semibold rounded-lg hover:shadow-lg transition disabled:opacity-50"
              >
                {loading ? 'Generating...' : 'Generate Resume'}
              </button>
              {resume && (
                <button
                  onClick={handleDownloadResume}
                  className="w-full flex items-center justify-center gap-2 px-6 py-3 border border-gray-300 text-gray-700 font-semibold rounded-lg hover:bg-gray-50 transition"
                >
                  <ArrowDownTrayIcon className="w-5 h-5" />
                  Download
                </button>
              )}
            </div>
          </div>
        </div>

        {/* Preview Panel */}
        <div className="lg:col-span-2">
          <div className="bg-white rounded-lg border border-gray-200 p-6">
            <h2 className="text-xl font-semibold text-gray-900 mb-6">Preview</h2>
            {resume ? (
              <div className="bg-gray-50 rounded-lg p-8 overflow-y-auto max-h-96">
                <div className="bg-white p-6 rounded text-gray-800 font-serif text-sm leading-relaxed">
                  {resume}
                </div>
              </div>
            ) : (
              <div className="bg-gray-50 rounded-lg p-8 text-center text-gray-500">
                <p>Your resume preview will appear here</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};
