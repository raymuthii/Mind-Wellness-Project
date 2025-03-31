import { configureStore } from '@reduxjs/toolkit';
import authReducer from './authSlice';
import mentalHealthReducer from './mentalHealthSlice';
import donationReducer from './donationSlice';

const store = configureStore({
  reducer: {
    auth: authReducer,
    mentalHealth: mentalHealthReducer,
    donation: donationReducer,
  },
});

export default store;
