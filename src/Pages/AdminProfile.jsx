/**
 * Author: Imtiaz Ahmed 2013552642
 */
import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import '../App.css'

function AdminProfile() {
    const navigate = useNavigate();
    const [username, setUsername] = useState("");

    useEffect(() => {
        const savedUsername = localStorage.getItem("username");
        const token = localStorage.getItem("token");

        if (!token) {
            navigate("/admin/login");
            return;
        }

        setUsername(savedUsername);
    }, []);
    // const Susername = localStorage.getItem("username");

    const logout = () => {
        localStorage.removeItem("token");
        localStorage.removeItem("username");

        navigate("/admin/login");
    };

    return (
        <div className="container">
            <h1>Welcome, {username}</h1>
            <div className="buttons">
                <button className="logout-button" onClick={logout}>Logout</button>
                <div className="buttons1">
                <button className="button" onClick={() => navigate("/admin/profile/assign_driver")}>
                    Assign Driver
                </button>
            </div>
            </div>
        </div>
    );
}

export default AdminProfile;
