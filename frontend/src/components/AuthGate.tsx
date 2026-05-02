import { useEffect, useState } from 'react'
import { api } from '../api'

export function AuthGate({ children }: { children: React.ReactNode }) {
  const [state, setState] = useState<'checking' | 'authed' | 'login'>('checking')
  const [err, setErr] = useState('')

  useEffect(() => {
    const t = localStorage.getItem('mf_token')
    if (!t) {
      setState('login')
      return
    }
    api.me().then(() => setState('authed')).catch(() => {
      localStorage.removeItem('mf_token')
      setState('login')
    })
  }, [])

  if (state === 'checking') return <div className="card">Checking login...</div>
  if (state === 'authed') return <>{children}</>

  return (
    <div style={{maxWidth:360, margin:'80px auto'}} className="card">
      <h2>MacroForge</h2>
      <p className="small">Sign in to continue.</p>
      <form onSubmit={async e => {
        e.preventDefault()
        const f = new FormData(e.currentTarget)
        try {
          const r = await api.login(String(f.get('username')), String(f.get('password')))
          localStorage.setItem('mf_token', r.access_token)
          location.reload()
        } catch {
          setErr('Login failed')
        }
      }}>
        <div className="grid">
          <input name="username" placeholder="Username" defaultValue="admin" />
          <input name="password" placeholder="Password" type="password" />
          <button type="submit">Login</button>
          {err && <div className="small">{err}</div>}
        </div>
      </form>
    </div>
  )
}
