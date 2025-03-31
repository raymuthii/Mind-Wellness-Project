import React, { useState } from 'react';
import { useDispatch } from 'react-redux';
import { login } from '../redux/authSlice';
import { useNavigate } from 'react-router-dom';

const LoginPage = () => {
  const [fullName, setFullName] = useState('');
  const [userName, setUserName] = useState('');
  const [contact, setContact] = useState('email');
  const [password, setPassword] = useState('');
  const [role, setRole] = useState('patient'); // Default to patient for mental health program
  const [loading, setLoading] = useState(false);
  const dispatch = useDispatch();
  const navigate = useNavigate();

  const isValidEmail = (email) =>
    /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/.test(email);
  const isValidPhoneNumber = (phone) => /^\+(\d{12})$/.test(phone);

  const handleLogin = () => {
    if (!fullName || !userName || !password || !role) {
      alert('Please enter all required fields.');
      return;
    }

    if (contact === 'email' && !isValidEmail(userName)) {
      alert('Please enter a valid email address.');
      return;
    }

    if (contact === 'phone' && !isValidPhoneNumber(userName)) {
      alert('Please enter a valid phone number starting with "+" and 12 digits.');
      return;
    }

    setLoading(true); // Start loading
    dispatch(login({ user: userName, contact, role, password, fullName }));
    alert('Login successful! Welcome to Mind Wellness.');
    navigate(`/home/${role}`);
  };

  return (
    <div style={styles.container}>
      <div style={styles.formContainer}>
        <h2 style={styles.heading}>Log In to Your Account</h2>
        <input
          type="text"
          placeholder="Full Name"
          value={fullName}
          onChange={(e) => setFullName(e.target.value)}
          style={styles.input}
        />
        
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
          placeholder={contact === 'email' ? 'Email Address' : 'Phone Number'}
          value={userName}
          onChange={(e) => setUserName(e.target.value)}
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
          <option value="admin">Admin</option>
        </select>
        
        <button onClick={handleLogin} style={styles.button} disabled={loading}>
          {loading ? 'Logging in...' : 'Log In'}
        </button>
        
        <p style={styles.registerPrompt}>
          Don't have an account? <a href="/signup" style={styles.link}>Sign up</a>
        </p>

        <p style={styles.forgotPassword}>
          <a href="/forgot-password" style={styles.link}>Forgot Password?</a>
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
  select: {
    width: '100%',
    padding: '12px',
    marginBottom: '15px',
    fontSize: '1rem',
    borderRadius: '8px',
    border: '1px solid #ddd',
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
  forgotPassword: {
    marginTop: '10px',
    fontSize: '0.9rem',
    color: '#333',
  },
};

export default LoginPage;
