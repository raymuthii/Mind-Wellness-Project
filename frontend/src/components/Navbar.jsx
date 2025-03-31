import React from 'react';
import { Link } from 'react-router-dom';
import { useDispatch, useSelector } from 'react-redux';
import { logout } from '../redux/authSlice';
import { FaHome, FaSignInAlt, FaInfoCircle, FaPhone } from 'react-icons/fa';

const Navbar = () => {
  const dispatch = useDispatch();
  const { isAuthenticated, role } = useSelector((state) => state.auth);

  const handleLogout = () => {
    dispatch(logout());
  };

  const renderNavLinks = () => {
    switch (role) {
      case 'patient':
        return (
          <>
            <li style={styles.navItem}>
              <Link to="/donations" style={styles.navLink}>Donate</Link>
            </li>
            <li style={styles.navItem}>
              <Link to="/donation-history" style={styles.navLink}>Donation History</Link>
            </li>
          </>
        );
      case 'doctor':
        return (
          <>
            <li style={styles.navItem}>
              <Link to="/provider-dashboard" style={styles.navLink}>Provider Dashboard</Link>
            </li>
            <li style={styles.navItem}>
              <Link to="/provider-application" style={styles.navLink}>Apply as a Provider</Link>
            </li>
          </>
        );
      case 'admin':
        return (
          <li style={styles.navItem}>
            <Link to="/admin-dashboard" style={styles.navLink}>Admin Dashboard</Link>
          </li>
        );
      default:
        return null;
    }
  };

  return (
    <nav style={styles.navbar}>
      {/* Website Name - Mind Wellness */}
      <div style={styles.siteName}>
        <Link to="/" style={styles.siteNameLink}>Mind Wellness</Link>
      </div>

      <ul style={styles.navList}>
        <li style={styles.navItem}>
          <Link to="/" style={styles.navLink}>
            <FaHome style={styles.icon} /> Home
          </Link>
        </li>
        {renderNavLinks()}
        {/* Contact link */}
        <li style={styles.navItem}>
          <Link to="/contact" style={styles.navLink}>
            <FaPhone style={styles.icon} /> Contact
          </Link>
        </li>
        {/* About link */}
        <li style={styles.navItem}>
          <Link to="/about" style={styles.navLink}>
            <FaInfoCircle style={styles.icon} /> About
          </Link>
        </li>

        {/* Logout button */}
        {isAuthenticated && (
          <li style={styles.navItem}>
            <button style={styles.logoutButton} onClick={handleLogout}>Logout</button>
          </li>
        )}

        {/* Login link (visible when not authenticated) */}
        {!isAuthenticated && (
          <li style={styles.navItem}>
            <Link to="/login" style={styles.navLink}>
              <FaSignInAlt style={styles.icon} /> Login
            </Link>
          </li>
        )}
      </ul>
    </nav>
  );
};

const styles = {
  navbar: {
    backgroundColor: '#333',
    padding: '10px',
    color: 'white',
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  siteName: {
    flex: 1,
    fontSize: '20px',
    fontWeight: 'bold',
  },
  siteNameLink: {
    color: 'white',
    textDecoration: 'none',
    fontSize: '20px',
  },
  navList: {
    listStyle: 'none',
    display: 'flex',
    padding: '0',
    margin: '0',
  },
  navItem: {
    marginRight: '20px',
  },
  navLink: {
    color: 'white',
    textDecoration: 'none',
    fontSize: '16px',
    display: 'flex',
    alignItems: 'center',
  },
  icon: {
    marginRight: '8px',
  },
  logoutButton: {
    backgroundColor: '#f44336',
    color: 'white',
    border: 'none',
    padding: '8px 16px',
    cursor: 'pointer',
    fontSize: '16px',
  },
};

export default Navbar;
