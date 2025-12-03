/**
 * Author: Imtiaz Ahmed 2013552642
 */
import '../App.css'
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
function AdminRegistration() {
const navigate = useNavigate();
    const [form, setForm] = useState({
        first_name: "",
        last_name: "",
        age: "",
        username: "",
        website_auth_code: "",
        dob: "",
        gender: "",
        password: "",
        confirm_password: "",
    });

    const handleChange = (e) => {
        setForm({ ...form, [e.target.name]: e.target.value });
    };

    const handleRegister = async () => {
        if (form.password !== form.confirm_password) {
            alert("Passwords did not match!!!");
            return;
        }

        try {
            for (const key in form) {
                if (!form[key]) {
                    alert(`${key} is required`);
                    return;
                }
            }

            const response = await fetch("http://localhost:5000/api/admin/register", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(form),
            });

            const data = await response.json();
            if (!response.ok) {
                alert(data.message);
                return;
            }
            alert("Admin Registration Successful!!!");
            navigate("/admin/login");

        } catch (error) {
            console.error("Error: ", error);
            alert("Please check the form and try again later!!!");
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
            
            <div className="intro1">Admin Registration</div> <br />
            <div className="formClass">
                <form className='form'>
                    <input name='first_name' type="text" placeholder="First Name" onChange={handleChange} /><br />
                    <input name='last_name' type="text" placeholder="Last Name" onChange={handleChange} /><br />
                    <input name='age' type="text" placeholder="Age" onChange={handleChange} /><br />
                    <input name='username' type="text" placeholder="User Name" onChange={handleChange} /><br />
                    <input name='website_auth_code' type="text" placeholder="Website Authentication Code" onChange={handleChange} /><br />
                    <input name='dob' type="date" placeholder="Date of Birth" onChange={handleChange} /><br />
                    <input name='gender' type="text" placeholder="Gender" onChange={handleChange} /><br />
                    <input name='password' type="password" placeholder="Password" onChange={handleChange} /><br />
                    <input name='confirm_password' type="password" placeholder="Confirm Password" onChange={handleChange} /><br />
                </form>
                <button className="registration-button" type="submit" onClick={handleRegister}>Register</button>
                <button className="back-button" onClick={goBack}>Back</button>
            </div>
        </div>
    )
}
export default AdminRegistration
