import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const ForgotPasswordPage = () => {
  const [contact, setContact] = useState('email'); // Default to email
  const [contactDetails, setContactDetails] = useState('');
  const navigate = useNavigate();

  // Validate email format
  const isValidEmail = (email) => {
    const regex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    return regex.test(email);
  };

  // Validate phone number format (+ followed by 12 digits)
  const isValidPhoneNumber = (phone) => {
    const regex = /^\+\d{12}$/;
    return regex.test(phone);
  };

  const handleSubmit = () => {
    if (!contactDetails) {
      alert('Please enter your contact details.');
      return;
    }

    // Validate based on contact type
    if (contact === 'email' && !isValidEmail(contactDetails)) {
      alert('Please enter a valid email address.');
      return;
    }

    if (contact === 'phone' && !isValidPhoneNumber(contactDetails)) {
      alert('Please enter a valid phone number starting with "+" followed by 12 digits.');
      return;
    }

    // Simulate sending password reset details
    alert(`Password reset instructions sent to ${contactDetails}. Please check your inbox for further steps to reconnect with your account and our mental health support network.`);
    
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
    background: 'linear-gradient(to right, #a1c4fd, #c2e9fb)', // Calming blue gradient
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
    background: 'linear-gradient(to right, #38ef7d, #11998e)', // Calming green gradient
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
    color: '#11998e',
    textDecoration: 'none',
  },
};

export default ForgotPasswordPage;
