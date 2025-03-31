import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import { Provider } from 'react-redux';
import store from './redux/store';
import Navbar from './components/Navbar';
import Home from './pages/HomePage';
import DonationList from './components/DonationList';
import DonateForm from './components/DonateForm';
import DonationHistory from './components/DonationHistory';
import ProviderApplication from './components/ProviderApplication';
import ProviderDashboard from './components/ProviderDashboard';
import AdminDashboard from './components/AdminDashboard';
import SignupPage from './pages/SignupPage';
import LoginPage from './pages/LoginPage';
import ContactPage from './pages/ContactPage';
import About from './pages/about';
import ForgotPasswordPage from './pages/ForgotPasswordPage'; 
import LearnMore from './pages/LearnMore'; 
import ExplorePage from './pages/ExplorePage'; 

import './App.css';

function App() {
  return (
    <Provider store={store}>
      <Router>
        <div className="App">
          <Navbar />
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/donations" element={<DonationList />} />
            <Route path="/donate" element={<DonateForm />} />
            <Route path="/donation-history" element={<DonationHistory />} />
            <Route path="/provider-application" element={<ProviderApplication />} />
            <Route path="/provider-dashboard" element={<ProviderDashboard />} />
            {/* Admin Routes */}
            <Route path="/admin-dashboard" element={<AdminDashboard />} />
            {/* Authentication Routes */}
            <Route path="/signup" element={<SignupPage />} />
            <Route path="/login" element={<LoginPage />} />
            {/* Contact & About Routes */}
            <Route path="/contact" element={<ContactPage />} />
            <Route path="about" element={<About />} />
            <Route path="/forgot-password" element={<ForgotPasswordPage />} />
            <Route path="/learn-more" element={<LearnMore />} />
            <Route path="/explore" element={<ExplorePage />} />
          </Routes>
        </div>
      </Router>
    </Provider>
  );
}

export default App;
