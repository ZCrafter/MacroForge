import { useEffect, useState } from 'react'
import { api } from '../api'

export function Dashboard() {
  const [data, setData] = useState<any>(null)
  useEffect(() => {
    api.dashboard().then(setData).catch(console.error)
  }, [])

  if (!data) return <div className="card">Loading...</div>

  return (
    <div className="grid">
      <div className="card">
        <h2>Weekly Totals</h2>
        <div className="row">
          <div>Calories: <strong>{data.totals.calories.toLocaleString()}</strong></div>
          <div>Protein: <strong>{data.totals.protein_g.toFixed(0)}g</strong></div>
          <div>Carbs: <strong>{data.totals.carbs_g.toFixed(0)}g</strong></div>
          <div>Fat: <strong>{data.totals.fat_g.toFixed(0)}g</strong></div>
          <div>Cost: $<strong>{data.totals.price.toFixed(2)}</strong></div>
        </div>
      </div>
      <div className="card">
        <h2>Meals</h2>
        {data.meals.map((m: any) => (
          <div key={m.meal_id} style={{marginBottom:16, padding:12, background:'var(--bg)', borderRadius:8}}>
            <div className="row">
              <strong>{m.name}</strong>
              <span>{m.servings_per_week} / week</span>
            </div>
            <div className="row">
              <div>Calories: {m.per_meal.calories.toFixed(0)}</div>
              <div>Protein: {m.per_meal.protein_g.toFixed(0)}g</div>
              <div>Cost: ${m.per_meal.price.toFixed(2)}</div>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
