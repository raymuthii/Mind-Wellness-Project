/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,jsx,ts,tsx}", // Scans all JS/JSX/TS/TSX files in src
  ],
  theme: {
    extend: {
      colors: {
        // Custom color palette matching your UI
        purple: {
          500: '#8B5CF6',
          600: '#7C3AED',
          700: '#6D28D9',
        },
        gray: {
          50: '#F9FAFB',
          100: '#F3F4F6',
          300: '#D1D5DB',
          400: '#9CA3AF',
          500: '#6B7280',
          600: '#4B5563',
          700: '#374151',
          900: '#111827',
        },
        // Optional: Add a calming blue for a mental health theme
        blue: {
          100: '#DBEAFE',
          500: '#3B82F6',
          600: '#2563EB',
        },
      },
      maxWidth: {
        '7xl': '80rem',
      },
    },
  },
  plugins: [
    require('@tailwindcss/forms'), // For better form styling
    require('@tailwindcss/typography'), // For the prose class in StoryCard
  ],
}
