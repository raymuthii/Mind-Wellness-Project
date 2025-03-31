import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const ForgotPasswordPage = () => {
  const [contact, setContact] = useState('email'); // Default to email
  const [contactDetails, setContactDetails] = useState('');
  const navigate = useNavigate();

  const handleSubmit = () => {
    if (!contactDetails) {
      alert('Please enter your contact details.');
      return;
    }

    // Simulate sending password reset instructions
    alert(`Password reset instructions sent to ${contactDetails}. Please check your inbox to reconnect with your mental health support network.`);

    // Redirect to login page after submission
    navigate('/login');
  };

  return (
    <div style={styles.container}>
      <div style={styles.formContainer}>
        <h2 style={styles.heading}>Reset Your Account Password</h2>
        
        <div style={styles.radioGroup}>
          <label style={styles.radioLabel}>
            <input
              type="radio"
              value="email"
              checked={contact === 'email'}
              onChange={() => setContact('email')}
              style={styles.radioButton}
            />
            Email
          </label>
          <label style={styles.radioLabel}>
            <input
              type="radio"
              value="phone"
              checked={contact === 'phone'}
              onChange={() => setContact('phone')}
              style={styles.radioButton}
            />
            Phone Number
          </label>
        </div>

        <input
          type={contact === 'email' ? 'email' : 'tel'}
          placeholder={contact === 'email' ? 'Enter your email' : 'Enter your phone number'}
          value={contactDetails}
          onChange={(e) => setContactDetails(e.target.value)}
          style={styles.input}
        />

        <button onClick={handleSubmit} style={styles.button}>Submit</button>

        <p style={styles.registerPrompt}>
          Remember your password? <a href="/login" style={styles.link}>Login</a>
        </p>
      </div>
    </div>
  );
};

const styles = {
  container: {
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
    minHeight: '100vh',
    background: 'linear-gradient(to right, #00c6ff, #0072ff)',
  },
  formContainer: {
    backgroundColor: 'white',
    padding: '40px',
    borderRadius: '10px',
    boxShadow: '0 8px 16px rgba(0, 0, 0, 0.1)',
    width: '100%',
    maxWidth: '400px',
    textAlign: 'center',
  },
  heading: {
    fontSize: '2rem',
    fontWeight: '600',
    marginBottom: '20px',
    color: '#333',
  },
  radioGroup: {
    display: 'flex',
    justifyContent: 'center',
    marginBottom: '20px',
  },
  radioLabel: {
    marginRight: '15px',
    fontSize: '1rem',
    color: '#333',
  },
  radioButton: {
    marginRight: '5px',
  },
  input: {
    width: '100%',
    padding: '12px',
    marginBottom: '15px',
    fontSize: '1rem',
    borderRadius: '8px',
    border: '1px solid #ddd',
    boxSizing: 'border-box',
  },
  button: {
    backgroundColor: '#0072ff',
    color: 'white',
    fontSize: '1.2rem',
    padding: '12px',
    border: 'none',
    borderRadius: '8px',
    cursor: 'pointer',
    width: '100%',
  },
  registerPrompt: {
    marginTop: '20px',
    fontSize: '0.9rem',
    color: '#333',
  },
  link: {
    color: '#0072ff',
    textDecoration: 'none',
  },
};

export default ForgotPasswordPage;
