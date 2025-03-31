import axios from 'axios';

// Create an Axios instance for the Mind Wellness app
const api = axios.create({
  baseURL: 'https://mindwellness-api.com/api', // Replace with your actual API base URL
  timeout: 10000, // Set a timeout for requests
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add the authorization token if available
api.interceptors.request.use(
  (config) => {
    // Retrieve the authentication token from local storage
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor to handle responses globally
api.interceptors.response.use(
  (response) => response.data, // Return only the data part of the response
  (error) => {
    if (error.response) {
      // The server responded with a status code outside the 2xx range
      console.error('API Error:', error.response.data);
      return Promise.reject(error.response.data);
    } else if (error.request) {
      // The request was made but no response was received
      console.error('API Error: No response received', error.request);
      return Promise.reject('No response received from the server');
    } else {
      // An error occurred while setting up the request
      console.error('API Error:', error.message);
      return Promise.reject(error.message);
    }
  }
);

export default api;
