import { useEffect, useState } from "react"
import {
  BarChart,
  Bar,
  PieChart,
  Pie,
  Cell,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts"
import { useNavigate } from "react-router-dom"

const COLORS = ["#0088FE", "#00C49F", "#FFBB28", "#FF8042", "#8884d8", "#82ca9d"]

const Analytics = () => {
  const navigate = useNavigate()
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState("")
  const [stats, setStats] = useState(null)

  useEffect(() => {
    let ignore = false
    async function fetchStats() {
      setLoading(true)
      setError("")
      try {
        const res = await fetch("/api/analytics/stats")
        const data = await res.json()
        if (!res.ok) {
          throw new Error(data?.message || "Failed to load analytics")
        }
        if (!ignore) {
          setStats(data)
        }
      } catch (e) {
        if (!ignore) {
          setError(e.message)
        }
      } finally {
        if (!ignore) {
          setLoading(false)
        }
      }
    }
    fetchStats()
    return () => {
      ignore = true
    }
  }, [])

  if (loading) {
    return (
      <div className="container" style={{ maxWidth: "1200px" }}>
        <div className="intro1">Analytics Dashboard</div>
        <div>Loading...</div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="container" style={{ maxWidth: "1200px" }}>
        <div className="intro1">Analytics Dashboard</div>
        <div style={{ color: "red" }}>{error}</div>
        <button className="back-button" onClick={() => navigate(-1)}>
          Back
        </button>
      </div>
    )
  }

  return (
    <div className="container" style={{ maxWidth: "1200px", minHeight: "90vh" }}>
      <div className="intro1" style={{ marginBottom: "1rem" }}>
        Analytics Dashboard
      </div>

      {/* Summary Cards */}
      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(auto-fit, minmax(200px, 1fr))",
          gap: "1rem",
          marginBottom: "2rem",
          width: "100%",
        }}
      >
        <div
          style={{
            background: "rgba(0, 136, 254, 0.2)",
            padding: "1rem",
            borderRadius: "0.5rem",
            textAlign: "center",
          }}
        >
          <div style={{ fontSize: "2rem", fontWeight: "bold", color: "#0088FE" }}>
            {stats?.total_routes || 0}
          </div>
          <div style={{ fontSize: "1rem", color: "#003333" }}>Available Routes</div>
        </div>
        <div
          style={{
            background: "rgba(0, 196, 159, 0.2)",
            padding: "1rem",
            borderRadius: "0.5rem",
            textAlign: "center",
          }}
        >
          <div style={{ fontSize: "2rem", fontWeight: "bold", color: "#00C49F" }}>
            {stats?.top_destinations?.length || 0}
          </div>
          <div style={{ fontSize: "1rem", color: "#003333" }}>Popular Destinations</div>
        </div>
      </div>

      {/* Charts Grid */}
      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(auto-fit, minmax(300px, 1fr))",
          gap: "2rem",
          width: "100%",
        }}
      >
        {/* Popular Routes Chart */}
        <div
          style={{
            background: "rgba(255,255,255,0.15)",
            backdropFilter: "blur(10px)",
            padding: "1rem",
            borderRadius: "0.5rem",
          }}
        >
          <h3 style={{ textAlign: "center", color: "#003333" }}>Most Popular Routes</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={stats?.top_routes?.slice(0, 8) || []}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="route" angle={-45} textAnchor="end" height={100} />
              <YAxis />
              <Tooltip />
              <Legend />
              <Bar dataKey="count" fill="#0088FE" name="Available Buses" />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Bus Type Distribution */}
        <div
          style={{
            background: "rgba(255,255,255,0.15)",
            backdropFilter: "blur(10px)",
            padding: "1rem",
            borderRadius: "0.5rem",
          }}
        >
          <h3 style={{ textAlign: "center", color: "#003333" }}>Bus Type Availability</h3>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={stats?.bus_type_distribution || []}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ type, count }) => `${type}: ${count}`}
                outerRadius={80}
                fill="#8884d8"
                dataKey="count"
              >
                {(stats?.bus_type_distribution || []).map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>

        {/* Top Destinations */}
        <div
          style={{
            background: "rgba(255,255,255,0.15)",
            backdropFilter: "blur(10px)",
            padding: "1rem",
            borderRadius: "0.5rem",
          }}
        >
          <h3 style={{ textAlign: "center", color: "#003333" }}>Popular Destinations</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={stats?.top_destinations || []}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="destination" angle={-45} textAnchor="end" height={80} />
              <YAxis />
              <Tooltip />
              <Legend />
              <Bar dataKey="count" fill="#00C49F" name="Routes Available" />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Fare Comparison by Operator */}
        <div
          style={{
            background: "rgba(255,255,255,0.15)",
            backdropFilter: "blur(10px)",
            padding: "1rem",
            borderRadius: "0.5rem",
          }}
        >
          <h3 style={{ textAlign: "center", color: "#003333" }}>Average Fare by Operator</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={stats?.fare_comparison || []}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="operator" angle={-45} textAnchor="end" height={80} />
              <YAxis />
              <Tooltip />
              <Legend />
              <Bar dataKey="avg_fare" fill="#FFBB28" name="Avg Fare (৳)" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Top Routes Table */}
      <div style={{ marginTop: "2rem", width: "100%" }}>
        <h3 style={{ textAlign: "center", color: "#003333" }}>All Popular Routes</h3>
        <div className="table-container">
          <table>
            <thead>
              <tr>
                <th>Route</th>
                <th>Available Buses</th>
              </tr>
            </thead>
            <tbody>
              {(stats?.top_routes || []).map((route, idx) => (
                <tr key={idx}>
                  <td>{route.route}</td>
                  <td>{route.count}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      <div className="buttons-hub" style={{ marginTop: "2rem" }}>
        <button className="back-button" onClick={() => navigate(-1)}>
          Back
        </button>
      </div>
    </div>
  )
}

export default Analytics
