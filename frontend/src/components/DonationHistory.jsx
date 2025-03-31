import React from 'react';
import { useSelector } from 'react-redux';

const DonationHistory = () => {
  const donationHistory = useSelector(state => state.donation.donationHistory);

  return (
    <div style={{ padding: '20px', fontFamily: 'Arial, sans-serif' }}>
      <h2>Your Mental Health Donation History</h2>
      {donationHistory.length > 0 ? (
        <ul style={{ listStyleType: 'none', padding: 0 }}>
          {donationHistory.map((donation, index) => (
            <li key={index} style={{ marginBottom: '20px', backgroundColor: '#f9f9f9', padding: '15px', borderRadius: '5px', boxShadow: '0 2px 4px rgba(0,0,0,0.1)' }}>
              <h3 style={{ margin: '0 0 10px 0' }}>{donation.campaignTitle}</h3>
              <p style={{ margin: '5px 0' }}>Amount Donated: ${donation.amount}</p>
              <p style={{ margin: '5px 0' }}>Date: {new Date(donation.date).toLocaleDateString()}</p>
              {donation.isAnonymous 
                ? <p style={{ margin: '5px 0', fontStyle: 'italic' }}>Anonymous Donation</p> 
                : <p style={{ margin: '5px 0' }}>Donor: {donation.userName}</p>}
            </li>
          ))}
        </ul>
      ) : (
        <p>No donations yet. Your support can make a difference in mental health care.</p>
      )}
    </div>
  );
};

export default DonationHistory;
