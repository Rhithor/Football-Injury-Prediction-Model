import { Navigate } from 'react-router-dom'
import { useEffect, useState } from 'react'
import api from './axiosConfig'

const ProtectedRoute = ({ children }) => {
  const token = localStorage.getItem('authToken')
  const [checking, setChecking] = useState(true)
  const [valid, setValid] = useState(false)

  useEffect(() => {
    // no token -> unauthenticated
    if (!token) {
      setChecking(false)
      setValid(false)
      return
    }

    // Validate token with backend; clear on failure
    let mounted = true
    api.get('/auth/user/')
      .then(() => {
        if (!mounted) return
        setValid(true)
      })
      .catch(() => {
        if (!mounted) return
        localStorage.removeItem('authToken')
        setValid(false)
      })
      .finally(() => {
        if (!mounted) return
        setChecking(false)
      })

    return () => { mounted = false }
  }, [token])

  // While validating return null to avoid UI flicker
  if (checking) return null

  if (!valid) {
    return <Navigate to="/login" replace />
  }

  return children
}

export default ProtectedRoute