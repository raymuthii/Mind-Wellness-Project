import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// Vite configuration for the Mind Wellness Donation Platform
export default defineConfig({
  plugins: [react()],
  server: {
    hmr: true,
    watch: {
      usePolling: true,
    },
  },
})
