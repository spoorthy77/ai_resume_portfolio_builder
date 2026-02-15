import React, { createContext, useContext, useState } from 'react';

const AppContext = createContext();

export const AppProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [resume, setResume] = useState(null);

  const loginUser = (userData) => {
    setUser(userData);
    localStorage.setItem('user', JSON.stringify(userData));
  };

  const logoutUser = () => {
    setUser(null);
    setProfile(null);
    localStorage.removeItem('user');
  };

  const updateProfile = (profileData) => {
    setProfile(profileData);
    localStorage.setItem('profile', JSON.stringify(profileData));
  };

  return (
    <AppContext.Provider value={{
      user,
      profile,
      loading,
      resume,
      loginUser,
      logoutUser,
      updateProfile,
      setLoading,
      setResume,
    }}>
      {children}
    </AppContext.Provider>
  );
};

export const useApp = () => {
  const context = useContext(AppContext);
  if (!context) {
    throw new Error('useApp must be used within AppProvider');
  }
  return context;
};
