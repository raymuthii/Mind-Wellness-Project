import React, { useState } from 'react';
import { FaFacebook, FaTwitter, FaInstagram, FaLinkedin, FaYoutube } from 'react-icons/fa';

const ContactPage = () => {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    phone: '',
    concern: '',
    message: '',
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prevData) => ({
      ...prevData,
      [name]: value,
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    // Handle form submission logic here (e.g., sending to a backend)
    alert('Your message has been sent! A mental health professional will reach out to you shortly.');
  };

  return (
    <div style={styles.container}>
      <div style={styles.formContainer}>
        <form onSubmit={handleSubmit}>
          <label htmlFor="name" style={styles.label}>Name</label>
          <input
            type="text"
            id="name"
            name="name"
            value={formData.name}
            onChange={handleChange}
            style={styles.input}
            placeholder="Enter your full name"
          />

          <label htmlFor="email" style={styles.label}>Email</label>
          <input
            type="email"
            id="email"
            name="email"
            value={formData.email}
            onChange={handleChange}
            style={styles.input}
            placeholder="Enter your email"
          />

          <label htmlFor="phone" style={styles.label}>Phone</label>
          <input
            type="tel"
            id="phone"
            name="phone"
            value={formData.phone}
            onChange={handleChange}
            style={styles.input}
            placeholder="Enter your phone number"
          />

          <label htmlFor="concern" style={styles.label}>How can we help you?</label>
          <input
            type="text"
            id="concern"
            name="concern"
            value={formData.concern}
            onChange={handleChange}
            style={styles.input}
            placeholder="Briefly describe your concern"
          />

          <label htmlFor="message" style={styles.label}>Additional Details</label>
          <textarea
            id="message"
            name="message"
            value={formData.message}
            onChange={handleChange}
            placeholder="Provide any additional information that might help us connect you with the right professional..."
            style={styles.textarea}
          ></textarea>

          <button type="submit" style={styles.button}>Send Message</button>
        </form>
      </div>
      <div style={styles.ctaContainer}>
        <h2 style={styles.ctaTitle}>Reach Out for Support</h2>
        <p>Your well-being matters. We’re here to connect you with experienced mental health professionals who can help.</p>
        <div style={styles.socialMediaIcons}>
          <button 
            style={styles.socialIcon} 
            onClick={() => window.location.href = 'https://facebook.com'}
          >
            <FaFacebook size={30} />
            <span style={styles.iconText}>Facebook</span>
          </button>
          <button 
            style={styles.socialIcon} 
            onClick={() => window.location.href = 'https://twitter.com'}
          >
            <FaTwitter size={30} />
            <span style={styles.iconText}>Twitter</span>
          </button>
          <button 
            style={styles.socialIcon} 
            onClick={() => window.location.href = 'https://instagram.com'}
          >
            <FaInstagram size={30} />
            <span style={styles.iconText}>Instagram</span>
          </button>
          <button 
            style={styles.socialIcon} 
            onClick={() => window.location.href = 'https://linkedin.com'}
          >
            <FaLinkedin size={30} />
            <span style={styles.iconText}>LinkedIn</span>
          </button>
          <button 
            style={styles.socialIcon} 
            onClick={() => window.location.href = 'https://youtube.com'}
          >
            <FaYoutube size={30} />
            <span style={styles.iconText}>YouTube</span>
          </button>
        </div>
      </div>
    </div>
  );
};

// Updated styles with a calming, supportive theme
const styles = {
  container: {
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
    minHeight: '100vh',
    background: 'linear-gradient(to right, #a1c4fd, #c2e9fb)',
    color: '#333',
    padding: '20px',
  },
  formContainer: {
    backgroundColor: '#ffffff',
    padding: '30px',
    borderRadius: '8px',
    marginRight: '20px',
    width: '500px',
    boxShadow: '0 8px 16px rgba(0, 0, 0, 0.1)',
  },
  label: {
    fontSize: '18px',
    fontWeight: 'bold',
    color: '#555',
    marginBottom: '8px',
    display: 'block',
    transition: 'color 0.3s ease',
  },
  input: {
    width: '100%',
    padding: '10px',
    margin: '10px 0',
    border: '1px solid #ccc',
    borderRadius: '4px',
    fontSize: '16px',
  },
  textarea: {
    width: '100%',
    padding: '10px',
    margin: '10px 0',
    border: '1px solid #ccc',
    borderRadius: '4px',
    minHeight: '100px',
    fontSize: '16px',
  },
  button: {
    backgroundColor: '#0072ff',
    color: '#ffffff',
    padding: '10px 20px',
    border: 'none',
    borderRadius: '4px',
    cursor: 'pointer',
    fontWeight: 'bold',
    letterSpacing: '1px',
    fontSize: '16px',
    marginTop: '10px',
  },
  ctaContainer: {
    maxWidth: '300px',
    padding: '20px',
    color: '#333',
  },
  ctaTitle: {
    fontSize: '24px',
    fontWeight: '700',
    marginBottom: '15px',
    color: '#0072ff',
    textTransform: 'uppercase',
  },
  socialMediaIcons: {
    display: 'flex',
    flexDirection: 'column',
    gap: '10px',
    marginTop: '20px',
  },
  socialIcon: {
    display: 'flex',
    alignItems: 'center',
    background: 'transparent',
    border: 'none',
    color: '#0072ff',
    fontSize: '18px',
    cursor: 'pointer',
    textDecoration: 'none',
    transition: 'transform 0.3s ease',
  },
  iconText: {
    marginLeft: '10px',
    fontSize: '16px',
    fontWeight: 'bold',
  },
};

export default ContactPage;
