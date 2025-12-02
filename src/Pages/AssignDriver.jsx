/**
 * Author: Imtiaz Ahmed 2013552642
 */
import { useEffect, useState } from "react";

function AssignDriver() {
    const [drivers, setDrivers] = useState([]);

    useEffect(() => {
        const fetchDrivers = async () => {
            const response = await fetch("http://localhost:5000/api/admin/drivers");
            const data = await response.json();
            setDrivers(data.drivers);
        };
        fetchDrivers();
    }, []);

    const assignDriver = async (id) => {
    await fetch(`http://localhost:5000/api/admin/assign_driver/${id}`, { method: "POST" });
    alert("Driver assigned!");
    // Remove from local state
    setDrivers(drivers.filter((d) => d.id !== id));
};


    const deleteDriver = async (id) => {
        await fetch(`http://localhost:5000/api/admin/delete_driver/${id}`, { method: "DELETE" });
        setDrivers(drivers.filter((d) => d.id !== id));
        alert("Driver deleted!");
    };

    return (
        <div className="container">
            <h2>Assign Driver</h2>
            <div className="table-container">
                <table>
                    <thead>
                        <tr>
                            <th>Id</th>
                            <th>First Name</th>
                            <th>Last Name</th>
                            <th>Age</th>
                            <th>Username</th>
                            <th>Email</th>
                            <th>DOB</th>
                            <th>Gender</th>
                            <th>Assign</th>
                            <th>Delete</th>
                        </tr>
                    </thead>
                    <tbody>
                        {drivers.map((driver) => (
                            <tr key={driver.id}>
                                <td>{driver.id}</td>
                                <td>{driver.first_name}</td>
                                <td>{driver.last_name}</td>
                                <td>{driver.age}</td>
                                <td>{driver.username}</td>
                                <td>{driver.email}</td>
                                <td>{driver.dob}</td>
                                <td>{driver.gender}</td>
                                <td><button onClick={() => assignDriver(driver.id)}>✅</button></td>
                                <td><button onClick={() => deleteDriver(driver.id)}>❌</button></td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>

    );
}

export default AssignDriver;
