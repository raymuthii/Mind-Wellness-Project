import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  Box,
  Container,
  Grid,
  Paper,
  Typography,
  Avatar,
  Chip,
  Button,
  Divider,
  CircularProgress,
  Alert,
  Rating,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
} from '@mui/material';
import api from '../services/api';
import { useAuth } from '../contexts/AuthContext';

function TherapistProfile() {
  const { id } = useParams();
  const navigate = useNavigate();
  const { user } = useAuth();
  const [therapist, setTherapist] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [bookingDialogOpen, setBookingDialogOpen] = useState(false);
  const [bookingData, setBookingData] = useState({
    date: '',
    time: '',
    duration: 60,
    notes: '',
  });

  useEffect(() => {
    if (!id) {
      setError('No therapist ID provided');
      setLoading(false);
      return;
    }
    fetchTherapist();
  }, [id]);

  const fetchTherapist = async () => {
    try {
      const response = await api.get(`/therapist/${id}`);
      if (response.data) {
        setTherapist(response.data);
        setError('');
      } else {
        setError('Failed to load therapist data');
      }
    } catch (err) {
      console.error('Error fetching therapist:', err);
      setError(err.response?.data?.error || 'Failed to load therapist profile');
    } finally {
      setLoading(false);
    }
  };

  const handleBookingSubmit = async () => {
    try {
      // TODO: Implement booking logic
      console.log('Booking data:', bookingData);
      setBookingDialogOpen(false);
      // Show success message
    } catch (err) {
      console.error('Error creating booking:', err);
      setError('Failed to create booking');
    }
  };

  if (loading) {
    return (
      <Box
        display="flex"
        justifyContent="center"
        alignItems="center"
        minHeight="80vh"
      >
        <CircularProgress />
      </Box>
    );
  }

  if (error || !therapist) {
    return (
      <Container maxWidth="lg">
        <Box sx={{ mt: 4 }}>
          <Alert severity="error">{error || 'Therapist not found'}</Alert>
          <Button
            variant="contained"
            onClick={() => navigate('/find-therapist')}
            sx={{ mt: 2 }}
          >
            Back to Therapists
          </Button>
        </Box>
      </Container>
    );
  }

  return (
    <Container maxWidth="lg">
      <Box sx={{ mt: 4, mb: 6 }}>
        <Grid container spacing={4}>
          {/* Left Column - Profile Info */}
          <Grid item xs={12} md={4}>
            <Paper elevation={3} sx={{ p: 3 }}>
              <Box sx={{ textAlign: 'center', mb: 3 }}>
                <Avatar
                  src={therapist.profile_image}
                  sx={{ width: 150, height: 150, mx: 'auto', mb: 2 }}
                />
                <Typography variant="h5" component="h1" gutterBottom>
                  {therapist.name}
                </Typography>
                <Typography
                  variant="subtitle1"
                  color="text.secondary"
                  gutterBottom
                >
                  {therapist.specialization}
                </Typography>
                <Rating value={4.5} precision={0.5} readOnly />
                <Typography variant="body2" color="text.secondary">
                  (24 reviews)
                </Typography>
              </Box>

              <Divider sx={{ my: 2 }} />

              <Box sx={{ mb: 3 }}>
                <Typography variant="subtitle2" gutterBottom>
                  Hourly Rate
                </Typography>
                <Typography variant="h6" color="primary">
                  ${therapist.hourly_rate}/hour
                </Typography>
              </Box>

              <Box sx={{ mb: 3 }}>
                <Typography variant="subtitle2" gutterBottom>
                  Experience
                </Typography>
                <Typography variant="body1">
                  {therapist.years_of_experience} years
                </Typography>
              </Box>

              <Box sx={{ mb: 3 }}>
                <Typography variant="subtitle2" gutterBottom>
                  Languages
                </Typography>
                <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
                  {therapist.languages.map((lang) => (
                    <Chip key={lang} label={lang} size="small" />
                  ))}
                </Box>
              </Box>

              <Button
                variant="contained"
                fullWidth
                onClick={() => setBookingDialogOpen(true)}
                disabled={!user}
              >
                {user ? 'Book Session' : 'Login to Book'}
              </Button>
            </Paper>
          </Grid>

          {/* Right Column - Detailed Info */}
          <Grid item xs={12} md={8}>
            <Paper elevation={3} sx={{ p: 3, mb: 3 }}>
              <Typography variant="h6" gutterBottom>
                About Me
              </Typography>
              <Typography variant="body1" paragraph>
                {therapist.bio}
              </Typography>

              <Typography variant="h6" gutterBottom sx={{ mt: 3 }}>
                Qualifications
              </Typography>
              <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
                {therapist.qualifications.map((qual, index) => (
                  <Chip key={index} label={qual} />
                ))}
              </Box>

              <Typography variant="h6" gutterBottom sx={{ mt: 3 }}>
                Availability
              </Typography>
              <Typography variant="body1">
                {therapist.availability
                  ? 'Available for sessions'
                  : 'Please contact for availability'}
              </Typography>
            </Paper>

            {/* Reviews Section */}
            <Paper elevation={3} sx={{ p: 3 }}>
              <Typography variant="h6" gutterBottom>
                Reviews
              </Typography>
              {/* TODO: Add reviews component */}
              <Typography variant="body1" color="text.secondary">
                No reviews yet.
              </Typography>
            </Paper>
          </Grid>
        </Grid>

        {/* Booking Dialog */}
        <Dialog
          open={bookingDialogOpen}
          onClose={() => setBookingDialogOpen(false)}
          maxWidth="sm"
          fullWidth
        >
          <DialogTitle>Book a Session</DialogTitle>
          <DialogContent>
            <Box sx={{ mt: 2 }}>
              <Grid container spacing={2}>
                <Grid item xs={12}>
                  <TextField
                    fullWidth
                    type="date"
                    label="Date"
                    value={bookingData.date}
                    onChange={(e) =>
                      setBookingData({ ...bookingData, date: e.target.value })
                    }
                    InputLabelProps={{ shrink: true }}
                  />
                </Grid>
                <Grid item xs={12}>
                  <TextField
                    fullWidth
                    type="time"
                    label="Time"
                    value={bookingData.time}
                    onChange={(e) =>
                      setBookingData({ ...bookingData, time: e.target.value })
                    }
                    InputLabelProps={{ shrink: true }}
                  />
                </Grid>
                <Grid item xs={12}>
                  <FormControl fullWidth>
                    <InputLabel>Session Duration</InputLabel>
                    <Select
                      value={bookingData.duration}
                      onChange={(e) =>
                        setBookingData({
                          ...bookingData,
                          duration: e.target.value,
                        })
                      }
                      label="Session Duration"
                    >
                      <MenuItem value={30}>30 minutes</MenuItem>
                      <MenuItem value={60}>1 hour</MenuItem>
                      <MenuItem value={90}>1.5 hours</MenuItem>
                      <MenuItem value={120}>2 hours</MenuItem>
                    </Select>
                  </FormControl>
                </Grid>
                <Grid item xs={12}>
                  <TextField
                    fullWidth
                    multiline
                    rows={4}
                    label="Additional Notes"
                    value={bookingData.notes}
                    onChange={(e) =>
                      setBookingData({ ...bookingData, notes: e.target.value })
                    }
                  />
                </Grid>
              </Grid>
            </Box>
          </DialogContent>
          <DialogActions>
            <Button onClick={() => setBookingDialogOpen(false)}>Cancel</Button>
            <Button
              variant="contained"
              onClick={handleBookingSubmit}
              disabled={!bookingData.date || !bookingData.time}
            >
              Confirm Booking
            </Button>
          </DialogActions>
        </Dialog>
      </Box>
    </Container>
  );
}

export default TherapistProfile; 