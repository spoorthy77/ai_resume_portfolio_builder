import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { Toaster } from 'react-hot-toast';
import { AppProvider, useApp } from './context/AppContext';
import { Header } from './components/Header';
import { Dashboard } from './pages/Dashboard';
import { Login } from './pages/Login';
import { Resume } from './pages/Resume';

// Home Page Component
const Home = () => (
  <div className="bg-gradient-to-br from-blue-50 to-purple-50 min-h-screen">
    <div className="container mx-auto px-4 py-20 text-center">
      <h1 className="text-5xl md:text-6xl font-bold text-gray-900 mb-6">
        Build Your Professional Resume with AI
      </h1>
      <p className="text-xl text-gray-600 mb-8">
        Create stunning resumes, portfolios, and cover letters in minutes
      </p>
      <div className="flex justify-center gap-4">
        <a
          href="/login"
          className="px-8 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 font-semibold transition"
        >
          Sign In
        </a>
        <a
          href="/register"
          className="px-8 py-3 bg-white border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 font-semibold transition"
        >
          Get Started
        </a>
      </div>
    </div>
  </div>
);


// Protected Route Component
const ProtectedRoute = ({ children }) => {
  const { user } = useApp();
  return user ? children : <Navigate to="/login" />;
};

// Main App Component
function AppContent() {
  return (
    <Router>
      <Header />
      <main className="bg-gray-50 min-h-screen">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/login" element={<Login />} />
          <Route
            path="/dashboard"
            element={
              <ProtectedRoute>
                <Dashboard />
              </ProtectedRoute>
            }
          />
          <Route
            path="/resume"
            element={
              <ProtectedRoute>
                <Resume />
              </ProtectedRoute>
            }
          />
        </Routes>
      </main>
      <Toaster position="top-right" />
    </Router>
  );
}

function App() {
  return (
    <AppProvider>
      <AppContent />
    </AppProvider>
  );
}

export default App;
