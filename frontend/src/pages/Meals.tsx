import { useEffect, useState } from 'react'
import { api } from '../api'

export function Meals() {
  const [meals, setMeals] = useState<any[]>([])
  const [newMealName, setNewMealName] = useState('')

  useEffect(() => {
    api.meals().then(setMeals)
  }, [])

  return (
    <div className="grid">
      <div className="card">
        <h2>Create Meal</h2>
        <div className="row">
          <input value={newMealName} onChange={e => setNewMealName(e.target.value)} placeholder="Meal name" />
          <button onClick={async () => {
            if (newMealName) {
              await api.createMeal({ name: newMealName })
              setNewMealName('')
              api.meals().then(setMeals)
            }
          }}>Create</button>
        </div>
      </div>
      <div className="card">
        <h2>Meals</h2>
        {meals.map(m => (
          <div key={m.id} style={{marginBottom:16}}>
            <strong>{m.name}</strong>
            <div className="small">{m.notes || 'No notes'}</div>
          </div>
        ))}
      </div>
    </div>
  )
}
