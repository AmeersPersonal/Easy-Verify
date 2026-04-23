import { BrowserRouter, Routes, Route } from 'react-router-dom'
import WebSocketVerifyPage from './pages/WebSocketVerifyPage'
import DevCoLandingPage from './pages/DevCoLandingPage'
import DevCoLoginPage from './pages/DevCoLoginPage'
import DevCoCreateAccountPage from './pages/DevCoCreateAccountPage'
import DevCoDashboard from './pages/DevCoDashboard'

function App() {
    return (
        <BrowserRouter>
            <Routes>
                <Route path="/" element={<DevCoLandingPage />} />
                <Route path="/login" element={<DevCoLoginPage />} />
                <Route path="/dashboard" element={<DevCoDashboard />} />
                <Route path="/verify" element={<WebSocketVerifyPage />} />
                <Route path="/create-account" element={<DevCoCreateAccountPage />} />
            </Routes>
        </BrowserRouter>
    )
}

export default App
