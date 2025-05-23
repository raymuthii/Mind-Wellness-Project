import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000/api/v1',
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  },
  withCredentials: true
});

// Add a request interceptor to add the auth token to requests
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    console.error('Request error:', error);
    return Promise.reject(error);
  }
);

// Add a response interceptor to handle errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('Response error:', error.response?.data || error.message);
    
    if (error.response?.status === 401) {
      // Handle unauthorized access
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error.response?.data || error);
  }
);

export const authService = {
  register: async (formData) => {
    try {
      // Determine which endpoint to use based on the role
      const endpoint = formData.role === 'therapist' ? '/therapist/register' : '/auth/register';
      const response = await api.post(endpoint, formData);
      
      if (response.data.access_token) {
        localStorage.setItem('token', response.data.access_token);
      }

      // Get user data from the appropriate response field
      const userData = formData.role === 'therapist' ? response.data.therapist : response.data.user;
      
      // Ensure we have the role
      if (!userData.role) {
        userData.role = formData.role;
      }

      console.log('Registration response:', response.data);
      console.log('User data with role:', userData);

      return {
        user: userData,
        access_token: response.data.access_token
      };
    } catch (error) {
      console.error('Registration error:', error);
      throw error;
    }
  },

  login: async (email, password) => {
    try {
      const response = await api.post('/auth/login', { email, password });
      if (response.data.access_token) {
        localStorage.setItem('token', response.data.access_token);
      }

      const userData = response.data.user;
      
      // If role is missing, get it from /auth/me endpoint
      if (!userData.role) {
        console.log('Role missing from login response, fetching from /auth/me');
        const userDetails = await api.get('/auth/me');
        userData.role = userDetails.data.role;
      }

      console.log('Login response:', response.data);
      console.log('User data with role:', userData);

      return {
        user: userData,
        access_token: response.data.access_token
      };
    } catch (error) {
      console.error('Login error:', error);
      throw error;
    }
  },

  getCurrentUser: async () => {
    try {
      const response = await api.get('/auth/me');
      return response.data;
    } catch (error) {
      console.error('Get current user error:', error);
      throw error;
    }
  },

  logout: () => {
    localStorage.removeItem('token');
  },
};

export const donationService = {
  createDonation: async (amount) => {
    try {
      const response = await api.post('/donation/', { amount });
      if (response.data.checkout_url) {
        return response.data;
      } else {
        throw new Error('No checkout URL received from server');
      }
    } catch (error) {
      console.error('Create donation error:', error);
      throw error.error || error.message || 'Failed to create donation';
    }
  },

  getDonations: async () => {
    try {
      const response = await api.get('/donation/');
      return response.data;
    } catch (error) {
      console.error('Get donations error:', error);
      throw error.error || error.message || 'Failed to fetch donations';
    }
  },
};

export default api; 