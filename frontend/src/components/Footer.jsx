import { Box, Container, Grid, Typography, Link } from '@mui/material'

function Footer() {
  return (
    <Box
      component="footer"
      sx={{
        py: 3,
        px: 2,
        mt: 'auto',
        backgroundColor: (theme) =>
          theme.palette.mode === 'light'
            ? theme.palette.grey[200]
            : theme.palette.grey[800],
      }}
    >
      <Container maxWidth="lg">
        <Grid container spacing={4}>
          <Grid item xs={12} sm={4}>
            <Typography variant="h6" color="text.primary" gutterBottom>
              About Us
            </Typography>
            <Typography variant="body2" color="text.secondary">
              Mind Wellness is dedicated to providing mental health resources and support
              to those in need. We believe in making mental health care accessible to everyone.
            </Typography>
          </Grid>
          <Grid item xs={12} sm={4}>
            <Typography variant="h6" color="text.primary" gutterBottom>
              Quick Links
            </Typography>
            <Box>
              <Link href="/resources" color="inherit" display="block" sx={{ mb: 1 }}>
                Resources
              </Link>
              <Link href="/donate" color="inherit" display="block" sx={{ mb: 1 }}>
                Donate
              </Link>
              <Link href="/contact" color="inherit" display="block" sx={{ mb: 1 }}>
                Contact Us
              </Link>
            </Box>
          </Grid>
          <Grid item xs={12} sm={4}>
            <Typography variant="h6" color="text.primary" gutterBottom>
              Contact Info
            </Typography>
            <Typography variant="body2" color="text.secondary">
              Email: support@mindwellness.com
              <br />
              Phone: (555) 123-4567
              <br />
              Address: 123 Mental Health Ave, Suite 100
              <br />
              City, State 12345
            </Typography>
          </Grid>
        </Grid>
        <Box sx={{ mt: 4, textAlign: 'center' }}>
          <Typography variant="body2" color="text.secondary">
            © {new Date().getFullYear()} Mind Wellness. All rights reserved.
          </Typography>
        </Box>
      </Container>
    </Box>
  )
}

export default Footer 