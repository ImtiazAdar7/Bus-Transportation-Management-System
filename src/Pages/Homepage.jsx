/**
 * Author: Imtiaz Ahmed 2013552642
 */
import { BrowserRouter, Route, Routes, useNavigate } from "react-router-dom"
import PassengerPortal from "./PassengerPortal"
import AdminPortal from "./AdminPortal"
import '../App.css'
function Homepage(){
    const navigate = useNavigate();

    return (<>


        <div className="container">
            <div className="intro">
                <h2>Bus Management System</h2>
            </div>
            <div className="pagesLink">
                <div className="button">
                        <button className="passenger-portal" onClick={() => navigate("/passenger")}>Passenger Portal</button>
                    </div>
                    <div className="button">
                        <button className="admin-portal" onClick={() => navigate("/admin")}>Admin Portal</button>
                    </div>
                    <div className="button">
                        <button className="driver-portal" onClick={() => navigate("/driver")}>Driver Portal</button>
                    </div>

                </div>
        </div>
    </>)
}
export default Homepage