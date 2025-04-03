import { useEffect, useState } from 'react';
import { Container, Paper, Typography, Button, Box, CircularProgress, Alert } from '@mui/material';
import { useNavigate, useSearchParams, Navigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

function PaymentSuccess() {
  const navigate = useNavigate();
  const { user } = useAuth();
  const [searchParams] = useSearchParams();
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    // Check if we have a session_id in the URL
    const sessionId = searchParams.get('session_id');
    if (!sessionId) {
      setError('Invalid payment session');
    }

    const timer = setTimeout(() => {
      setLoading(false);
    }, 2000);

    return () => clearTimeout(timer);
  }, [searchParams]);

  // Redirect to home if not logged in
  if (!user) {
    return <Navigate to="/" replace />;
  }

  return (
    <Container maxWidth="sm">
      <Box sx={{ mt: 8 }}>
        <Paper elevation={3} sx={{ p: 4, textAlign: 'center' }}>
          {loading ? (
            <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '200px' }}>
              <CircularProgress />
            </Box>
          ) : error ? (
            <>
              <Alert severity="error" sx={{ mb: 3 }}>
                {error}
              </Alert>
              <Button
                variant="contained"
                color="primary"
                onClick={() => navigate('/donate')}
              >
                Return to Donation Page
              </Button>
            </>
          ) : (
            <>
              <Typography variant="h4" component="h1" gutterBottom>
                Thank You for Your Donation!
              </Typography>
              <Typography variant="body1" paragraph>
                Your contribution has been received and will help us provide mental health resources
                and support to those in need.
              </Typography>
              <Box sx={{ mt: 4, display: 'flex', gap: 2, justifyContent: 'center' }}>
                <Button
                  variant="contained"
                  color="primary"
                  onClick={() => navigate('/')}
                >
                  Return to Home
                </Button>
                <Button
                  variant="outlined"
                  color="primary"
                  onClick={() => navigate('/donate')}
                >
                  Make Another Donation
                </Button>
              </Box>
            </>
          )}
        </Paper>
      </Box>
    </Container>
  );
}

export default PaymentSuccess; 