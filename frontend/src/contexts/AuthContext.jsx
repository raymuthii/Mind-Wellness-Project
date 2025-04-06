import { createContext, useContext, useState, useEffect } from 'react'
import { authService } from '../services/api'

const AuthContext = createContext(undefined)

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const initAuth = async () => {
      try {
        const token = localStorage.getItem('token')
        if (token) {
          const userData = await authService.getCurrentUser()
          setUser(userData)
        }
      } catch (error) {
        console.error('Error initializing auth:', error)
        // Clear invalid token
        localStorage.removeItem('token')
      } finally {
        setLoading(false)
      }
    }

    initAuth()
  }, [])

  const register = async (formData) => {
    try {
      const { user, access_token } = await authService.register(formData)
      setUser(user)
      return user
    } catch (error) {
      console.error('Registration error:', error)
      throw error
    }
  }

  const login = async (email, password) => {
    try {
      const { user, access_token } = await authService.login(email, password)
      setUser(user)
      return user
    } catch (error) {
      console.error('Login error:', error)
      throw error
    }
  }

  const logout = () => {
    authService.logout()
    setUser(null)
  }

  // Debug user state
  useEffect(() => {
    console.log('Current user state:', user)
  }, [user])

  return (
    <AuthContext.Provider value={{ user, loading, register, login, logout }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
} 