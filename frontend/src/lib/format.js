const usd = new Intl.NumberFormat('en-US', {
  style: 'currency',
  currency: 'USD',
  maximumFractionDigits: 0,
})

const usdCents = new Intl.NumberFormat('en-US', {
  style: 'currency',
  currency: 'USD',
  minimumFractionDigits: 2,
})

export const money = (n) => usd.format(Number(n) || 0)
export const moneyExact = (n) => usdCents.format(Number(n) || 0)

export const todayISO = () => {
  // Local date, not UTC — otherwise anyone east of GMT logs income on the
  // wrong day for the first few hours of every morning.
  const d = new Date()
  const pad = (v) => String(v).padStart(2, '0')
  return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}`
}

export const prettyDate = (iso) => {
  const [y, m, d] = String(iso).split('-').map(Number)
  if (!y) return iso
  return new Date(y, m - 1, d).toLocaleDateString('en-US', { month: 'short', day: 'numeric' })
}
