
import { Link, useNavigate } from 'react-router-dom'
import api from '../axiosConfig'
import '../App.css'

const Header = () => {
  const navigate = useNavigate()
  const token = localStorage.getItem('authToken')

  const handleLogout = async () => {
    try {
      await api.post('/auth/logout/')
    } catch (e) {
      // ignore backend logout errors
    }
    localStorage.removeItem('authToken')
    navigate('/login')
  }

  return (
    <header className="top-nav-wrapper">
      <nav className="top-nav">
        <div className="brand">
          <Link to="/" className="brand-link">
            <span className="brand-icon" aria-hidden="true" />
            Football Injury Prediction
          </Link>
        </div>
        <div className="nav-links">
          {!token ? (
            <>
              <Link to="/login">Sign In</Link>
              <Link to="/register">Sign Up</Link>
            </>
          ) : (
            <button className="signout-btn" onClick={handleLogout}>Sign Out</button>
          )}
        </div>
      </nav>
    </header>
  )
}

export default Header
