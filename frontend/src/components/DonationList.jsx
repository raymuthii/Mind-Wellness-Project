import React from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { setSelectedCampaign } from '../redux/donationSlice';
import { Link } from 'react-router-dom';

const DonationList = () => {
  const dispatch = useDispatch();
  // Updated to use the providers state instead of the old charity state
  const campaigns = useSelector(state => state.providers.providers);

  const handleCampaignClick = (campaign) => {
    dispatch(setSelectedCampaign(campaign));
  };

  return (
    <div>
      <h2>Mental Health Support Campaigns</h2>
      {campaigns && campaigns.length > 0 ? (
        <ul>
          {campaigns.map((campaign) => (
            <li key={campaign.id}>
              <h3>{campaign.name}</h3>
              <p>{campaign.description}</p>
              <Link to="/donate" onClick={() => handleCampaignClick(campaign)}>
                <button>Donate Now</button>
              </Link>
            </li>
          ))}
        </ul>
      ) : (
        <p>No campaigns available. Be the first to support mental health care!</p>
      )}
    </div>
  );
};

export default DonationList;
