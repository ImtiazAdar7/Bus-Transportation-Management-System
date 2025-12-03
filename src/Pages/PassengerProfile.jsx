/**
 * Author: Imtiaz Ahmed 2013552642
 */

import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import '../App.css'
function PassengerProfile() {
  const navigate = useNavigate();
  const [username, setUsername] = useState("");

  useEffect(() => {
    const savedUsername = localStorage.getItem("username");
    const token = localStorage.getItem("token");

    if (!token) {
      navigate("/passenger/login");
      return;
    }

    setUsername(savedUsername);
  }, []);

    const logout = () => {
        localStorage.removeItem("token");
        localStorage.removeItem("username");

        navigate("/passenger/login");
    };


  return (
    <div className="container">
      <h1>Welcome, {username}</h1>
      <div className="buttons1">
        <button className="button" onClick={() => navigate("/passenger/my-tickets")}>My Tickets</button>
        <button className="button" onClick={() => navigate("/passenger/bus-routes")}>Bus Routes</button>
        <button className="button" onClick={() => navigate("/passenger/")}>Back To Portal</button>
        <button className="logout-button" onClick={logout}>Logout</button>
      </div>
    </div>
  );
}

export default PassengerProfile;
