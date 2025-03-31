import React, { useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { addDonation } from '../redux/donationSlice';
import { loadStripe } from '@stripe/stripe-js';
import { Elements } from '@stripe/react-stripe-js';
import CheckoutForm from './CheckoutForm';
import { Bar } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend } from 'chart.js';

// Register chart.js components
ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

const stripePromise = loadStripe('your-stripe-public-key-here');

const DonateForm = () => {
  const dispatch = useDispatch();
  const selectedCampaign = useSelector(state => state.donation.selectedCampaign);
  const donationHistory = useSelector(state => state.donation.donationHistory);

  const donationSuccessCount = donationHistory.filter(donation => donation.success).length;  // Count of successful donations
  const donationSuccessRate = donationHistory.length > 0 ? (donationSuccessCount / donationHistory.length) * 100 : 0;

  const [amount, setAmount] = useState('');
  const [userName, setUserName] = useState('');
  const [recurring, setRecurring] = useState(false);
  const [anonymity, setAnonymity] = useState(true);

  const handleDonate = async () => {
    const donationData = {
      amount,
      userName: anonymity ? 'Anonymous' : userName,
      recurring,
      date: new Date().toISOString(),
      campaignTitle: selectedCampaign ? selectedCampaign.title : 'Mental Health Support Campaign',
      isAnonymous: anonymity,
      success: true,  // Assuming the donation is successful; integrate Stripe API for real tracking
    };

    dispatch(addDonation(donationData));  // Dispatch donation to Redux store
    alert('Donation successful! Thank you for supporting mental health care.');
  };

  // Calculate the total donation amount
  const totalDonations = donationHistory.reduce((total, donation) => total + parseFloat(donation.amount), 0).toFixed(2);

  // Month-over-Month (MoM) calculation
  const getMonthChange = () => {
    const lastMonthDonations = donationHistory.filter(donation => {
      const donationDate = new Date(donation.date);
      const lastMonth = new Date();
      lastMonth.setMonth(lastMonth.getMonth() - 1);
      return donationDate.getMonth() === lastMonth.getMonth() && donationDate.getFullYear() === lastMonth.getFullYear();
    });

    const thisMonthDonations = donationHistory.filter(donation => {
      const donationDate = new Date(donation.date);
      const currentMonth = new Date();
      return donationDate.getMonth() === currentMonth.getMonth() && donationDate.getFullYear() === currentMonth.getFullYear();
    });

    const lastMonthTotal = lastMonthDonations.reduce((total, donation) => total + parseFloat(donation.amount), 0);
    const thisMonthTotal = thisMonthDonations.reduce((total, donation) => total + parseFloat(donation.amount), 0);
    
    const monthChange = lastMonthTotal ? ((thisMonthTotal - lastMonthTotal) / lastMonthTotal) * 100 : 0;

    return monthChange.toFixed(2);
  };

  // Year-over-Year (YoY) calculation
  const getYearChange = () => {
    const lastYearDonations = donationHistory.filter(donation => {
      const donationDate = new Date(donation.date);
      const lastYear = new Date();
      lastYear.setFullYear(lastYear.getFullYear() - 1);
      return donationDate.getFullYear() === lastYear.getFullYear();
    });

    const thisYearDonations = donationHistory.filter(donation => {
      const donationDate = new Date(donation.date);
      const currentYear = new Date();
      return donationDate.getFullYear() === currentYear.getFullYear();
    });

    const lastYearTotal = lastYearDonations.reduce((total, donation) => total + parseFloat(donation.amount), 0);
    const thisYearTotal = thisYearDonations.reduce((total, donation) => total + parseFloat(donation.amount), 0);
    
    const yearChange = lastYearTotal ? ((thisYearTotal - lastYearTotal) / lastYearTotal) * 100 : 0;

    return yearChange.toFixed(2);
  };

  // Chart Data for transaction success rate
  const data = {
    labels: ['Transaction Success Rate'],
    datasets: [
      {
        label: 'Success Rate (%)',
        data: [donationSuccessRate],
        backgroundColor: 'rgba(75, 192, 192, 0.6)',
        borderColor: 'rgba(75, 192, 192, 1)',
        borderWidth: 1,
      },
    ],
  };

  const options = {
    responsive: true,
    scales: {
      y: {
        beginAtZero: true,
        max: 100,
        ticks: {
          stepSize: 20,
        },
      },
    },
    plugins: {
      legend: {
        position: 'top',
      },
      title: {
        display: true,
        text: 'Transaction Success Rate',
      },
    },
  };

  return (
    <div>
      <h2>Donate to {selectedCampaign?.title || 'Mental Health Support Campaign'}</h2>

      {/* Donation Benefits Section */}
      <div className="donation-benefits">
        <h3>Why Donate?</h3>
        <ul>
          <li><strong>Improve Mental Health:</strong> Your donation helps connect patients with vital mental health professionals.</li>
          <li><strong>Community Support:</strong> Contribute to initiatives that enhance mental health services and awareness.</li>
          <li><strong>Tax Benefits:</strong> Donations may be tax-deductible, allowing you to give while saving.</li>
        </ul>
      </div>

      {/* Donation Stats Section */}
      <div className="donation-stats">
        <h3>Donation Impact Dashboard</h3>
        <p><strong>Successful Transactions:</strong> {donationSuccessCount} successful donations.</p>
        <p><strong>Transaction Success Rate:</strong> {donationSuccessRate.toFixed(2)}%</p>
        <p><strong>Total Donations:</strong> ${totalDonations}</p>
        <p><strong>MoM Change:</strong> +{getMonthChange()}%</p>
        <p><strong>YoY Change:</strong> +{getYearChange()}%</p>
      </div>

      {/* Bar Chart for Transaction Success Rate */}
      <div className="success-rate-chart">
        <Bar data={data} options={options} />
      </div>

      {/* Donation Form */}
      <div className="donation-form">
        <input
          type="number"
          placeholder="Donation Amount"
          value={amount}
          onChange={(e) => setAmount(e.target.value)}
        />
        <label>
          <input
            type="checkbox"
            checked={recurring}
            onChange={() => setRecurring(!recurring)}
          />
          Recurring Donation
        </label>
        <label>
          <input
            type="checkbox"
            checked={anonymity}
            onChange={() => setAnonymity(!anonymity)}
          />
          Anonymous Donation
        </label>
        {!anonymity && (
          <input
            type="text"
            placeholder="Your Name"
            value={userName}
            onChange={(e) => setUserName(e.target.value)}
          />
        )}
        
        <Elements stripe={stripePromise}>
          <CheckoutForm donationAmount={amount} />
        </Elements>

        <button onClick={handleDonate}>Donate</button>
      </div>
    </div>
  );
};

export default DonateForm;
