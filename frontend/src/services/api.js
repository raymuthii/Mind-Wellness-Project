import axios from 'axios';

// Create an Axios instance for the Tender Hands app
const api = axios.create({
  baseURL: 'https://tenderhands-api.com/api', // Replace with your actual API base URL
  timeout: 10000, // Set a timeout for requests
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add authorization token if needed
api.interceptors.request.use(
  (config) => {
    // If you have an authentication token, you can add it here
    const token = localStorage.getItem('token'); // Example: getting token from local storage
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor to handle responses globally
api.interceptors.response.use(
  (response) => {
    // You can handle specific response statuses here if needed
    return response.data; // Return only the data part of the response
  },
  (error) => {
    // Handle errors globally
    if (error.response) {
      // The request was made and the server responded with a status code
      console.error('API Error:', error.response.data);
      return Promise.reject(error.response.data);
    } else if (error.request) {
      // The request was made but no response was received
      console.error('API Error: No response received', error.request);
      return Promise.reject('No response received from the server');
    } else {
      // Something happened in setting up the request that triggered an Error
      console.error('API Error:', error.message);
      return Promise.reject(error.message);
    }
  }
);

export default api;
