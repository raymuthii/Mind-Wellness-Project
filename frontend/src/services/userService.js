import api from './api';

const userService = {
  // Authenticate user and retrieve JWT token
  login: async (credentials) => {
    try {
      const response = await api.post('/auth/login', credentials);
      return response.data;
    } catch (error) {
      throw error.response.data;
    }
  },

  // Register a new user
  register: async (userData) => {
    try {
      const response = await api.post('/auth/register', userData);
      return response.data;
    } catch (error) {
      throw error.response.data;
    }
  },

  // Get the profile of the currently authenticated user
  getProfile: async () => {
    try {
      const response = await api.get('/users/profile');
      return response.data;
    } catch (error) {
      throw error.response.data;
    }
  },

  // Update the profile of the currently authenticated user
  updateProfile: async (userData) => {
    try {
      const response = await api.put('/users/profile', userData);
      return response.data;
    } catch (error) {
      throw error.response.data;
    }
  }
};

export default userService;
