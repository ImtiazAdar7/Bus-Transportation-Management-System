/**
 * Author: Imtiaz Ahmed 2013552642
 */
import '../App.css'
import { useState } from 'react'
import { useNavigate } from 'react-router-dom'

function AdminLogin() {
    const navigate = useNavigate();
    const [form, setForm] = useState({
        username: "",
        password: "",
    });

    const handleChange = (e) => {
        setForm({...form, [e.target.name]: e.target.value});
    };

    const handleLogin = async () => {
        try {
            const response = await fetch("http://localhost:5000/api/admin/login", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify(form),
            });

            const data = await response.json();
            if(!response.ok){
                alert(data.message);
                return;
            }

            localStorage.setItem("token", data.token);
            localStorage.setItem("username", data.username);
            alert("Admin Login Successful!!!");
            navigate("/admin/profile");

        } catch(error) {
            console.error("Error: ", error);
            alert("Invalid credentials, please try again later!!!");
        }
    };

    const goBack = () => {
    const token = localStorage.getItem("token");

    if (!token) {
        navigate("/admin");
    } else {
        navigate(-1);
    }
};


    return (
        <div className="container">
            
            <div className="intro1">Admin Login</div> <br />
            <div className="formClass">
                <form className='form'>
                    <input name="username" type="text" placeholder="User Name" onChange={handleChange}/><br />
                    <input name="password" type="password" placeholder="Password" onChange={handleChange}/><br />
                </form>
                <button className="login-button" type="submit" onClick={handleLogin}>Login</button>
                <button className="back-button" onClick={goBack}>Back</button>
            </div>
        </div>
    )
}
export default AdminLogin

