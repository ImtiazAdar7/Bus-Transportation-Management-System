/**
 * Author: Imtiaz Ahmed 2013552642
 */
import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import '../App.css'

function PassengerPortal() {
  const navigate = useNavigate();
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  useEffect(() => {
    const check = () => setIsLoggedIn(!!localStorage.getItem("token"));
    check();
    const onStorage = (e) => {
      if (e.key === "token") check();
    };
    window.addEventListener("storage", onStorage);
    return () => window.removeEventListener("storage", onStorage);
  }, []);

  const handleLogout = () => {
    try {
      localStorage.removeItem("token");
      localStorage.removeItem("username");
      setIsLoggedIn(false);
      // notify other tabs/windows about logout
      try {
        localStorage.setItem("__logout", Date.now().toString());
        localStorage.removeItem("__logout");
      } catch (err) {
        // ignore
      }
      navigate("/");
    } catch (err) {
      console.error("Logout error:", err);
    }
  };

  return (
    <div className="container">
        <h1>Passenger Portal</h1>

      {!isLoggedIn && (
        <>
          <button className="login1-button" onClick={() => navigate("/passenger/login")}>Login</button>

          <button className="registration1-button" onClick={() => navigate("/passenger/registration")}>Registration</button>
        </>
      )}

      {isLoggedIn && (
        <>
          <button className="home-button" onClick={handleLogout}>Logout</button>

          <button className="home-button" onClick={() => navigate("/passenger/bus-routes")}>Search Buses</button>

          <button className="home-button" onClick={() => navigate("/analytics")}>Analytics Dashboard</button>
        </>
      )}

      <button className="home-button" onClick={() => navigate("/")}>Home Page</button>

    </div>
  );
}

export default PassengerPortal;
