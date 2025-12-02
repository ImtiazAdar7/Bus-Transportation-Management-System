/**
 * Author: Imtiaz Ahmed 2013552642
 */
import { useState } from 'react'
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import Homepage from './Pages/Homepage'
import PassengerLogin from './Pages/PassengerLogin'
import PassengerRegistration from './Pages/PassengerRegistration'
import AdminRegistration from './Pages/AdminRegistration'
import AdminLogin from './Pages/AdminLogin'
import PassengerPortal from './Pages/PassengerPortal'
import DriverPortal from './Pages/DriverPortal'
import AdminPortal from './Pages/AdminPortal'
import DriverLogin from './Pages/DriverLogin'
import DriverRegistration from './Pages/DriverRegistration'
import PassengerProfile from './Pages/PassengerProfile'
import AdminProfile from './Pages/AdminProfile'
import DriverProfile from './Pages/DriverProfile'
import AssignDriver from './Pages/AssignDriver'
import './App.css'

function App() {
  const [count, setCount] = useState(0)

  return (
    <div className='app-container'>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Homepage />} />
          {/* Passenger, Admin, Driver Portals*/}
          <Route path="/passenger" element={<PassengerPortal />} />
          <Route path="/admin" element={<AdminPortal />} />
          <Route path="/driver" element={<DriverPortal />} />
          {/* Admin Route */}
          <Route path="/admin/login" element={<AdminLogin />} />
          <Route path="/admin/registration" element={<AdminRegistration />} />
          {/* Passenger Route */}
          <Route path="/passenger/login" element={<PassengerLogin />} />
          <Route path="/passenger/registration" element={<PassengerRegistration />} />
          {/* Driver Route */}
          <Route path="/driver/login" element={<DriverLogin />} />
          <Route path="/driver/registration" element={<DriverRegistration />} />
          {/* Profile Route */}
          <Route path="/passenger/profile" element={<PassengerProfile />} />
          {/* Admin Route */}
          <Route path="/admin/profile" element={<AdminProfile />} />
          <Route path="/driver/profile" element={<DriverProfile />} />
          <Route path="/admin/profile/assign_driver" element={<AssignDriver />} />

        </Routes>
      </BrowserRouter>
    </div>
  )
}

export default App
