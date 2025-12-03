/**
 * Author: Imtiaz Ahmed 2013552642
 */
import { useNavigate } from "react-router-dom";
import '../App.css'
function DriverPortal() {
  const navigate = useNavigate();

  return (
    <div className="container">
      <h1>Driver Portal</h1>

      <button className="login1-button" onClick={() => navigate("/driver/login")}>Login</button>
      <button className="registration1-button" onClick={() => navigate("/driver/registration")}>Registration</button>
      <button className="home-button" onClick={() => navigate("/")}>Home Page</button>
    </div>
  );
}

export default DriverPortal;
