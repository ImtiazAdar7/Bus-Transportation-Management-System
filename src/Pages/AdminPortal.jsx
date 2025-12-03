/**
 * Author: Imtiaz Ahmed 2013552642
 */
import { useNavigate } from "react-router-dom";
import '../App.css'
function AdminPortal() {
  const navigate = useNavigate();

  return (
    <div className="container">
        <h1>Admin Portal</h1>

      <button className="login1-button" onClick={() => navigate("/admin/login")}>Login</button>
      <button className="registration1-button" onClick={() => navigate("/admin/registration")}>Registration</button>
      <button className="home-button" onClick={() => navigate("/")}>Home Page</button>
    </div>
  );
}

export default AdminPortal;
