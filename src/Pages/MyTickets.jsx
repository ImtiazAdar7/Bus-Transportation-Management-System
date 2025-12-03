/**
 * Author: Imtiaz Ahmed 2013552642
 */
import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import '../App.css'

const apiBase = "/api/passenger";

function MyTickets() {
  const navigate = useNavigate();
  const [bookings, setBookings] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) {
      navigate("/passenger/login");
      return;
    }
    fetchBookings();
  }, [navigate]);

  const fetchBookings = async () => {
    const token = localStorage.getItem("token");
    if (!token) {
      navigate("/passenger/login");
      return;
    }

    setLoading(true);
    setError("");

    try {
      const response = await fetch(`${apiBase}/bookings`, {
        method: "GET",
        headers: {
          "Authorization": `Bearer ${token}`,
          "Content-Type": "application/json"
        }
      });

      // Check if response is JSON
      const contentType = response.headers.get("content-type");
      if (!contentType || !contentType.includes("application/json")) {
        const text = await response.text();
        throw new Error(`Server returned non-JSON response: ${text.substring(0, 100)}`);
      }

      const data = await response.json();
      
      if (!response.ok) {
        throw new Error(data.message || "Failed to fetch bookings");
      }

      setBookings(data.bookings || []);
    } catch (e) {
      setError(e.message || "Failed to fetch bookings. Please try again.");
      console.error("Error fetching bookings:", e);
    } finally {
      setLoading(false);
    }
  };

  const formatTime = (timeStr) => {
    if (!timeStr) return "N/A";
    // Handle time format (HH:MM:SS or HH:MM)
    return timeStr.substring(0, 5);
  };

  return (
    <div className="container" style={{maxWidth: '1000px'}}>
      <div className="intro1">My Tickets</div>

      <div className="buttons-hub" style={{marginBottom: '1rem'}}>
        <button className="back-button" onClick={() => navigate("/passenger/profile")}>
          Back to Profile
        </button>
        <button className="registration-button" onClick={fetchBookings} disabled={loading}>
          {loading ? 'Refreshing...' : 'Refresh'}
        </button>
      </div>

      {error && (
        <div style={{color: 'red', marginBottom: '1rem', padding: '0.5rem', background: '#ffebee', borderRadius: '0.25rem'}}>
          {error}
        </div>
      )}

      {loading && bookings.length === 0 ? (
        <div className="intro1">Loading your tickets...</div>
      ) : bookings.length === 0 ? (
        <div className="intro1" style={{marginTop: '2rem'}}>
          No bookings found. <br />
          <button className="registration-button" onClick={() => navigate("/passenger/bus-routes")} style={{marginTop: '1rem'}}>
            Book a Ticket
          </button>
        </div>
      ) : (
        <div className="table-container" style={{marginTop: '1rem'}}>
          <table>
            <thead>
              <tr>
                <th>Booking ID</th>
                <th>Operator</th>
                <th>Route</th>
                <th>Departure Time</th>
                <th>Price</th>
                <th>Capacity</th>
              </tr>
            </thead>
            <tbody>
              {bookings.map((booking) => (
                <tr key={booking.booking_id}>
                  <td>#{booking.booking_id}</td>
                  <td>{booking.operator || 'N/A'}</td>
                  <td>{booking.route || 'N/A'}</td>
                  <td>{formatTime(booking.departure_time)}</td>
                  <td>৳{booking.price}</td>
                  <td>{booking.capacity || 'N/A'}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

export default MyTickets;

