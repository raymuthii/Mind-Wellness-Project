import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { donationService } from '../services/api'
import { loadStripe } from '@stripe/stripe-js'

const stripePromise = loadStripe(import.meta.env.VITE_STRIPE_PUBLIC_KEY)

export function useDonation() {
  const navigate = useNavigate()
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const handleDonation = async (formData) => {
    try {
      setLoading(true)
      setError(null)

      const amount = formData.amount === 'custom'
        ? parseFloat(formData.customAmount)
        : parseFloat(formData.amount)

      if (isNaN(amount) || amount <= 0) {
        throw new Error('Invalid donation amount')
      }

      const donation = await donationService.createDonation(amount)
      const stripe = await stripePromise

      if (!stripe) {
        throw new Error('Failed to load Stripe')
      }

      const { error: stripeError } = await stripe.redirectToCheckout({
        sessionId: donation.id,
      })

      if (stripeError) {
        throw new Error(stripeError.message)
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred')
      navigate('/payment/cancel')
    } finally {
      setLoading(false)
    }
  }

  return {
    loading,
    error,
    handleDonation,
  }
} 