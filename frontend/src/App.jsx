import { useEffect } from 'react'
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import ProtectedRoute from './ProtectedRoute'
import Header from './components/Header'
import Home from './components/Home'
import LoginPage from './components/LoginPage'
import RegisterPage from './components/RegisterPage'
import api from './axiosConfig'
import SocialAuthHandler from './components/SocialAuthHandler'

function App() {
  useEffect(() => {
    api.get('/api/auth/csrf/').catch(() => {})
  }, [])

  // If redirected back after social login, the backend will place the
  // token in the URL fragment (hash) so it is not sent to server logs.
  // Read the fragment first then fall back to query params for
  // backward-compatibility.
  useEffect(() => {
    try {
      let token = null
      // prefer token from hash (fragment)
      if (window.location.hash) {
        const raw = window.location.hash.replace(/^#/, '')
        const hashParams = new URLSearchParams(raw)
        token = hashParams.get('token') || hashParams.get('key')
      }
      // fallback to query string if not present in hash
      if (!token) {
        const params = new URLSearchParams(window.location.search)
        token = params.get('token') || params.get('key')
      }

      if (token) {
        localStorage.setItem('authToken', token)
        // clear the token from the fragment or querystring so it isn't left visible
        try {
          if (window.location.hash) {
            const raw = window.location.hash.replace(/^#/, '')
            const hashParams = new URLSearchParams(raw)
            hashParams.delete('token')
            hashParams.delete('key')
            const newHash = hashParams.toString()
            const newUrl = window.location.pathname + window.location.search + (newHash ? '#' + newHash : '')
            window.history.replaceState({}, document.title, newUrl)
          } else {
            const params = new URLSearchParams(window.location.search)
            params.delete('token')
            params.delete('key')
            const newSearch = params.toString()
            const newUrl = window.location.pathname + (newSearch ? '?' + newSearch : '')
            window.history.replaceState({}, document.title, newUrl)
          }
        } catch (ex) {
          // ignore history manipulation errors
        }

        // land on root app page now that token is stored
        window.location.replace('/')
      }
    } catch (e) {
      // ignore parsing errors
    }
  }, [])

  return (
    <BrowserRouter>
      <Header />
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />
        <Route path="/auth/complete" element={<SocialAuthHandler />} />
        
        <Route
          path="/"
          element={
            <ProtectedRoute>
              <Home />
            </ProtectedRoute>
          }
        />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App

