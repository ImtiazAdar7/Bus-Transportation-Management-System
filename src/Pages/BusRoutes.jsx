import { useEffect, useMemo, useState } from "react"
import { useNavigate } from "react-router-dom"

const apiBase = "/api/routes"

function SeatLayoutModal({ open, onClose, data }){
  if(!open) return null
  return (
    <div style={{position:'fixed', inset:0, background:'rgba(0,0,0,0.5)', display:'flex', alignItems:'center', justifyContent:'center', zIndex: 1000}}>
      <div style={{background:'#fff', padding:'1rem', borderRadius:'0.5rem', width:'90%', maxWidth: '800px'}}>
        <div style={{display:'flex', justifyContent:'space-between', alignItems:'center'}}>
          <h3>Seat Layout - {data?.route?.operator} ({data?.route?.route})</h3>
          <button className="back-button" onClick={onClose}>Close</button>
        </div>
        <div style={{margin:'0.5rem 0'}}>Travel Date: {data?.travel_date}</div>
        <div style={{display:'grid', gridTemplateColumns:'repeat(5, 1fr)', gap:'0.5rem', alignItems:'center', justifyItems:'center'}}>
          {data?.layout?.map((row, idx) => (
            <div key={idx} style={{gridColumn:'1 / -1', display:'grid', gridTemplateColumns:'repeat(5, 1fr)', gap:'0.25rem'}}>
              {row.map((seat, i) => (
                seat ? (
                  <div key={i} style={{padding:'0.5rem', background: seat.available ? '#e8ffe8' : '#ffefef', border:'1px solid #ccc', borderRadius:'4px', textAlign:'center'}}>
                    {seat.label}
                  </div>
                ) : (
                  <div key={i} style={{height:'100%', width:'100%'}} />
                )
              ))}
            </div>
          ))}
        </div>
        <div style={{marginTop:'1rem', display:'flex', gap:'0.5rem'}}>
          <button className="registration-button" onClick={() => alert('Proceeding to booking (placeholder)')}>Proceed to Booking</button>
          <button className="back-button" onClick={onClose}>Cancel</button>
        </div>
      </div>
    </div>
  )
}

const BusRoutes = () => {
  const [from, setFrom] = useState("")
  const [to, setTo] = useState("")
  const [date, setDate] = useState("")
  const [busType, setBusType] = useState("")
  const [operator, setOperator] = useState("")
  const [priceMin, setPriceMin] = useState("")
  const [priceMax, setPriceMax] = useState("")
  const [sortBy, setSortBy] = useState("price")

  const [loading, setLoading] = useState(false)
  const [error, setError] = useState("")
  const [buses, setBuses] = useState([])
  const [suggestions, setSuggestions] = useState([])

  const [stations, setStations] = useState([])
  const [operators, setOperators] = useState([])

  const [layoutOpen, setLayoutOpen] = useState(false)
  const [layoutData, setLayoutData] = useState(null)

  const navigate = useNavigate();

  const canSearch = useMemo(() => from && to && date, [from,to,date])

  // Load meta (stations/operators) on mount (no routes by default)
  useEffect(() => {
    let ignore = false
    async function load(){
      setLoading(true)
      setError("")
      try{
        const metaRes = await fetch(`${apiBase}/meta`)
        const meta = await metaRes.json()
        if(!metaRes.ok){ throw new Error(meta?.message || 'Failed to load stations') }
        if(!ignore){
          setStations(meta.stations || [])
          setOperators(meta.operators || [])
          setBuses([])
          setSuggestions([])
        }
      }catch(e){
        if(!ignore){ setError(e.message) }
      }finally{
        if(!ignore){ setLoading(false) }
      }
    }
    load()
    return () => { ignore = true }
  }, [])

  async function fetchAllRoutes(){
    setLoading(true)
    setError("")
    try{
      const res = await fetch(`${apiBase}/all`)
      const data = await res.json()
      if(!res.ok){ throw new Error(data?.message || 'Failed to load routes') }
      setBuses(data.buses || [])
      setSuggestions([])
    }catch(e){
      setError(e.message)
    }finally{
      setLoading(false)
    }
  }

  async function handleSearch(){
    if(!canSearch) return
    setLoading(true)
    setError("")
    setBuses([])
    setSuggestions([])
    try{
      const params = new URLSearchParams({ from, to, date, sort_by: sortBy })
      if(busType) params.append('bus_type', busType)
      if(operator) params.append('operator', operator)
      if(priceMin) params.append('price_min', priceMin)
      if(priceMax) params.append('price_max', priceMax)
      const res = await fetch(`${apiBase}/search?${params.toString()}`)
      const data = await res.json()
      if(!res.ok){
        throw new Error(data?.message || 'Search failed')
      }
      setBuses(data.buses || [])
      setSuggestions(data.suggestions || [])
    }catch(e){
      setError(e.message)
    }finally{
      setLoading(false)
    }
  }

  async function openSeatLayout(routeId){
    if(!date) return
    setLayoutOpen(true)
    setLayoutData(null)
    try{
      const res = await fetch(`${apiBase}/seat-layout/${routeId}?date=${encodeURIComponent(date)}`)
      const data = await res.json()
      if(!res.ok){
        throw new Error(data?.message || 'Failed to load seat layout')
      }
      setLayoutData(data)
    }catch(e){
      setLayoutData({ error: e.message })
    }
  }

  return (
    <div className="container" style={{maxWidth:'1000px'}}>
      <div className="intro1">Search Buses</div>
      <div className="formClass">
        <div className="form">
          <select value={from} onChange={e=>setFrom(e.target.value)}>
            <option value="">Select From</option>
            {stations.map((s) => (
              <option key={`from-${s}`} value={s}>{s}</option>
            ))}
          </select>
        </div>
        <div className="form">
          <select value={to} onChange={e=>setTo(e.target.value)}>
            <option value="">Select To</option>
            {stations.map((s) => (
              <option key={`to-${s}`} value={s}>{s}</option>
            ))}
          </select>
        </div>
        <div className="form">
          <input type="date" placeholder="Travel Date" value={date} onChange={e=>setDate(e.target.value)} />
        </div>
        <div className="form" style={{display:'flex', gap:'0.5rem', flexWrap:'wrap'}}>
          <select value={busType} onChange={e=>setBusType(e.target.value)} style={{padding:'0.5rem'}}>
            <option value="">All Types</option>
            <option value="AC">AC</option>
            <option value="Non-AC">Non-AC</option>
          </select>
          <input placeholder="Operator (e.g., Green Line)" value={operator} onChange={e=>setOperator(e.target.value)} style={{width:'auto'}}/>
          <input placeholder="Min Price" value={priceMin} onChange={e=>setPriceMin(e.target.value)} style={{width:'120px'}}/>
          <input placeholder="Max Price" value={priceMax} onChange={e=>setPriceMax(e.target.value)} style={{width:'120px'}}/>
          <select value={sortBy} onChange={e=>setSortBy(e.target.value)} style={{padding:'0.5rem'}}>
            <option value="price">Sort by Price</option>
            <option value="rating">Sort by Rating</option>
            <option value="departure">Sort by Departure</option>
          </select>
        </div>
        <div className="buttons-hub">
          <button disabled={!canSearch || loading} onClick={handleSearch} className="home-button">
            {loading ? 'Searching...' : 'Search'}
          </button>
          <button className="back-button" onClick={() => { setFrom(""); setTo(""); setDate(""); setBusType(""); setOperator(""); setPriceMin(""); setPriceMax(""); }}>
            Reset
          </button>
          <button className="registration-button" disabled={loading} onClick={fetchAllRoutes}>
            {loading ? 'Loading...' : 'Show All Routes'}
          </button>
           <button className="registration-button"  onClick={() => navigate("/passenger")}>
            Back
          </button>
        </div>
      </div>

      {error && <div style={{color:'red'}}>{error}</div>}

      {buses.length > 0 && (
        <div className="table-container" style={{marginTop:'1rem'}}>
          <table>
            <thead>
              <tr>
                <th>Operator</th>
                <th>Route</th>
                <th>Departure</th>
                <th>Type</th>
                <th>Seats</th>
                <th>Fare</th>
                <th>Rating</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody>
              {buses.map((b) => (
                <tr key={b.id}>
                  <td>{b.operator}</td>
                  <td>{b.from} → {b.to}</td>
                  <td>{b.departure_time}</td>
                  <td>{b.bus_type}</td>
                  <td>{b.seat_availability}</td>
                  <td>৳{b.fare}</td>
                  <td>{b.rating}</td>
                  <td>
                    <button className="registration-button" onClick={() => openSeatLayout(b.id)}>View Seats</button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {buses.length === 0 && suggestions.length > 0 && (
        <div style={{marginTop:'1rem', width:'100%'}}>
          <div className="intro1" style={{fontSize:'1.5rem'}}>No exact matches. Try these:</div>
          <div className="table-container" style={{marginTop:'0.5rem'}}>
            <table>
              <thead>
                <tr>
                  <th>Operator</th>
                  <th>Route</th>
                  <th>Departure</th>
                  <th>Seats</th>
                </tr>
              </thead>
              <tbody>
                {suggestions.map((s) => (
                  <tr key={s.id}>
                    <td>{s.operator}</td>
                    <td>{s.route}</td>
                    <td>{s.time}</td>
                    <td>{s.capacity}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      <SeatLayoutModal open={layoutOpen} onClose={()=>setLayoutOpen(false)} data={layoutData} />
    </div>
  )
}

export default BusRoutes