import { createSlice } from '@reduxjs/toolkit';

const authSlice = createSlice({
  name: 'auth',
  initialState: {
    user: null,               // Stores user details
    isAuthenticated: false,   // Whether the user is logged in
    role: '',                 // User role ('patient', 'provider', 'admin')
  },
  reducers: {
    login: (state, action) => {
      state.user = action.payload.user;
      state.isAuthenticated = true;
      state.role = action.payload.role;
    },
    logout: (state) => {
      state.user = null;
      state.isAuthenticated = false;
      state.role = '';
    },
  },
});

export const { login, logout } = authSlice.actions;
export default authSlice.reducer;
