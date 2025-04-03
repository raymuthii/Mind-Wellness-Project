import React from 'react';
import { Routes, Route } from 'react-router-dom';
import { ThemeProvider, createTheme } from '@mui/material';
import CssBaseline from '@mui/material/CssBaseline';
import Navigation from './components/Navigation';
import Home from './pages/Home';
import Login from './pages/Login';
import Register from './pages/Register';
import TherapistRegister from './pages/TherapistRegister';
import FindTherapist from './pages/FindTherapist';
import TherapistProfile from './pages/TherapistProfile';
import TherapistAppointments from './pages/TherapistAppointments';
import PatientAppointments from './pages/PatientAppointments';
import { AuthProvider } from './contexts/AuthContext';
import PrivateRoute from './components/PrivateRoute';

const theme = createTheme({
  palette: {
    primary: {
      main: '#1976d2',
    },
    secondary: {
      main: '#dc004e',
    },
  },
});

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <AuthProvider>
        <Navigation />
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/therapist/register" element={<TherapistRegister />} />
          <Route path="/find-therapist" element={<FindTherapist />} />
          
          {/* Protected Routes */}
          <Route
            path="/therapist/profile"
            element={
              <PrivateRoute allowedRoles={['therapist']}>
                <TherapistProfile />
              </PrivateRoute>
            }
          />
          <Route
            path="/therapist/appointments"
            element={
              <PrivateRoute allowedRoles={['therapist']}>
                <TherapistAppointments />
              </PrivateRoute>
            }
          />
          <Route
            path="/my-appointments"
            element={
              <PrivateRoute allowedRoles={['patient']}>
                <PatientAppointments />
              </PrivateRoute>
            }
          />
        </Routes>
      </AuthProvider>
    </ThemeProvider>
  );
}

export default App; 