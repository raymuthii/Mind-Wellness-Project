import { useState, useEffect } from 'react';
import {
  Box,
  Container,
  Grid,
  Card,
  CardContent,
  Typography,
  TextField,
  MenuItem,
  Chip,
  Avatar,
  Button,
  CircularProgress,
  Alert,
  FormControl,
  InputLabel,
  Select,
  Slider,
} from '@mui/material';
import { useNavigate } from 'react-router-dom';
import api from '../services/api';

const specializations = [
  'Clinical Psychology',
  'Counseling Psychology',
  'Child Psychology',
  'Marriage and Family Therapy',
  'Cognitive Behavioral Therapy',
  'Psychoanalysis',
  'Addiction Therapy',
  'Trauma Therapy',
];

function FindTherapist() {
  const navigate = useNavigate();
  const [therapists, setTherapists] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [filters, setFilters] = useState({
    specialization: '',
    minExperience: 0,
    maxRate: 300,
    language: '',
  });

  const [filteredTherapists, setFilteredTherapists] = useState([]);

  useEffect(() => {
    fetchTherapists();
  }, []);

  useEffect(() => {
    applyFilters();
  }, [filters, therapists]);

  const fetchTherapists = async () => {
    try {
      const response = await api.get('/therapist');
      setTherapists(response.data.therapists || []);
      setFilteredTherapists(response.data.therapists || []);
      setError('');
    } catch (err) {
      console.error('Error fetching therapists:', err);
      setError('Failed to load therapists. Please try again later.');
      setTherapists([]);
      setFilteredTherapists([]);
    } finally {
      setLoading(false);
    }
  };

  const applyFilters = () => {
    let filtered = [...therapists];

    if (filters.specialization) {
      filtered = filtered.filter(
        (t) => t.specialization === filters.specialization
      );
    }

    if (filters.minExperience > 0) {
      filtered = filtered.filter(
        (t) => t.years_of_experience >= filters.minExperience
      );
    }

    if (filters.maxRate < 300) {
      filtered = filtered.filter((t) => t.hourly_rate <= filters.maxRate);
    }

    if (filters.language) {
      filtered = filtered.filter((t) =>
        t.languages.includes(filters.language)
      );
    }

    setFilteredTherapists(filtered);
  };

  const handleFilterChange = (event) => {
    const { name, value } = event.target;
    setFilters((prev) => ({
      ...prev,
      [name]: value,
    }));
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

  return (
    <Container maxWidth="lg">
      <Box sx={{ mt: 4, mb: 6 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          Find a Therapist
        </Typography>

        {error && (
          <Alert severity="error" sx={{ mb: 3 }}>
            {error}
          </Alert>
        )}

        <Grid container spacing={3} sx={{ mb: 4 }}>
          <Grid item xs={12} sm={6} md={3}>
            <FormControl fullWidth>
              <InputLabel>Specialization</InputLabel>
              <Select
                name="specialization"
                value={filters.specialization}
                onChange={handleFilterChange}
                label="Specialization"
              >
                <MenuItem value="">All</MenuItem>
                {specializations.map((spec) => (
                  <MenuItem key={spec} value={spec}>
                    {spec}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
          </Grid>

          <Grid item xs={12} sm={6} md={3}>
            <TextField
              fullWidth
              type="number"
              label="Minimum Years of Experience"
              name="minExperience"
              value={filters.minExperience}
              onChange={handleFilterChange}
              inputProps={{ min: 0 }}
            />
          </Grid>

          <Grid item xs={12} sm={6} md={3}>
            <Box sx={{ width: '100%' }}>
              <Typography gutterBottom>Maximum Hourly Rate ($)</Typography>
              <Slider
                value={filters.maxRate}
                onChange={(_, value) =>
                  handleFilterChange({ target: { name: 'maxRate', value } })
                }
                min={0}
                max={300}
                valueLabelDisplay="auto"
              />
            </Box>
          </Grid>

          <Grid item xs={12} sm={6} md={3}>
            <FormControl fullWidth>
              <InputLabel>Language</InputLabel>
              <Select
                name="language"
                value={filters.language}
                onChange={handleFilterChange}
                label="Language"
              >
                <MenuItem value="">All</MenuItem>
                {['English', 'Spanish', 'French', 'German', 'Chinese', 'Japanese', 'Arabic', 'Hindi'].map(
                  (lang) => (
                    <MenuItem key={lang} value={lang}>
                      {lang}
                    </MenuItem>
                  )
                )}
              </Select>
            </FormControl>
          </Grid>
        </Grid>

        <Grid container spacing={3}>
          {filteredTherapists.map((therapist) => (
            <Grid item xs={12} sm={6} md={4} key={therapist.id}>
              <Card>
                <CardContent>
                  <Box
                    sx={{
                      display: 'flex',
                      alignItems: 'center',
                      mb: 2,
                    }}
                  >
                    <Avatar
                      src={therapist.profile_image || ''}
                      sx={{ width: 56, height: 56, mr: 2 }}
                    />
                    <Box>
                      <Typography variant="h6" component="div">
                        {therapist.name}
                      </Typography>
                      <Typography
                        variant="subtitle2"
                        color="text.secondary"
                      >
                        {therapist.specialization}
                      </Typography>
                    </Box>
                  </Box>

                  <Typography variant="body2" color="text.secondary" paragraph>
                    {therapist.bio?.length > 150
                      ? `${therapist.bio.substring(0, 150)}...`
                      : therapist.bio}
                  </Typography>

                  <Box sx={{ mb: 1.5 }}>
                    <Typography
                      variant="subtitle2"
                      component="span"
                      sx={{ mr: 2 }}
                    >
                      ${therapist.hourly_rate}/hour
                    </Typography>
                    <Typography
                      variant="subtitle2"
                      component="span"
                      color="text.secondary"
                    >
                      {therapist.years_of_experience} years exp.
                    </Typography>
                  </Box>

                  <Box sx={{ mb: 2 }}>
                    {therapist.languages?.slice(0, 3).map((lang) => (
                      <Chip
                        key={lang}
                        label={lang}
                        size="small"
                        sx={{ mr: 0.5, mb: 0.5 }}
                      />
                    ))}
                    {therapist.languages?.length > 3 && (
                      <Chip
                        label={`+${therapist.languages.length - 3}`}
                        size="small"
                        variant="outlined"
                      />
                    )}
                  </Box>

                  <Button
                    variant="contained"
                    fullWidth
                    onClick={() => navigate(`/therapist/${therapist.id}`)}
                  >
                    View Profile
                  </Button>
                </CardContent>
              </Card>
            </Grid>
          ))}

          {filteredTherapists.length === 0 && (
            <Grid item xs={12}>
              <Box
                sx={{
                  textAlign: 'center',
                  py: 4,
                }}
              >
                <Typography variant="h6" color="text.secondary">
                  No therapists found matching your criteria
                </Typography>
              </Box>
            </Grid>
          )}
        </Grid>
      </Box>
    </Container>
  );
}

export default FindTherapist; 