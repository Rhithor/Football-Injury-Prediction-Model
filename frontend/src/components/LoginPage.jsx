import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import api from '../axiosConfig'
import './Auth.css'

const LoginPage = () => {
  const navigate = useNavigate()
  const [form, setForm] = useState({ email: '', password: '' })
  const [error, setError] = useState('')

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value })
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    try {
      const { data } = await api.post('/auth/login/', form)
      localStorage.setItem('authToken', data.key)
      navigate('/')
    } catch (err) {
      const resp = err.response?.data
      setError(resp?.non_field_errors?.[0] || 'Login failed')
    }
  }

  const handleGoogleLogin = () => {
    // Prefer a Vite env var so different environments can point to other backends
    // without changing source. Falls back to localhost:8000 for local dev.
    const backend = import.meta.env.VITE_BACKEND_URL || 'http://localhost:8000'
    // Allow configuring prompt from environment (Vite) but default to
    // `login` so the provider will reauthenticate when possible.
    const prompt = import.meta.env.VITE_GOOGLE_PROMPT || 'login'
    window.location.href = `${backend}/accounts/google/login/?prompt=${encodeURIComponent(prompt)}`
  }

  return (
    <div className="auth-container">
      <form className="auth-card" onSubmit={handleSubmit} autoComplete="off">
        <h2>Welcome back</h2>
        {error && <p className="auth-error">{error}</p>}

        <label htmlFor="email">Email</label>
        <input
          id="email"
          name="email"
          type="email"
          value={form.email}
          onChange={handleChange}
          required
          autoComplete="email"
        />

        <label htmlFor="password">Password</label>
        <input
          id="password"
          name="password"
          type="password"
          value={form.password}
          onChange={handleChange}
          required
          autoComplete="new-password"
        />

        <button type="submit">Login</button>

        <div className="auth-divider">or</div>

        <button type="button" className="google-btn" onClick={handleGoogleLogin}>
          Continue with Google
        </button>

        <p>
          New here? <Link to="/register">Create an account</Link>
        </p>
      </form>
      </div>
  )
}

export default LoginPage
