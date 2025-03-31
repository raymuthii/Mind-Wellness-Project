import React, { useState } from "react";
import { Link } from "react-router-dom";

const Home = ({ role, approvedOrganizations }) => {
  const [activeFAQ, setActiveFAQ] = useState(null);
  const [isDropdownOpen, setDropdownOpen] = useState(false);

  const toggleFAQAnswer = (index) => {
    setActiveFAQ(activeFAQ === index ? null : index);
  };

  const toggleDropdown = () => {
    setDropdownOpen(!isDropdownOpen);
  };

  const renderHomeContent = () => {
    switch (role) {
      case "individual":
        return (
          <div style={contentStyle}>
            <h1 style={mainTitleStyle}>Connect with Mental Health Doctors</h1>
            <p style={descriptionStyle}>
              Discover trusted mental health professionals ready to support your journey toward well-being. Find the care you need with ease.
            </p>

            <h2 style={{ ...mainTitleStyle, fontSize: "2rem", marginTop: "40px" }}>
              Frequently Asked Questions
            </h2>

            <div style={faqSectionStyle}>
              <div style={faqQuestionStyle} onClick={() => toggleFAQAnswer(0)}>
                ❓ <strong>How can I schedule an appointment with a doctor?</strong>
              </div>
              {activeFAQ === 0 && (
                <div style={faqAnswerStyle}>
                  Browse our list of certified mental health professionals and book an appointment at a time that works for you.
                </div>
              )}

              <div style={faqQuestionStyle} onClick={() => toggleFAQAnswer(1)}>
                ❓ <strong>Are online consultations effective?</strong>
              </div>
              {activeFAQ === 1 && (
                <div style={faqAnswerStyle}>
                  Yes, our online consultations provide convenience and expert support, allowing you to connect with doctors from the comfort of your home.
                </div>
              )}
            </div>

            <Link to="/doctors">
              <button style={buttonStyle}>Find a Doctor</button>
            </Link>
          </div>
        );
      case "organization":
        return (
          <div style={contentStyle}>
            <h1 style={mainTitleStyle}>Join Our Mental Health Provider Network</h1>
            <p style={descriptionStyle}>
              We partner with leading organizations dedicated to delivering quality mental health care. Expand your reach by joining our network.
            </p>

            <h2 style={{ ...mainTitleStyle, fontSize: "2rem", marginTop: "40px" }}>
              Trusted Partners
            </h2>
            {approvedOrganizations && approvedOrganizations.length > 0 ? (
              approvedOrganizations.map((org) => (
                <div key={org.id} style={{ marginBottom: "30px" }}>
                  <h3>{org.name}</h3>
                  <p>{org.description}</p>
                </div>
              ))
            ) : (
              <p>No approved organizations at the moment.</p>
            )}

            <Link to="/apply">
              <button style={buttonStyle}>Join as a Provider</button>
            </Link>
          </div>
        );
      default:
        return (
          <div style={contentStyle}>
            <h1 style={mainTitleStyle}>Your Mental Health Matters</h1>
            <p style={descriptionStyle}>
              Start your journey to better mental wellness today. Connect with experienced doctors and get the support you need.
            </p>
            <Link to="/doctors">
              <button style={buttonStyle}>Connect Now</button>
            </Link>
          </div>
        );
    }
  };

  return (
    <div style={containerStyle}>
      {renderHomeContent()}
      <footer style={footerStyle}>
        <div>
          <Link to="/terms" style={footerLinkStyle}>Terms of Service</Link>
          <Link to="/privacy-policy" style={footerLinkStyle}>Privacy Policy</Link>
        </div>
        <p style={{ marginTop: "20px", fontSize: "0.9rem" }}>© 2024 Mind Wellness. All rights reserved.</p>
      </footer>
    </div>
  );
};

const containerStyle = { textAlign: "center", padding: "40px" };
const contentStyle = { textAlign: "center", padding: "40px" };
const mainTitleStyle = { color: "#2980b9", fontSize: "2.5rem", fontWeight: "bold" };
const descriptionStyle = { fontSize: "1.2rem", color: "#34495e" };
const faqSectionStyle = { textAlign: "left", marginTop: "40px" };
const faqQuestionStyle = { fontSize: "1.2rem", fontWeight: "bold", color: "#2980b9", cursor: "pointer", marginBottom: "10px" };
const faqAnswerStyle = { fontSize: "1.1rem", color: "#34495e", marginBottom: "20px", paddingLeft: "20px" };
const buttonStyle = { padding: "10px 20px", backgroundColor: "#2980b9", color: "white", border: "none", borderRadius: "5px", cursor: "pointer" };
const footerStyle = { marginTop: "60px", padding: "20px 0", backgroundColor: "#2c3e50", color: "#ecf0f1", textAlign: "center" };
const footerLinkStyle = { margin: "0 15px", color: "#ecf0f1", textDecoration: "none" };

export default Home;
