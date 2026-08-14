import React, {useEffect, useState} from 'react'
import axios from 'axios'

function Card({title, value}){
  return <div className="card"><div className="card-title">{title}</div><div className="card-value">{value}</div></div>
}

export default function App(){
  const [health, setHealth] = useState(null)
  const [transactions, setTransactions] = useState([])

  useEffect(()=>{
    axios.get('/api/health').then(r=>setHealth(r.data))
    axios.get('/api/transactions').then(r=>setTransactions(r.data))
  },[])

  return (
    <div className="app">
      <header className="topbar">Capital Allocation Manager</header>
      <main>
        <section className="grid">
          <Card title="Net Income This Month" value="$16,000" />
          <Card title="Manager Salary Remaining" value="$3,200" />
          <Card title="Truck Repair Reserve" value="$26,000 / $30,000" />
          <Card title="Tax Reserve" value="$3,200" />
        </section>

        <section>
          <h2>Recent Transactions</h2>
          <div className="tx-list">
            {transactions.map(tx=> (
              <div key={tx.id} className="tx">{tx.date} — {tx.bucket} — {tx.amount}</div>
            ))}
          </div>
        </section>
      </main>
      <nav className="bottom-nav">
        <button>Dashboard</button>
        <button>Transactions</button>
        <button className="add">+</button>
        <button>Trucks</button>
        <button>More</button>
      </nav>
    </div>
  )
}
