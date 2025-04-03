import { useState } from 'react'
import {
  Box,
  Container,
  Typography,
  Grid,
  Card,
  CardContent,
  CardMedia,
  Tabs,
  Tab,
  TextField,
  InputAdornment,
} from '@mui/material'
import SearchIcon from '@mui/icons-material/Search'

function Resources() {
  const [selectedTab, setSelectedTab] = useState(0)
  const [searchQuery, setSearchQuery] = useState('')

  const handleTabChange = (event, newValue) => {
    setSelectedTab(newValue)
  }

  const handleSearchChange = (event) => {
    setSearchQuery(event.target.value)
  }

  const resources = {
    articles: [
      {
        title: 'Understanding Anxiety',
        description: 'Learn about the different types of anxiety and how to manage them effectively.',
        image: '/images/anxiety.jpg',
        category: 'articles',
      },
      {
        title: 'Coping with Depression',
        description: 'Practical strategies and techniques for managing depression in daily life.',
        image: '/images/depression.jpg',
        category: 'articles',
      },
      {
        title: 'Stress Management',
        description: 'Effective ways to reduce and manage stress in your life.',
        image: '/images/stress.jpg',
        category: 'articles',
      },
    ],
    guides: [
      {
        title: 'Mindfulness Meditation Guide',
        description: 'A step-by-step guide to practicing mindfulness meditation.',
        image: '/images/mindfulness.jpg',
        category: 'guides',
      },
      {
        title: 'Self-Care Checklist',
        description: 'A comprehensive checklist for maintaining good mental health.',
        image: '/images/selfcare.jpg',
        category: 'guides',
      },
      {
        title: 'Sleep Hygiene Tips',
        description: 'Learn how to improve your sleep quality with these practical tips.',
        image: '/images/sleep.jpg',
        category: 'guides',
      },
    ],
    tools: [
      {
        title: 'Mood Tracker',
        description: 'Track your daily mood and identify patterns over time.',
        image: '/images/mood-tracker.jpg',
        category: 'tools',
      },
      {
        title: 'Breathing Exercise',
        description: 'Interactive breathing exercise to help reduce stress and anxiety.',
        image: '/images/breathing.jpg',
        category: 'tools',
      },
      {
        title: 'Gratitude Journal',
        description: 'A digital journal to practice gratitude and improve well-being.',
        image: '/images/gratitude.jpg',
        category: 'tools',
      },
    ],
  }

  const filteredResources = Object.values(resources).flat().filter((resource) => {
    const matchesSearch = resource.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      resource.description.toLowerCase().includes(searchQuery.toLowerCase())
    const matchesTab = selectedTab === 0 || resource.category === Object.keys(resources)[selectedTab - 1]
    return matchesSearch && matchesTab
  })

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Typography variant="h4" component="h1" gutterBottom>
        Mental Health Resources
      </Typography>

      <TextField
        fullWidth
        variant="outlined"
        placeholder="Search resources..."
        value={searchQuery}
        onChange={handleSearchChange}
        sx={{ mb: 4 }}
        InputProps={{
          startAdornment: (
            <InputAdornment position="start">
              <SearchIcon />
            </InputAdornment>
          ),
        }}
      />

      <Tabs
        value={selectedTab}
        onChange={handleTabChange}
        sx={{ mb: 4 }}
      >
        <Tab label="All" />
        <Tab label="Articles" />
        <Tab label="Guides" />
        <Tab label="Tools" />
      </Tabs>

      <Grid container spacing={4}>
        {filteredResources.map((resource) => (
          <Grid item xs={12} sm={6} md={4} key={resource.title}>
            <Card sx={{ height: '100%' }}>
              <CardMedia
                component="img"
                height="200"
                image={resource.image}
                alt={resource.title}
              />
              <CardContent>
                <Typography gutterBottom variant="h5" component="h2">
                  {resource.title}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  {resource.description}
                </Typography>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>

      {filteredResources.length === 0 && (
        <Box sx={{ textAlign: 'center', mt: 4 }}>
          <Typography variant="body1" color="text.secondary">
            No resources found matching your search criteria.
          </Typography>
        </Box>
      )}
    </Container>
  )
}

export default Resources 