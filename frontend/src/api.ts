const API = import.meta.env.VITE_API_URL || 'http://localhost:8000'

export function token() { return localStorage.getItem('mf_token') || '' }

async function req(path: string, method = 'GET', body?: any) {
  const r = await fetch(`${API}${path}`, {
    method,
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token()}`
    },
    body: body ? JSON.stringify(body) : undefined
  })
  if (!r.ok) throw new Error(await r.text())
  return r.json()
}

export const api = {
  login: (username: string, password: string) =>
    fetch(`${API}/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password })
    }).then(r => r.json()),

  me: () => req('/auth/me'),
  dashboard: () => req('/dashboard'),
  ingredients: () => req('/ingredients'),
  createIngredient: (d: any) => req('/ingredients', 'POST', d),
  updateIngredient: (id: number, d: any) => req(`/ingredients/${id}`, 'PUT', d),
  revertIngredient: (id: number) => req(`/ingredients/${id}/revert`, 'POST'),
  deleteIngredient: (id: number) => req(`/ingredients/${id}`, 'DELETE'),
  usdaSearch: (query: string, page_size = 10) => req('/ingredients/search', 'POST', { query, page_size }),
  usdaImport: (fdc_id: number) => req(`/ingredients/import/${fdc_id}`, 'POST'),
  meals: () => req('/meals'),
  createMeal: (d: any) => req('/meals', 'POST', d),
  addMealItem: (d: any) => req('/meals/item', 'POST', d),
  setMealPlan: (d: any) => req('/meals/plan', 'POST', d),
}
