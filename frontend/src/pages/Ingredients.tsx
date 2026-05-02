import { useEffect, useState } from 'react'
import { api } from '../api'

export function Ingredients() {
  const [items, setItems] = useState<any[]>([])
  useEffect(() => { api.ingredients().then(setItems) }, [])
  return (
    <div className="card">
      <h2>Ingredients</h2>
      <pre>{JSON.stringify(items, null, 2)}</pre>
    </div>
  )
}
