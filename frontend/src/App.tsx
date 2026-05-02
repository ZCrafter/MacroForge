import { useState } from 'react'
import { Shell } from './components/Shell'
import { Dashboard } from './pages/Dashboard'
import { Ingredients } from './pages/Ingredients'
import { Meals } from './pages/Meals'
import { Goals } from './pages/Goals'
import { Settings } from './pages/Settings'

export default function App() {
  const [tab, setTab] = useState('dashboard')
  return (
    <Shell>
      <div className="row" style={{marginBottom:16}}>
        {['dashboard','ingredients','meals','goals','settings'].map(t => <button key={t} onClick={() => setTab(t)}>{t}</button>)}
      </div>
      {tab === 'dashboard' && <Dashboard />}
      {tab === 'ingredients' && <Ingredients />}
      {tab === 'meals' && <Meals />}
      {tab === 'goals' && <Goals />}
      {tab === 'settings' && <Settings />}
    </Shell>
  )
}
