import React from 'react';
import { useNavigate } from 'react-router-dom';

const LearnMore = () => {
  const navigate = useNavigate();

  const handleDoctorClick = () => {
    navigate('/doctors'); // Navigate to the doctor connection page
  };

  return (
    <div style={{ fontFamily: 'Arial, sans-serif', padding: '40px 20px', background: 'linear-gradient(to right, #a1c4fd, #c2e9fb)' }}>
      <h1 style={{ textAlign: 'center', color: '#004085', marginBottom: '30px', fontSize: '36px' }}>
        Connect with Mental Health Professionals
      </h1>

      <section style={{ backgroundColor: '#fff', borderRadius: '8px', padding: '30px', boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)', marginBottom: '30px' }}>
        <h2 style={{ color: '#0066cc', fontSize: '24px', marginBottom: '15px' }}>About Our Program</h2>
        <p style={{ fontSize: '18px', color: '#555', lineHeight: '1.8', marginBottom: '20px' }}>
          Our mental health program is dedicated to connecting patients with experienced doctors and therapists. We believe that timely support and professional care are essential for improving your mental well-being.
        </p>
        <p style={{ fontSize: '18px', color: '#555', lineHeight: '1.8' }}>
          Access personalized care tailored to your needs through our network of trusted mental health professionals.
        </p>
      </section>

      <section style={{ backgroundColor: '#fff', borderRadius: '8px', padding: '30px', boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)', marginBottom: '30px' }}>
        <h2 style={{ color: '#0066cc', fontSize: '24px', marginBottom: '15px' }}>How It Works</h2>
        <ul style={{ listStyleType: 'disc', marginLeft: '30px', color: '#555', fontSize: '18px', lineHeight: '1.8' }}>
          <li>Create your personalized profile.</li>
          <li>Browse our list of mental health professionals.</li>
          <li>Schedule appointments at your convenience.</li>
          <li>Receive expert support tailored to your needs.</li>
          <li>Stay connected with your doctor for ongoing care.</li>
        </ul>
      </section>

      <section style={{ textAlign: 'center', marginTop: '40px' }}>
        <h2 style={{ color: '#004085', fontSize: '24px', marginBottom: '20px' }}>Take the Next Step</h2>
        <p style={{ fontSize: '18px', color: '#004085', lineHeight: '1.8', marginBottom: '20px' }}>
          Ready to improve your mental health? Our professionals are here to guide you every step of the way.
        </p>
        <button 
          style={{
            background: 'linear-gradient(to right, #38ef7d, #11998e)',
            color: 'white',
            border: 'none',
            padding: '15px 40px',
            fontSize: '20px',
            cursor: 'pointer',
            borderRadius: '5px',
            marginTop: '20px',
            transition: 'background-color 0.3s ease, transform 0.2s ease',
            fontWeight: 'bold'
          }}
          onClick={handleDoctorClick}
        >
          Find a Doctor
        </button>
      </section>
    </div>
  );
};

export default LearnMore;
