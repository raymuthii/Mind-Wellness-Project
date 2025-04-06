import React from 'react';
import { Link as RouterLink, useNavigate } from 'react-router-dom';
import {
  AppBar,
  Toolbar,
  Typography,
  Button,
  Box,
  Container,
} from '@mui/material';
import { useAuth } from '../contexts/AuthContext';

const Navigation = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = async () => {
    try {
      await logout();
      navigate('/');
    } catch (error) {
      console.error('Error logging out:', error);
    }
  };

  // Determine if the home link should navigate to a role-specific page
  const getHomeLink = () => {
    if (user?.role === 'therapist') {
      return '/therapist/appointments';
    }
    return '/';
  };

  return (
    <AppBar position="static">
      <Container maxWidth="lg">
        <Toolbar disableGutters>
          <Typography
            variant="h6"
            component={RouterLink}
            to={getHomeLink()}
            sx={{
              flexGrow: 1,
              textDecoration: 'none',
              color: 'inherit',
            }}
          >
            Mind Wellness
          </Typography>

          <Box sx={{ display: 'flex', gap: 2 }}>
            {user ? (
              <>
                {user.role === 'therapist' ? (
                  <>
                    <Button
                      color="inherit"
                      component={RouterLink}
                      to="/therapist/appointments"
                    >
                      My Appointments
                    </Button>
                    <Button
                      color="inherit"
                      component={RouterLink}
                      to="/therapist/profile"
                    >
                      My Profile
                    </Button>
                  </>
                ) : (
                  <>
                    <Button
                      color="inherit"
                      component={RouterLink}
                      to="/find-therapist"
                    >
                      Find Therapist
                    </Button>
                    <Button
                      color="inherit"
                      component={RouterLink}
                      to="/my-appointments"
                    >
                      My Appointments
                    </Button>
                    <Button
                      color="inherit"
                      component={RouterLink}
                      to="/donate"
                    >
                      Make a Donation
                    </Button>
                  </>
                )}
                <Button color="inherit" onClick={handleLogout}>
                  Logout
                </Button>
              </>
            ) : (
              <>
                <Button
                  color="inherit"
                  component={RouterLink}
                  to="/login"
                >
                  Login
                </Button>
                <Button
                  color="inherit"
                  component={RouterLink}
                  to="/register"
                >
                  Register
                </Button>
                <Button
                  color="inherit"
                  component={RouterLink}
                  to="/therapist/register"
                >
                  Join as Therapist
                </Button>
              </>
            )}
          </Box>
        </Toolbar>
      </Container>
    </AppBar>
  );
};

export default Navigation; 