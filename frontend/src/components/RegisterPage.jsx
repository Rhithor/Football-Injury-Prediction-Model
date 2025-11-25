import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import api from '../axiosConfig'
import './Auth.css'

const RegisterPage = () => {
  const navigate = useNavigate()
  const [form, setForm] = useState({
    username: '',
    email: '',
    password1: '',
    password2: '',
  })
  const [error, setError] = useState('')

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value })
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    try {
      const { data } = await api.post('/auth/registration/', form)
      localStorage.setItem('authToken', data.key)
      navigate('/')
    } catch (err) {
      const resp = err.response?.data
      setError(
        resp?.email?.[0] ||
        resp?.password1?.[0] ||
        resp?.non_field_errors?.[0] ||
        'Registration failed'
      )
    }
  }

  const handleGoogleSignup = () => {
    const backend = import.meta.env.VITE_BACKEND_URL || 'http://localhost:8000'
    window.location.href = `${backend}/accounts/google/login/`
  }

  return (
    <div className="auth-container">
      <form className="auth-card" onSubmit={handleSubmit} autoComplete="off">
        <h2>Create account</h2>
        {error && <p className="auth-error">{error}</p>}

        <label htmlFor="username">Username</label>
        <input
          id="username"
          name="username"
          value={form.username}
          onChange={handleChange}
          required
          autoComplete="off"
        />

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

        <label htmlFor="password1">Password</label>
        <input
          id="password1"
          name="password1"
          type="password"
          value={form.password1}
          onChange={handleChange}
          required
          autoComplete="new-password"
        />

        <label htmlFor="password2">Confirm password</label>
        <input
          id="password2"
          name="password2"
          type="password"
          value={form.password2}
          onChange={handleChange}
          required
          autoComplete="new-password"
        />

        <button type="submit">Register</button>

        <div className="auth-divider">or</div>

        <button type="button" className="google-btn" onClick={handleGoogleSignup}>
          Sign up with Google
        </button>

        <p>
          Already have an account? <Link to="/login">Login</Link>
        </p>
      </form>
      </div>
  )
}

export default RegisterPage
