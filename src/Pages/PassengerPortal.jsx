/**
 * Author: Imtiaz Ahmed 2013552642
 */
import { useNavigate } from "react-router-dom";
import '../App.css'
function PassengerPortal() {
  const navigate = useNavigate();

  return (
    <div className="container">
        <h1>Passenger Portal</h1>


      <button className="login1-button" onClick={() => navigate("/passenger/login")}>Login</button>

      <button className="registration1-button" onClick={() => navigate("/passenger/registration")}>Registration</button>

      <button className="home-button" onClick={() => navigate("/")}>Home Page</button>

    </div>
  );
}

export default PassengerPortal;
