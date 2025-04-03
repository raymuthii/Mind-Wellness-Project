# Mind Wellness Frontend

This is the frontend application for the Mind Wellness donation platform. It's built with React, TypeScript, and Material-UI.

## Features

- Modern, responsive design
- User authentication
- Secure donation processing with Stripe
- Real-time payment status updates
- Mobile-friendly interface

## Prerequisites

- Node.js (v14 or higher)
- npm (v6 or higher)

## Getting Started

1. Install dependencies:
   ```bash
   npm install
   ```

2. Create a `.env` file in the root directory with the following variables:
   ```
   VITE_API_URL=http://localhost:8000/api/v1
   VITE_STRIPE_PUBLIC_KEY=your_stripe_public_key
   ```

3. Start the development server:
   ```bash
   npm run dev
   ```

4. Open [http://localhost:5173](http://localhost:5173) in your browser.

## Project Structure

```
src/
├── components/     # Reusable UI components
├── contexts/      # React contexts for state management
├── hooks/         # Custom React hooks
├── pages/         # Page components
├── services/      # API services
└── utils/         # Utility functions
```

## Available Scripts

- `npm run dev` - Start the development server
- `npm run build` - Build the production version
- `npm run preview` - Preview the production build locally
- `npm run lint` - Run ESLint
- `npm run type-check` - Run TypeScript type checking

## Technologies Used

- React
- TypeScript
- Material-UI
- React Router
- React Query
- Axios
- Stripe.js

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
