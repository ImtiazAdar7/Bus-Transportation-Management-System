/**
 * Author: Imtiaz Ahmed 2013552642
 */
import { useState } from 'react'
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import Homepage from './Pages/Homepage.jsx'
import PassengerLogin from './Pages/PassengerLogin.jsx'
import PassengerRegistration from './Pages/PassengerRegistration.jsx'
import AdminRegistration from './Pages/AdminRegistration.jsx'
import AdminLogin from './Pages/AdminLogin.jsx'
import PassengerPortal from './Pages/PassengerPortal.jsx'
import DriverPortal from './Pages/DriverPortal.jsx'
import AdminPortal from './Pages/AdminPortal.jsx'
import DriverLogin from './Pages/DriverLogin.jsx'
import DriverRegistration from './Pages/DriverRegistration.jsx'
import PassengerProfile from './Pages/PassengerProfile.jsx'
import AdminProfile from './Pages/AdminProfile.jsx'
import DriverProfile from './Pages/DriverProfile.jsx'
import AssignDriver from './Pages/AssignDriver.jsx'
import BusRoutes from './Pages/BusRoutes.jsx'
import Analytics from './Pages/Analytics.jsx'
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
          <Route path="/passenger/bus-routes" element={<BusRoutes />} />
          {/* Driver Route */}
          <Route path="/driver/login" element={<DriverLogin />} />
          <Route path="/driver/registration" element={<DriverRegistration />} />
          {/* Profile Route */}
          <Route path="/passenger/profile" element={<PassengerProfile />} />
          {/* Admin Route */}
          <Route path="/admin/profile" element={<AdminProfile />} />
          <Route path="/driver/profile" element={<DriverProfile />} />
          <Route path="/admin/profile/assign_driver" element={<AssignDriver />} />
          {/* Analytics Route */}
          <Route path="/analytics" element={<Analytics />} />

        </Routes>
      </BrowserRouter>
    </div>
  )
}

export default App
