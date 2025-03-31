import api from './api';

export const storyService = {
  // Fetch all published success stories
  getStories: async () => {
    return await api.get('/api/success-stories');
  },
  
  // Fetch success stories for a specific provider
  getProviderStories: async (providerId) => {
    return await api.get(`/api/providers/${providerId}/success-stories`);
  },
  
  // Create a new success story
  createStory: async (storyData) => {
    return await api.post('/api/success-stories', storyData);
  },
  
  // Update an existing success story
  updateStory: async (storyId, storyData) => {
    return await api.put(`/api/success-stories/${storyId}`, storyData);
  },
  
  // Delete a success story
  deleteStory: async (storyId) => {
    return await api.delete(`/api/success-stories/${storyId}`);
  }
};

// Export storyService as the default export
export default storyService;
