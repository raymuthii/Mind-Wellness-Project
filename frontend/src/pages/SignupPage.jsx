import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const SignupPage = () => {
  const [userName, setUserName] = useState('');
  const [email, setEmail] = useState('');
  const [phoneNumber, setPhoneNumber] = useState('');
  const [password, setPassword] = useState('');
  const [role, setRole] = useState('patient'); // Default to patient
  const navigate = useNavigate();

  // Email validation
  const isValidEmail = (email) => {
    const regex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    return regex.test(email);
  };

  // Phone number validation
  const isValidPhoneNumber = (phone) => {
    const regex = /^\+(\d{12})$/;  // International phone number format: + followed by 12 digits
    return regex.test(phone);
  };

  const handleSignup = () => {
    if (!userName || !email || !phoneNumber || !password || !role) {
      alert('Please fill in all fields.');
      return;
    }

    if (!isValidEmail(email)) {
      alert('Please enter a valid email address (e.g., example@gmail.com).');
      return;
    }

    if (!isValidPhoneNumber(phoneNumber)) {
      alert('Please enter a valid phone number starting with "+" followed by 12 digits.');
      return;
    }

    // Simulate signup success
    alert('Signup successful! Welcome to Mental Health Connect.');
    
    // Redirect to the login page
    navigate('/login');
  };

  return (
    <div style={styles.container}>
      <div style={styles.formContainer}>
        <h2 style={styles.heading}>Mental Health Connect - Sign Up</h2>

        <input
          type="text"
          placeholder="Full Name"
          value={userName}
          onChange={(e) => setUserName(e.target.value)}
          style={styles.input}
        />
        <input
          type="email"
          placeholder="Email Address"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          style={styles.input}
        />
        <input
          type="tel"
          placeholder="Phone Number"
          value={phoneNumber}
          onChange={(e) => setPhoneNumber(e.target.value)}
          style={styles.input}
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          style={styles.input}
        />
        
        <select value={role} onChange={(e) => setRole(e.target.value)} style={styles.select}>
          <option value="patient">Patient</option>
          <option value="doctor">Doctor</option>
        </select>

        <button onClick={handleSignup} style={styles.button}>Sign Up</button>
        
        <p style={styles.loginPrompt}>
          Already have an account? <a href="/login" style={styles.link}>Log in</a>
        </p>
      </div>
    </div>
  );
};

// Updated Styles for a calming mental health theme
const styles = {
  container: {
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
    minHeight: '100vh',
    background: 'linear-gradient(to right, #a1c4fd, #c2e9fb)', // soothing blue gradient
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
    fontSize: '1.8rem',
    fontWeight: '600',
    marginBottom: '20px',
    color: '#333',
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
  select: {
    width: '100%',
    padding: '12px',
    marginBottom: '20px',
    fontSize: '1rem',
    borderRadius: '8px',
    border: '1px solid #ddd',
  },
  button: {
    background: 'linear-gradient(to right, #11998e, #38ef7d)', // calming green gradient
    color: 'white',
    fontSize: '1.2rem',
    padding: '12px',
    border: 'none',
    borderRadius: '8px',
    cursor: 'pointer',
    width: '100%',
  },
  loginPrompt: {
    marginTop: '20px',
    fontSize: '0.9rem',
    color: '#333',
  },
  link: {
    color: '#38ef7d',
    textDecoration: 'none',
  },
};

export default SignupPage;
