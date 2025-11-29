
import { Link, useNavigate } from 'react-router-dom'
import { useEffect, useState } from 'react'
import api from '../axiosConfig'
import '../App.css'

const Header = () => {
  const navigate = useNavigate()
  const token = localStorage.getItem('authToken')
  const [user, setUser] = useState(null)

  const handleLogout = async () => {
    try {
      await api.post('/auth/logout/')
    } catch (e) {
      // ignore backend logout errors
    }
    localStorage.removeItem('authToken')
    navigate('/login')
  }

  const handleDeleteAccount = async () => {
    const ok = window.confirm('Delete your account permanently? This cannot be undone.')
    if (!ok) return
    try {
      await api.delete('/api/account/delete/')
    } catch (e) {
      window.alert('Unable to delete account: ' + (e.response?.data?.detail || e.message))
      return
    }
    // Remove client-side auth state and navigate to the home page
    localStorage.removeItem('authToken')
    setUser(null)
    navigate('/')
  }

  useEffect(() => {
    let mounted = true
    const fetchUser = async () => {
      if (!token) return
      try {
        const resp = await api.get('/auth/user/')
        if (mounted && resp && resp.data) {
          // store the full user payload returned by the API
          setUser(resp.data)
        }
      } catch (e) {
        // ignore — token may be invalid or expired
        setUser(null)
      }
    }
    fetchUser()
    return () => { mounted = false }
  }, [token])

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
              <div style={{display:'flex',gap:12,alignItems:'center'}}>
                {user ? (
                  <div style={{display:'flex',alignItems:'center',gap:8}}>
                    {/* avatar or initials */}
                    {user.avatar || user.picture || user.profile_image ? (
                      <img src={user.avatar || user.picture || user.profile_image} alt="avatar" style={{width:36,height:36,borderRadius:10,objectFit:'cover',border:'1px solid rgba(255,255,255,0.06)'}} />
                    ) : (
                      <div style={{width:36,height:36,borderRadius:9999,display:'flex',alignItems:'center',justifyContent:'center',background:'#d4af37',color:'#0b0b0b',fontWeight:700}}>
                        {(() => {
                          const full = ((user.first_name || '') + ' ' + (user.last_name || '')).trim() || user.username || user.email || ''
                          const parts = full.split(/\s+/).filter(Boolean)
                          if (parts.length === 0) return ''
                          if (parts.length === 1) return parts[0].slice(0,2).toUpperCase()
                          return (parts[0][0] + parts[parts.length-1][0]).toUpperCase()
                        })()}
                      </div>
                    )}

                    <div style={{display:'flex',flexDirection:'column',lineHeight:1}}>
                      <div style={{fontWeight:700, color:'#fff'}}>{(user.first_name || user.last_name) ? `${user.first_name || ''} ${user.last_name || ''}`.trim() : (user.username || user.email)}</div>
                      {user.email ? <div style={{fontSize:'0.8rem', color:'rgba(255,255,255,0.7)'}}>{user.email}</div> : null}
                    </div>
                    </div>
                ) : null}
                <div style={{display:'flex',gap:8,alignItems:'center'}}>
                  <button className="signout-btn" onClick={handleLogout}>Sign Out</button>
                  <button style={{background:'transparent',border:'1px solid rgba(255,80,80,0.18)',color:'#ff6b6b',padding:'8px 12px',borderRadius:8,cursor:'pointer'}} onClick={handleDeleteAccount}>Delete account</button>
                </div>
              </div>
          )}
        </div>
      </nav>
    </header>
  )
}

export default Header
