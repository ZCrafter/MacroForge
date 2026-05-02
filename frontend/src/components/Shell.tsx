export function Shell({ children }: { children: React.ReactNode }) {
  return (
    <div className="container">
      <div className="row" style={{justifyContent:'space-between', marginBottom:20}}>
        <h1>MacroForge</h1>
        <div className="row">
          <button onClick={toggleTheme} className="btn-small">Theme</button>
          <button onClick={() => { localStorage.removeItem('mf_token'); location.reload() }} className="btn-small">Logout</button>
        </div>
      </div>
      {children}
    </div>
  )
}
