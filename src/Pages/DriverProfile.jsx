/**
 * Author: Imtiaz Ahmed 2013552642
 */
import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import '../App.css';

function DriverProfile() {
    const navigate = useNavigate();
    const [username, setUsername] = useState("");

    useEffect(() => {
        const token = localStorage.getItem("token");
        const savedUsername = localStorage.getItem("username");

        if (!token) {
            navigate("/driver/login");
            return;
        }

        setUsername(savedUsername);
    }, []);

    const logout = () => {
        localStorage.removeItem("token");
        localStorage.removeItem("username");
        navigate("/driver/login");
    };

    return (
        <div className="container">
            <h1>Welcome, {username}</h1>
            <div className="buttons1">
                <button className="button" onClick={logout}>Logout</button>
            </div>
        </div>
    );
}

export default DriverProfile;
