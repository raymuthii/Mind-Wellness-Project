import { useState } from 'react'
import {
  Container,
  Paper,
  TextField,
  Button,
  Typography,
  Box,
  Grid,
  Alert,
} from '@mui/material'
import { useAuth } from '../contexts/AuthContext'
import { donationService } from '../services/api'

function Donate() {
  const { user } = useAuth()
  const [amount, setAmount] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    setLoading(true)

    try {
      // Validate amount
      const numAmount = parseFloat(amount)
      if (isNaN(numAmount) || numAmount <= 0) {
        throw new Error('Please enter a valid positive amount')
      }

      const response = await donationService.createDonation(numAmount)
      
      if (response.checkout_url) {
        window.location.href = response.checkout_url
      } else {
        throw new Error('Failed to create donation. Please try again.')
      }
    } catch (err) {
      console.error('Donation error:', err)
      setError(err.message || 'An error occurred. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  if (!user) {
    return (
      <Container maxWidth="sm">
        <Box sx={{ mt: 8 }}>
          <Paper elevation={3} sx={{ p: 4 }}>
            <Typography variant="h5" gutterBottom align="center">
              Please log in to make a donation
            </Typography>
          </Paper>
        </Box>
      </Container>
    )
  }

  return (
    <Container maxWidth="md">
      <Box sx={{ mt: 8 }}>
        <Paper elevation={3} sx={{ p: 4 }}>
          <Typography variant="h4" component="h1" gutterBottom align="center">
            Make a Donation
          </Typography>
          {error && (
            <Alert severity="error" sx={{ mb: 3 }}>
              {error}
            </Alert>
          )}
          <Grid container spacing={4}>
            <Grid item xs={12} md={6}>
              <Typography variant="h6" gutterBottom>
                Your Impact
              </Typography>
              <Typography paragraph>
                Your donation helps us provide mental health resources and support to those in need.
                Every contribution makes a difference in someone's life.
              </Typography>
            </Grid>
            <Grid item xs={12} md={6}>
              <form onSubmit={handleSubmit}>
                <TextField
                  fullWidth
                  label="Amount ($)"
                  type="number"
                  value={amount}
                  onChange={(e) => {
                    setAmount(e.target.value)
                    setError('')
                  }}
                  margin="normal"
                  required
                  inputProps={{ 
                    min: "0.01",
                    step: "0.01"
                  }}
                  error={!!error}
                  helperText={error || 'Enter the amount you wish to donate'}
                  disabled={loading}
                />
                <Button
                  type="submit"
                  fullWidth
                  variant="contained"
                  color="primary"
                  sx={{ mt: 3 }}
                  disabled={loading || !amount}
                >
                  {loading ? 'Processing...' : 'Donate Now'}
                </Button>
              </form>
            </Grid>
          </Grid>
        </Paper>
      </Box>
    </Container>
  )
}

export default Donate 