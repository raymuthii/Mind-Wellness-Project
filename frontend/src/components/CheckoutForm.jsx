import React, { useState } from 'react';
import { CardElement, useStripe, useElements } from '@stripe/react-stripe-js';

const CheckoutForm = ({ donationAmount, campaignTitle, isAnonymous, userName, beneficiaryStories }) => {
  const stripe = useStripe();
  const elements = useElements();
  const [processing, setProcessing] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!stripe || !elements) {
      return;
    }

    setProcessing(true);

    const cardElement = elements.getElement(CardElement);

    const { error, paymentIntent } = await stripe.confirmCardPayment(
      'your-client-secret-from-backend',
      {
        payment_method: {
          card: cardElement,
        },
      }
    );

    if (error) {
      setError(error.message);
    } else {
      const newDonation = {
        campaignTitle,
        amount: donationAmount,
        date: new Date().toISOString(),
        isAnonymous,
        userName,  
        beneficiaryStories, 
      };

      const donationHistory = JSON.parse(localStorage.getItem('donations')) || [];
      localStorage.setItem('donations', JSON.stringify([...donationHistory, newDonation]));

      console.log('Payment succeeded!', paymentIntent);
      setError(null);
    }

    setProcessing(false);
  };

  return (
    <form onSubmit={handleSubmit}>
      <label>
        Donation Payment Details
        <CardElement />
      </label>
      <br />
      
      {error && <p>{error}</p>}
    </form>
  );
};

export default CheckoutForm;
