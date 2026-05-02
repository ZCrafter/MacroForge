import { toggleTheme } from '../theme'

export function Shell({ children }: { children: React.ReactNode }) {
  return (
    <div style={{maxWidth:1400, margin:'0 auto', padding:20}}>
      <div className="row" style={{justifyContent:'space-between', marginBottom:20}}>
        <h1>MacroForge</h1>
        <div className="row">
          <button onClick={toggleTheme}>Toggle Theme</button>
          <button onClick={() => { localStorage.removeItem('mf_token'); location.reload() }}>Logout</button>
        </div>
      </div>
      {children}
    </div>
  )
}
