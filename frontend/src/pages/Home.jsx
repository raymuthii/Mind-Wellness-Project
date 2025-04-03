import { useNavigate } from 'react-router-dom'
import {
  Box,
  Button,
  Container,
  Typography,
  Grid,
  Card,
  CardContent,
  CardMedia,
} from '@mui/material'
import { useAuth } from '../contexts/AuthContext'

function Home() {
  const navigate = useNavigate()
  const { user } = useAuth()

  const features = [
    {
      title: 'Mental Health Resources',
      description: 'Access a comprehensive collection of articles, guides, and tools to support your mental well-being.',
      image: 'https://source.unsplash.com/random/800x600/?mindfulness',
    },
    {
      title: 'Professional Support',
      description: 'Connect with licensed mental health professionals for personalized guidance and support.',
      image: 'https://source.unsplash.com/random/800x600/?therapy',
    },
    {
      title: 'Community',
      description: 'Join a supportive community of individuals who understand what you\'re going through.',
      image: 'https://source.unsplash.com/random/800x600/?community',
    },
  ]

  return (
    <Box>
      {/* Hero Section */}
      <Box
        sx={{
          bgcolor: 'primary.main',
          color: 'white',
          py: 8,
          mb: 6,
        }}
      >
        <Container maxWidth="md">
          <Typography variant="h2" component="h1" gutterBottom align="center">
            Your Mental Health Matters
          </Typography>
          <Typography variant="h5" align="center" paragraph>
            Access professional support, resources, and a community that cares about your well-being.
          </Typography>
          <Box sx={{ display: 'flex', justifyContent: 'center', gap: 2, mt: 4 }}>
            {!user ? (
              <>
                <Button
                  variant="contained"
                  color="secondary"
                  size="large"
                  onClick={() => navigate('/register')}
                >
                  Get Started
                </Button>
                <Button
                  variant="outlined"
                  color="inherit"
                  size="large"
                  onClick={() => navigate('/login')}
                >
                  Log In
                </Button>
              </>
            ) : (
              <Button
                variant="contained"
                color="secondary"
                size="large"
                onClick={() => navigate('/donate')}
              >
                Make a Donation
              </Button>
            )}
          </Box>
        </Container>
      </Box>

      {/* Features Section */}
      <Container maxWidth="lg" sx={{ mb: 8 }}>
        <Typography variant="h3" component="h2" gutterBottom align="center">
          How We Can Help
        </Typography>
        <Grid container spacing={4} sx={{ mt: 2 }}>
          {features.map((feature) => (
            <Grid item xs={12} md={4} key={feature.title}>
              <Card sx={{ height: '100%' }}>
                <CardMedia
                  component="img"
                  height="200"
                  image={feature.image}
                  alt={feature.title}
                />
                <CardContent>
                  <Typography gutterBottom variant="h5" component="h3">
                    {feature.title}
                  </Typography>
                  <Typography variant="body1" color="text.secondary">
                    {feature.description}
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>
      </Container>

      {/* Call to Action */}
      <Box sx={{ bgcolor: 'grey.100', py: 8 }}>
        <Container maxWidth="md">
          <Typography variant="h4" component="h2" gutterBottom align="center">
            Ready to Take the First Step?
          </Typography>
          <Typography variant="body1" align="center" paragraph>
            Join our community and start your journey towards better mental health today.
          </Typography>
          <Box sx={{ display: 'flex', justifyContent: 'center', mt: 4 }}>
            <Button
              variant="contained"
              color="primary"
              size="large"
              onClick={() => navigate('/login')}
            >
              Get Started
            </Button>
          </Box>
        </Container>
      </Box>
    </Box>
  )
}

export default Home 