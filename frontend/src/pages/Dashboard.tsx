import { useEffect, useState } from 'react'
import { api } from '../api'
import type { Dashboard as Dash } from '../types'

export function Dashboard() {
  const [data, setData] = useState<Dash | null>(null)
  useEffect(() => { api.dashboard().then(setData) }, [])
  if (!data) return <div className="card">Loading...</div>
  return (
    <div className="grid">
      <div className="card">
        <h2>Weekly Totals</h2>
        <pre>{JSON.stringify(data.totals, null, 2)}</pre>
      </div>
      <div className="card">
        <h2>Meals</h2>
        {data.meals.map(m => (
          <div key={m.meal_id} style={{marginBottom:16}}>
            <strong>{m.name}</strong> — {m.servings_per_week} / week
            <pre>{JSON.stringify(m.weekly, null, 2)}</pre>
          </div>
        ))}
      </div>
    </div>
  )
}
