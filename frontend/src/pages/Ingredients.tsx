import { useEffect, useState } from 'react'
import { api } from '../api'
import { IngredientsTable } from '../components/IngredientsTable'

export function Ingredients() {
  const [items, setItems] = useState<any[]>([])
  const [query, setQuery] = useState('')
  const [results, setResults] = useState<any[]>([])

  async function load() {
    setItems(await api.ingredients())
  }

  useEffect(() => { load() }, [])

  return (
    <div className="grid">
      <div className="card">
        <h2>Ingredients</h2>
        <div className="row">
          <input value={query} onChange={e => setQuery(e.target.value)} placeholder="Search USDA..." />
          <button onClick={async () => setResults(await api.usdaSearch(query))}>Search USDA</button>
        </div>
        <div className="small">Auto-import works once you add a USDA API key to the backend environment.</div>
        {results.length > 0 && (
          <div style={{marginTop:12}}>
            {results.map(r => (
              <div key={r.fdcId} className="row" style={{justifyContent:'space-between', marginBottom:8}}>
                <div>{r.description}</div>
                <button onClick={async () => { await api.usdaImport(r.fdcId); await load(); }}>Import</button>
              </div>
            ))}
          </div>
        )}
      </div>
      <div className="card">
        <IngredientsTable data={items} />
      </div>
    </div>
  )
}
