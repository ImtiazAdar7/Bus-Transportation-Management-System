/**
 * Author: Imtiaz Ahmed 2013552642
 */
import { useState, useEffect } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import '../App.css'

const apiBase = "http://localhost:5000/api/passenger";

function Booking() {
  const navigate = useNavigate();
  const location = useLocation();
  const [routeData, setRouteData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [confirmed, setConfirmed] = useState(false);
  const [bookingSuccess, setBookingSuccess] = useState(false);

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) {
      navigate("/passenger/login");
      return;
    }

    const data = location.state?.routeData;
    if (!data) {
      navigate("/passenger/bus-routes");
      return;
    }
    setRouteData(data);
  }, [location, navigate]);

  const handleConfirm = async () => {
    if (!routeData) return;

    const token = localStorage.getItem("token");
    if (!token) {
      alert("Please login to continue");
      navigate("/passenger/login");
      return;
    }

    setLoading(true);
    setError("");

    try {
      const response = await fetch(`${apiBase}/booking`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify({
          bus_route_id: routeData.id,
          price: routeData.fare
        })
      });

      const data = await response.json();
      
      if (!response.ok) {
        throw new Error(data.message || "Failed to create booking");
      }

      setBookingSuccess(true);
      setConfirmed(true);
      alert("Booking confirmed successfully!");
      
      // Redirect to my tickets after 2 seconds
      setTimeout(() => {
        navigate("/passenger/my-tickets");
      }, 2000);
    } catch (e) {
      setError(e.message);
      alert(`Booking failed: ${e.message}`);
    } finally {
      setLoading(false);
    }
  };

  const handlePayment = () => {
    // Dummy payment button - just shows an alert
    alert("Payment gateway integration coming soon! Click 'Confirm Booking' to proceed.");
  };

  if (!routeData) {
    return (
      <div className="container">
        <div className="intro1">Loading...</div>
      </div>
    );
  }

  return (
    <div className="container" style={{maxWidth: '800px'}}>
      <div className="intro1">Booking Confirmation</div>
      
      <div className="formClass" style={{marginTop: '2rem'}}>
        <div style={{background: '#f5f5f5', padding: '1.5rem', borderRadius: '0.5rem', marginBottom: '1rem', color: '#1a1a1a'}}>
          <h2 style={{marginTop: 0, color: '#1a1a1a'}}>Bus Details</h2>
          <div style={{display: 'grid', gap: '0.75rem'}}>
            <div style={{display: 'flex', justifyContent: 'space-between', padding: '0.5rem 0', borderBottom: '1px solid #ddd', color: '#1a1a1a'}}>
              <strong style={{color: '#1a1a1a'}}>Operator:</strong>
              <span style={{color: '#1a1a1a'}}>{routeData.operator}</span>
            </div>
            <div style={{display: 'flex', justifyContent: 'space-between', padding: '0.5rem 0', borderBottom: '1px solid #ddd', color: '#1a1a1a'}}>
              <strong style={{color: '#1a1a1a'}}>Route:</strong>
              <span style={{color: '#1a1a1a'}}>{routeData.from} → {routeData.to}</span>
            </div>
            <div style={{display: 'flex', justifyContent: 'space-between', padding: '0.5rem 0', borderBottom: '1px solid #ddd', color: '#1a1a1a'}}>
              <strong style={{color: '#1a1a1a'}}>Departure Time:</strong>
              <span style={{color: '#1a1a1a'}}>{routeData.departure_time}</span>
            </div>
            <div style={{display: 'flex', justifyContent: 'space-between', padding: '0.5rem 0', borderBottom: '1px solid #ddd', color: '#1a1a1a'}}>
              <strong style={{color: '#1a1a1a'}}>Bus Type:</strong>
              <span style={{color: '#1a1a1a'}}>{routeData.bus_type}</span>
            </div>
            <div style={{display: 'flex', justifyContent: 'space-between', padding: '0.5rem 0', borderBottom: '1px solid #ddd', color: '#1a1a1a'}}>
              <strong style={{color: '#1a1a1a'}}>Available Seats:</strong>
              <span style={{color: '#1a1a1a'}}>{routeData.seat_availability}</span>
            </div>
            <div style={{display: 'flex', justifyContent: 'space-between', padding: '0.5rem 0', fontSize: '1.2rem', fontWeight: 'bold', color: '#1a1a1a'}}>
              <strong style={{color: '#1a1a1a'}}>Price:</strong>
              <span style={{color: '#1a1a1a'}}>৳{routeData.fare}</span>
            </div>
          </div>
        </div>

        {error && (
          <div style={{color: 'red', marginBottom: '1rem', padding: '0.5rem', background: '#ffebee', borderRadius: '0.25rem'}}>
            {error}
          </div>
        )}

        {bookingSuccess && (
          <div style={{color: 'green', marginBottom: '1rem', padding: '0.5rem', background: '#e8f5e9', borderRadius: '0.25rem'}}>
            Booking confirmed successfully! Redirecting to your tickets...
          </div>
        )}

        <div className="buttons-hub" style={{display: 'flex', gap: '1rem', flexWrap: 'wrap', justifyContent: 'center'}}>
          <button 
            className="registration-button" 
            onClick={handlePayment}
            disabled={confirmed || loading}
            style={{background: '#4CAF50'}}
          >
            Pay Now (Dummy)
          </button>
          <button 
            className="registration-button" 
            onClick={handleConfirm}
            disabled={confirmed || loading}
          >
            {loading ? 'Processing...' : confirmed ? 'Confirmed' : 'Confirm Booking'}
          </button>
          <button 
            className="back-button" 
            onClick={() => navigate("/passenger/bus-routes")}
            disabled={loading}
          >
            Cancel
          </button>
        </div>
      </div>
    </div>
  );
}

export default Booking;
