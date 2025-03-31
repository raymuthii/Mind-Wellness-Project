import { createSlice } from '@reduxjs/toolkit';

const initialState = {
  selectedCampaign: null,           // The mental health support campaign selected by the donor
  donationAmount: 0,
  recurring: false,
  anonymity: true,
  userName: '',
  donationHistory: [],              // Tracks all donations made
  donationsByCampaign: {},          // Tracks donations by campaign ID
};

const donationSlice = createSlice({
  name: 'donation',
  initialState,
  reducers: {
    setSelectedCampaign: (state, action) => {
      state.selectedCampaign = action.payload;
    },
    setDonationAmount: (state, action) => {
      state.donationAmount = action.payload;
    },
    setRecurring: (state, action) => {
      state.recurring = action.payload;
    },
    setAnonymity: (state, action) => {
      state.anonymity = action.payload;
    },
    setUserName: (state, action) => {
      state.userName = action.payload;
    },
    addDonation: (state, action) => {
      const donationData = action.payload;
      // Add donation to global history
      state.donationHistory.push(donationData);

      // Use campaignTitle as the campaign identifier
      const campaignId = donationData.campaignTitle;
      if (!state.donationsByCampaign[campaignId]) {
        state.donationsByCampaign[campaignId] = [];
      }
      state.donationsByCampaign[campaignId].push(donationData);
    },
  },
});

export const {
  setSelectedCampaign,
  setDonationAmount,
  setRecurring,
  setAnonymity,
  setUserName,
  addDonation,
} = donationSlice.actions;

export default donationSlice.reducer;
