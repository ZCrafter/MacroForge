export function initTheme() {
  const dark = localStorage.getItem('mf_theme') ?? 'dark'
  document.documentElement.dataset.theme = dark
}
export function toggleTheme() {
  const next = document.documentElement.dataset.theme === 'dark' ? 'light' : 'dark'
  document.documentElement.dataset.theme = next
  localStorage.setItem('mf_theme', next)
}
