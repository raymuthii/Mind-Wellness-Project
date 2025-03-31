import { createSlice } from '@reduxjs/toolkit';

const mentalHealthSlice = createSlice({
  name: 'mentalHealth',
  initialState: {
    providers: [],              // List of approved mental health providers
    donors: [],                 // List of donors
    totalDonations: 0,
    testimonials: [],           // List of patient testimonials
    inventory: [],
    successStories: {},         // Success stories associated with each provider
    providerApplications: [],   // Track provider applications
  },
  reducers: {
    setProviderDetails: (state, action) => {
      // Add a new provider application with pending status
      state.providerApplications.push({ ...action.payload, status: 'pending' });
    },
    approveProvider: (state, action) => {
      const providerId = action.payload;
      const index = state.providerApplications.findIndex(p => p.id === providerId);
      if (index !== -1) {
        const provider = state.providerApplications[index];
        provider.status = 'approved';
        state.providers.push(provider);
        state.providerApplications.splice(index, 1);
      }
    },
    rejectProvider: (state, action) => {
      const providerId = action.payload;
      const index = state.providerApplications.findIndex(p => p.id === providerId);
      if (index !== -1) {
        state.providerApplications[index].status = 'rejected';
      }
    },
    deleteProvider: (state, action) => {
      const providerId = action.payload;
      state.providers = state.providers.filter(p => p.id !== providerId);
      state.providerApplications = state.providerApplications.filter(p => p.id !== providerId);
    },
    setDonors: (state, action) => {
      state.donors = action.payload;
    },
    setTotalDonations: (state, action) => {
      state.totalDonations = action.payload;
    },
    setInventory: (state, action) => {
      state.inventory = action.payload;
    },
    addTestimonial: (state, action) => {
      state.testimonials.push(action.payload);
    },
    addSuccessStory: (state, action) => {
      const { providerId, title, content } = action.payload;
      if (!state.successStories[providerId]) {
        state.successStories[providerId] = [];
      }
      state.successStories[providerId].push({ title, content });
    },
  },
});

export const {
  setProviderDetails,
  approveProvider,
  rejectProvider,
  deleteProvider,
  setDonors,
  setTotalDonations,
  setInventory,
  addTestimonial,
  addSuccessStory,
} = mentalHealthSlice.actions;

export default mentalHealthSlice.reducer;
