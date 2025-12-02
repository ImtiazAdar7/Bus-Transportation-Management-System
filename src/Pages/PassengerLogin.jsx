import '../App.css'
import { useState } from 'react'
import { useNavigate } from 'react-router-dom'

function PassengerLogin() {
    const navigate = useNavigate();
    const [form, setFrom] = useState({
        email: "",
        password: "",
    });

    const handleChange = (e) => {
        setFrom({ ...form, [e.target.name]: e.target.value });
    };

    const handleLogin = async () => {
        try {
            const response = await fetch("http://localhost:5000/api/passenger/login", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(form),
            });
            const data = await response.json();
            if (!response.ok) {
                alert(data.message);
                return;
            }
            localStorage.setItem("token", data.token);
            localStorage.setItem("username", data.username);
            alert("Login Successful!!!");
            navigate("/passenger/profile");

        }
        catch (error) {
            console.error("Error: ", error);
            alert("Invalid credentials, please try again later!!!");
        }
    };

    const goBack = () => {
        const token = localStorage.getItem("token");

        if (!token) {
            navigate("/passenger");
        } else {
            navigate(-1);
        }
    };


    return (
        <>
            <div className="container">

                <div className="intro">Passenger Login</div> <br></br>
                <div className="formClass">
                    <form className='form'>
                        <input name="email" type="email" placeholder="Email" onChange={handleChange} /><br />
                        <input name="password" type="password" placeholder="Password" onChange={handleChange} /><br />
                    </form>
                    <div className="button-group">
                        <button className="login-button" type="submit" onClick={handleLogin}>Login</button>
                        <button className="back-button" onClick={goBack}>Back</button>
                    </div>
                </div>
            </div>
        </>
    )
}
export default PassengerLogin
