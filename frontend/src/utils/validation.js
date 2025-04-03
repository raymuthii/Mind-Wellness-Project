export const validateEmail = (email) => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  return emailRegex.test(email)
}

export const validatePassword = (password) => {
  // At least 8 characters, 1 uppercase letter, 1 lowercase letter, 1 number
  const passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$/
  return passwordRegex.test(password)
}

export const validateAmount = (amount) => {
  return amount > 0 && amount <= 1000000 // Maximum donation of $1,000,000
}

export const validateName = (name) => {
  return name.length >= 2 && name.length <= 100
}

export const validateMessage = (message) => {
  return message.length <= 500 // Maximum message length of 500 characters
}

export const validateDonationForm = (formData) => {
  const errors = {}

  if (!validateEmail(formData.email)) {
    errors.email = 'Please enter a valid email address'
  }

  if (!validateName(formData.name)) {
    errors.name = 'Name must be between 2 and 100 characters'
  }

  const amount = formData.amount === 'custom'
    ? parseFloat(formData.customAmount)
    : parseFloat(formData.amount)

  if (isNaN(amount) || !validateAmount(amount)) {
    errors.amount = 'Please enter a valid donation amount between $0.01 and $1,000,000'
  }

  if (formData.message && !validateMessage(formData.message)) {
    errors.message = 'Message must be less than 500 characters'
  }

  return errors
} 