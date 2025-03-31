import React from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { approveProvider, rejectProvider, deleteProvider } from '../redux/providersSlice';
import { useNavigate } from 'react-router-dom';
import { Pie } from 'react-chartjs-2';
import { Chart as ChartJS, Title, Tooltip, Legend, ArcElement, CategoryScale, LinearScale } from 'chart.js';

// Register Chart.js components
ChartJS.register(Title, Tooltip, Legend, ArcElement, CategoryScale, LinearScale);

const AdminDashboard = () => {
  const dispatch = useDispatch();
  const navigate = useNavigate();
  
  // Updated state selectors for mental health providers
  const approvedProviders = useSelector(state => state.providers.approvedProviders);
  const providerApplications = useSelector(state => state.providers.providerApplications);

  // Example data for the pie chart
  const pieChartData = {
    labels: ['Pending', 'Approved', 'Rejected'],
    datasets: [
      {
        data: [
          providerApplications.filter(p => p.status === 'pending').length,
          approvedProviders.length,
          providerApplications.filter(p => p.status === 'rejected').length
        ],
        backgroundColor: ['#FFCE56', '#36A2EB', '#FF5733'],
        hoverBackgroundColor: ['#FFB84D', '#2F8BDE', '#FF4C3B']
      }
    ]
  };

  const handleApprove = (id) => {
    dispatch(approveProvider(id));
  };

  const handleReject = (id) => {
    dispatch(rejectProvider(id));
  };

  const handleDelete = (id) => {
    const confirmed = window.confirm('Are you sure you want to delete this provider?');
    if (confirmed) {
      dispatch(deleteProvider(id));
    }
  };

  return (
    <div style={styles.dashboardContainer}>
      <h2 style={styles.header}>Admin Dashboard</h2>

      {/* Pie Chart Section */}
      <div style={styles.chartContainer}>
        <h3 style={styles.chartHeader}>Provider Application Status</h3>
        <div style={styles.chartWrapper}>
          <Pie data={pieChartData} options={{ responsive: true }} />
        </div>
      </div>

      {/* Provider Applications Section */}
      <div style={styles.section}>
        <h3 style={styles.sectionHeader}>Review Provider Applications</h3>
        {providerApplications.length > 0 ? (
          <ul style={styles.list}>
            {providerApplications.map((provider) => (
              <li key={provider.id} style={styles.listItem}>
                <h4>{provider.name}</h4>
                <p>{provider.description}</p>
                <p>Status: {provider.status}</p>
                <div>
                  <button
                    onClick={() => handleApprove(provider.id)}
                    disabled={provider.status !== 'pending'}
                    style={styles.button}
                  >
                    Approve
                  </button>
                  <button
                    onClick={() => handleReject(provider.id)}
                    disabled={provider.status !== 'pending'}
                    style={styles.button}
                  >
                    Reject
                  </button>
                  <button
                    onClick={() => handleDelete(provider.id)}
                    style={styles.buttonDelete}
                  >
                    Delete
                  </button>
                </div>
              </li>
            ))}
          </ul>
        ) : (
          <p>No pending provider applications.</p>
        )}
      </div>

      {/* Approved Providers Section */}
      <div style={styles.section}>
        <h3 style={styles.sectionHeader}>Approved Providers</h3>
        {approvedProviders.length > 0 ? (
          <ul style={styles.list}>
            {approvedProviders.map((provider) => (
              <li key={provider.id} style={styles.listItem}>
                <h4>{provider.name}</h4>
                <p>{provider.description}</p>
                <p>Status: {provider.status}</p>
                <div>
                  <button
                    onClick={() => navigate(`/provider/${provider.id}`)}
                    style={styles.button}
                  >
                    View Provider
                  </button>
                  <button
                    onClick={() => handleDelete(provider.id)}
                    style={styles.buttonDelete}
                  >
                    Delete
                  </button>
                </div>
              </li>
            ))}
          </ul>
        ) : (
          <p>No approved providers yet.</p>
        )}
      </div>
    </div>
  );
};

// Inline styles for the Admin Dashboard
const styles = {
  dashboardContainer: {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    padding: '20px',
    fontFamily: 'Arial, sans-serif',
    backgroundColor: '#f4f4f4',
    minHeight: '100vh',
  },
  header: {
    fontSize: '2rem',
    marginBottom: '20px',
  },
  chartContainer: {
    width: '80%',
    marginBottom: '40px',
    backgroundColor: '#fff',
    padding: '20px',
    borderRadius: '8px',
    boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)',
  },
  chartHeader: {
    fontSize: '1.5rem',
    marginBottom: '20px',
  },
  chartWrapper: {
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
  },
  section: {
    width: '80%',
    backgroundColor: '#fff',
    padding: '20px',
    marginBottom: '40px',
    borderRadius: '8px',
    boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)',
  },
  sectionHeader: {
    fontSize: '1.5rem',
    marginBottom: '15px',
  },
  list: {
    listStyleType: 'none',
    paddingLeft: '0',
  },
  listItem: {
    padding: '10px',
    backgroundColor: '#f9f9f9',
    marginBottom: '10px',
    borderRadius: '5px',
    boxShadow: '0 2px 4px rgba(0, 0, 0, 0.1)',
  },
  button: {
    margin: '5px',
    padding: '8px 16px',
    borderRadius: '5px',
    border: 'none',
    backgroundColor: '#36A2EB',
    color: '#fff',
    cursor: 'pointer',
  },
  buttonDelete: {
    margin: '5px',
    padding: '8px 16px',
    borderRadius: '5px',
    border: 'none',
    backgroundColor: '#FF5733',
    color: '#fff',
    cursor: 'pointer',
  }
};

export default AdminDashboard;
