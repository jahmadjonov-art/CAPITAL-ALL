import { useCallback, useEffect, useMemo, useState } from 'react'
import { supabase } from './supabaseClient'
import { BUCKETS, DEFAULT_SETTINGS, allocateIncome } from './lib/allocate'

const newId = () =>
  crypto.randomUUID ? crypto.randomUUID() : String(Date.now()) + Math.random().toString(16).slice(2)

// Supabase returns { data, error } rather than throwing. Funnelling every call
// through here means a failed write surfaces in the UI instead of vanishing.
function unwrap({ data, error }) {
  if (error) throw new Error(error.message)
  return data
}

/**
 * Everything the app knows, loaded once per session and kept in memory.
 *
 * A budget is a few hundred rows, so there is no pagination, no cache layer
 * and no optimistic updates: mutate, refetch, re-render. Simple enough to
 * reason about at a glance and fast enough that you will never notice.
 */
export function useStore(session) {
  const userId = session?.user?.id ?? null

  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [settings, setSettings] = useState(DEFAULT_SETTINGS)
  const [buckets, setBuckets] = useState([])
  const [trucks, setTrucks] = useState([])
  const [transactions, setTransactions] = useState([])

  // First login has no settings row and no buckets. Create them rather than
  // making the user seed anything by hand.
  const bootstrap = useCallback(async () => {
    const existing = unwrap(
      await supabase.from('settings').select('user_id').eq('user_id', userId).maybeSingle()
    )
    if (!existing) {
      unwrap(await supabase.from('settings').insert({ user_id: userId, ...DEFAULT_SETTINGS }))
    }

    const haveBuckets = unwrap(await supabase.from('buckets').select('key').eq('user_id', userId))
    const missing = BUCKETS.filter((b) => !haveBuckets.some((h) => h.key === b.key))
    if (missing.length) {
      unwrap(
        await supabase.from('buckets').insert(
          missing.map((b) => ({
            user_id: userId,
            key: b.key,
            name: b.name,
            sort: b.sort,
            target:
              b.key === 'truck_repair'
                ? DEFAULT_SETTINGS.repair_target
                : b.key === 'future_truck'
                  ? DEFAULT_SETTINGS.future_truck_target
                  : null,
          }))
        )
      )
    }
  }, [userId])

  const refresh = useCallback(async () => {
    if (!userId) return
    try {
      setError(null)
      const [s, b, t, tx] = await Promise.all([
        supabase.from('settings').select('*').eq('user_id', userId).maybeSingle(),
        supabase.from('buckets').select('*').eq('user_id', userId).order('sort'),
        supabase.from('trucks').select('*').eq('user_id', userId).order('created_at'),
        supabase
          .from('transactions')
          .select('*')
          .eq('user_id', userId)
          .order('date', { ascending: false })
          .order('created_at', { ascending: false }),
      ])
      setSettings({ ...DEFAULT_SETTINGS, ...(unwrap(s) || {}) })
      setBuckets(unwrap(b))
      setTrucks(unwrap(t))
      setTransactions(unwrap(tx))
    } catch (e) {
      setError(e.message)
    }
  }, [userId])

  useEffect(() => {
    let cancelled = false
    if (!userId) {
      setLoading(false)
      return
    }
    ;(async () => {
      setLoading(true)
      try {
        await bootstrap()
        await refresh()
      } catch (e) {
        if (!cancelled) setError(e.message)
      } finally {
        if (!cancelled) setLoading(false)
      }
    })()
    return () => {
      cancelled = true
    }
  }, [userId, bootstrap, refresh])

  // Balances are summed from the ledger, never stored. The ledger is the only
  // source of truth, so a balance cannot drift away from its transactions.
  const balances = useMemo(() => {
    const totals = Object.fromEntries(BUCKETS.map((b) => [b.key, 0]))
    for (const tx of transactions) {
      totals[tx.bucket_key] = (totals[tx.bucket_key] || 0) + Number(tx.amount)
    }
    return totals
  }, [transactions])

  const monthKey = new Date().toISOString().slice(0, 7)
  const thisMonth = useMemo(
    () => transactions.filter((tx) => String(tx.date).slice(0, 7) === monthKey),
    [transactions, monthKey]
  )

  const summary = useMemo(() => {
    const income = thisMonth
      .filter((tx) => tx.type === 'income')
      .reduce((sum, tx) => sum + Number(tx.amount), 0)
    const spend = thisMonth
      .filter((tx) => tx.type === 'expense')
      .reduce((sum, tx) => sum + Number(tx.amount), 0)
    const salaryPaid = thisMonth
      .filter((tx) => tx.type === 'income' && tx.bucket_key === 'personal')
      .reduce((sum, tx) => sum + Number(tx.amount), 0)
    return {
      income,
      spend: Math.abs(spend),
      net: income + spend,
      salaryPaid,
      salaryRemaining: Math.max(0, Number(settings.manager_salary_cap) - salaryPaid),
    }
  }, [thisMonth, settings])

  // ----------------------------------------------------------- mutations --

  const addIncome = useCallback(
    async ({ date, amount, payee, notes }) => {
      const { lines } = allocateIncome({
        amount,
        settings,
        repairBalance: balances.truck_repair || 0,
      })
      if (!lines.length) throw new Error('Enter an income amount greater than zero.')

      const group_id = newId()
      unwrap(
        await supabase.from('transactions').insert(
          lines.map((line) => ({
            user_id: userId,
            date,
            amount: line.amount,
            type: 'income',
            bucket_key: line.bucket_key,
            category: line.category,
            payee: payee || null,
            notes: [notes, line.notes].filter(Boolean).join(' — '),
            group_id,
          }))
        )
      )
      await refresh()
    },
    [userId, settings, balances, refresh]
  )

  const addExpense = useCallback(
    async ({ date, amount, bucket_key, category, payee, notes, truck_id, odometer }) => {
      const value = Math.abs(Number(amount))
      if (!(value > 0)) throw new Error('Enter an expense amount greater than zero.')
      unwrap(
        await supabase.from('transactions').insert({
          user_id: userId,
          date,
          amount: -value, // expenses always leave a bucket
          type: 'expense',
          bucket_key,
          category: category || null,
          payee: payee || null,
          notes: notes || null,
          truck_id: truck_id || null,
          odometer: odometer ? Number(odometer) : null,
        })
      )
      await refresh()
    },
    [userId, refresh]
  )

  const addTransfer = useCallback(
    async ({ date, amount, from, to, notes }) => {
      const value = Math.abs(Number(amount))
      if (!(value > 0)) throw new Error('Enter a transfer amount greater than zero.')
      if (from === to) throw new Error('Pick two different buckets.')

      const group_id = newId()
      const shared = { user_id: userId, date, type: 'transfer', group_id, notes: notes || null }
      unwrap(
        await supabase.from('transactions').insert([
          { ...shared, amount: -value, bucket_key: from, category: 'Transfer out' },
          { ...shared, amount: value, bucket_key: to, category: 'Transfer in' },
        ])
      )
      await refresh()
    },
    [userId, refresh]
  )

  // Deleting one leg of an income split or a transfer would leave the ledger
  // unbalanced, so the whole group goes together.
  const deleteTransaction = useCallback(
    async (tx) => {
      const query = supabase.from('transactions').delete().eq('user_id', userId)
      unwrap(await (tx.group_id ? query.eq('group_id', tx.group_id) : query.eq('id', tx.id)))
      await refresh()
    },
    [userId, refresh]
  )

  const saveSettings = useCallback(
    async (next) => {
      const payload = Object.fromEntries(
        Object.keys(DEFAULT_SETTINGS).map((k) => [k, Number(next[k]) || 0])
      )
      unwrap(
        await supabase
          .from('settings')
          .update({ ...payload, updated_at: new Date().toISOString() })
          .eq('user_id', userId)
      )
      await refresh()
    },
    [userId, refresh]
  )

  const saveTruck = useCallback(
    async (truck) => {
      const payload = {
        name: truck.name,
        year: truck.year ? Number(truck.year) : null,
        make: truck.make || null,
        model: truck.model || null,
        vin: truck.vin || null,
        mileage: truck.mileage ? Number(truck.mileage) : null,
        purchase_price: Number(truck.purchase_price) || 0,
        purchase_date: truck.purchase_date || null,
        loan_balance: Number(truck.loan_balance) || 0,
      }
      unwrap(
        truck.id
          ? await supabase.from('trucks').update(payload).eq('id', truck.id).eq('user_id', userId)
          : await supabase.from('trucks').insert({ user_id: userId, ...payload })
      )
      await refresh()
    },
    [userId, refresh]
  )

  const deleteTruck = useCallback(
    async (id) => {
      unwrap(await supabase.from('trucks').delete().eq('id', id).eq('user_id', userId))
      await refresh()
    },
    [userId, refresh]
  )

  return {
    loading,
    error,
    setError,
    settings,
    buckets,
    trucks,
    transactions,
    balances,
    summary,
    refresh,
    addIncome,
    addExpense,
    addTransfer,
    deleteTransaction,
    saveSettings,
    saveTruck,
    deleteTruck,
  }
}
