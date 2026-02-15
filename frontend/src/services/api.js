import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add auth token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const authAPI = {
  login: (email, password) => api.post('/auth/login', { email, password }),
  register: (name, email, password) => api.post('/auth/register', { name, email, password }),
  logout: () => api.post('/auth/logout'),
};

export const profileAPI = {
  getProfile: () => api.get('/profile'),
  updateProfile: (profileData) => api.put('/profile', profileData),
  deleteProfile: (profileId) => api.delete(`/profile/${profileId}`),
};

export const resumeAPI = {
  generateResume: (profileData, templateName = 'professional', format = 'pdf') =>
    api.post('/ai/generate-resume', { profileData, templateName, format }),
  optimizeResume: (resume) => api.post('/ai/optimize-resume', { resume }),
  exportResume: (resume, format = 'pdf', filename = 'resume') =>
    api.post('/ai/export-resume', { resume, format, filename }, { responseType: 'blob' }),
};

export const portfolioAPI = {
  generatePortfolio: (profileData) => api.post('/ai/generate-portfolio', { profileData }),
  exportPortfolio: (portfolio) => api.post('/ai/export-portfolio', { portfolio }, { responseType: 'blob' }),
};

export const coverLetterAPI = {
  generateCoverLetter: (profileData, jobTitle, company) =>
    api.post('/ai/generate-cover-letter', { profileData, jobTitle, company }),
};

export default api;
