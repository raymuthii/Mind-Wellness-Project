import React from 'react';

const About = () => {
  return (
    <div style={styles.aboutPage}>
      <header style={styles.header}>
        <h1 style={styles.heading}>About Our Mental Health Platform</h1>
        <p style={styles.subHeading}>Helping people overcome their mental hurdles by linking them to therapists.</p>
      </header>

      <section style={styles.section}>
        <h2 style={styles.sectionHeading}>Problem Statement</h2>
        <p style={styles.text}>
          Mental health issues are on the rise globally, with many individuals struggling to access the support they need. Stigma, lack of awareness, and limited access to mental health professionals often prevent people from seeking help.
        </p>
        <p style={styles.text}>
          Studies show that nearly 1 in 5 adults experience mental health challenges each year, yet only a fraction receive adequate care. This gap in access to mental health services can lead to worsening conditions, reduced quality of life, and even long-term disability.
        </p>
        <p style={styles.text}>
          Our platform aims to bridge this gap by connecting individuals with licensed therapists and providing resources to help them manage their mental health effectively.
        </p>
      </section>

      <section style={styles.section}>
        <h2 style={styles.sectionHeading}>Our Solution</h2>
        <p style={styles.text}>
          We have created a platform that connects individuals with licensed therapists, making mental health support more accessible and convenient. Whether you're dealing with anxiety, depression, stress, or other challenges, our platform is here to help.
        </p>
        <p style={styles.text}>
          Users can easily find therapists based on their needs, preferences, and location. Our platform also offers tools and resources to help individuals track their mental health progress and practice self-care.
        </p>
      </section>

      <section style={styles.section}>
        <h2 style={styles.sectionHeading}>Who Can Use This Platform?</h2>
        <p style={styles.text}>This platform is designed to be used by three types of users:</p>
        <ul style={styles.list}>
          <li style={styles.listItem}><strong>Individuals Seeking Help:</strong> People looking for professional mental health support to manage their challenges.</li>
          <li style={styles.listItem}><strong>Therapists:</strong> Licensed mental health professionals who want to connect with clients and provide support.</li>
          <li style={styles.listItem}><strong>Administrators:</strong> Individuals who manage the platform, ensuring it runs smoothly and securely.</li>
        </ul>
      </section>

      <section style={styles.section}>
        <h2 style={styles.sectionHeading}>User Stories</h2>
        <h3 style={styles.subHeading}>As an individual seeking help, you should be able to:</h3>
        <ul style={styles.list}>
          <li style={styles.listItem}>Browse and connect with licensed therapists based on your needs.</li>
          <li style={styles.listItem}>Create an account to manage your therapy sessions and progress.</li>
          <li style={styles.listItem}>Schedule appointments with therapists at your convenience.</li>
          <li style={styles.listItem}>Access tools and resources to track your mental health journey.</li>
          <li style={styles.listItem}>Communicate securely with your therapist through the platform.</li>
        </ul>

        <h3 style={styles.subHeading}>As a therapist, you should be able to:</h3>
        <ul style={styles.list}>
          <li style={styles.listItem}>Create a professional profile to showcase your expertise and availability.</li>
          <li style={styles.listItem}>Manage appointments and communicate with clients securely.</li>
          <li style={styles.listItem}>Access tools to help you provide effective support to your clients.</li>
          <li style={styles.listItem}>Track your client sessions and progress over time.</li>
        </ul>

        <h3 style={styles.subHeading}>As an administrator, you should be able to:</h3>
        <ul style={styles.list}>
          <li style={styles.listItem}>Manage user accounts and ensure the platform operates securely.</li>
          <li style={styles.listItem}>Monitor therapist profiles and verify their credentials.</li>
          <li style={styles.listItem}>Provide support to users and resolve any technical issues.</li>
        </ul>
      </section>

      <footer style={styles.footer}>
        <p style={styles.footerText}>
          Together, we can break the stigma around mental health and ensure everyone has access to the support they need. Your mental health matters, and we're here to help you every step of the way.
        </p>
      </footer>
    </div>
  );
};

const styles = {
  aboutPage: {
    fontFamily: 'Arial, sans-serif',
    lineHeight: '1.6',
    padding: '20px',
    backgroundColor: '#f4f4f4',
    color: '#333',
  },
  header: {
    background: 'linear-gradient(to right, black, #0072ff,black)',
    color: '#fff',
    padding: '20px',
    borderRadius: '8px',
    textAlign: 'center',
  },
  heading: {
    fontSize: '36px',
    margin: '0',
  },
  subHeading: {
    fontSize: '18px',
    fontStyle: 'italic',
  },
  section: {
    margin: '20px 0',
  },
  sectionHeading: {
    fontSize: '28px',
    color: '#1e90ff',
    marginBottom: '10px',
  },
  text: {
    fontSize: '16px',
    marginBottom: '10px',
    padding: '0 10px',
  },
  list: {
    listStyleType: 'none',
    paddingLeft: '0',
  },
  listItem: {
    fontSize: '16px',
    marginBottom: '8px',
    padding: '5px 10px',
    backgroundColor: '#e0f7fa',
    borderRadius: '5px',
  },
  footer: {
    backgroundColor: '#333',
    color: '#fff',
    textAlign: 'center',
    padding: '15px',
    marginTop: '30px',
    borderRadius: '8px',
  },
  footerText: {
    fontSize: '16px',
  },
};

export default About;