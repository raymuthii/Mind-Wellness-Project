import { useState, useEffect } from 'react'
import {
  Box,
  Container,
  Typography,
  Grid,
  Card,
  CardContent,
  Button,
  List,
  ListItem,
  ListItemText,
  Divider,
} from '@mui/material'
import { useAuth } from '../contexts/AuthContext'
import { donationService } from '../services/api'

function Dashboard() {
  const { user } = useAuth()
  const [donations, setDonations] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    const fetchDonations = async () => {
      try {
        const response = await donationService.getDonations()
        setDonations(response.data)
      } catch (err) {
        setError('Failed to fetch donations')
        console.error('Error fetching donations:', err)
      } finally {
        setLoading(false)
      }
    }

    fetchDonations()
  }, [])

  const totalDonated = donations.reduce((sum, donation) => sum + donation.amount, 0)

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Typography variant="h4" component="h1" gutterBottom>
        Welcome, {user?.firstName}!
      </Typography>

      <Grid container spacing={3}>
        {/* Profile Summary */}
        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Profile Summary
              </Typography>
              <List>
                <ListItem>
                  <ListItemText
                    primary="Name"
                    secondary={`${user?.firstName} ${user?.lastName}`}
                  />
                </ListItem>
                <ListItem>
                  <ListItemText
                    primary="Email"
                    secondary={user?.email}
                  />
                </ListItem>
                <Divider />
                <ListItem>
                  <ListItemText
                    primary="Total Donated"
                    secondary={`$${totalDonated.toFixed(2)}`}
                  />
                </ListItem>
              </List>
            </CardContent>
          </Card>
        </Grid>

        {/* Recent Donations */}
        <Grid item xs={12} md={8}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Recent Donations
              </Typography>
              {loading ? (
                <Typography>Loading donations...</Typography>
              ) : error ? (
                <Typography color="error">{error}</Typography>
              ) : donations.length === 0 ? (
                <Typography>No donations yet.</Typography>
              ) : (
                <List>
                  {donations.map((donation) => (
                    <div key={donation.id}>
                      <ListItem>
                        <ListItemText
                          primary={`$${donation.amount.toFixed(2)}`}
                          secondary={new Date(donation.createdAt).toLocaleDateString()}
                        />
                      </ListItem>
                      <Divider />
                    </div>
                  ))}
                </List>
              )}
              <Box sx={{ mt: 2 }}>
                <Button
                  variant="contained"
                  color="primary"
                  href="/donate"
                >
                  Make a Donation
                </Button>
              </Box>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Container>
  )
}

export default Dashboard 