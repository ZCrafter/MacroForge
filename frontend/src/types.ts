export type Dashboard = {
  meals: Array<{
    meal_id: number
    name: string
    servings_per_week: number
    per_meal: Record<string, number>
    weekly: Record<string, number>
  }>
  totals: Record<string, number>
}
