import { useEffect } from 'react'
import { useNavigate } from 'react-router-dom'

const SocialAuthHandler = () => {
  const navigate = useNavigate()

  useEffect(() => {
    try {
      // Prefer fragment (hash), fall back to query params
      let token = null
      if (window.location.hash) {
        const raw = window.location.hash.replace(/^#/, '')
        const p = new URLSearchParams(raw)
        token = p.get('token') || p.get('key')
      }
      if (!token) {
        const params = new URLSearchParams(window.location.search)
        token = params.get('token') || params.get('key')
      }

      if (token) {
        localStorage.setItem('authToken', token)
      }
      // remove any tokens from url for cleanliness
      try {
        const url = window.location.pathname
        window.history.replaceState({}, document.title, url)
      } catch (e) {
        // ignore
      }
    } catch (e) {
      // ignore parsing errors
    }

    // Always move to the root after handling token
    navigate('/')
  }, [navigate])

  return null
}

export default SocialAuthHandler
