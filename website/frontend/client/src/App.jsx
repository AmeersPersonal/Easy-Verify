import { BrowserRouter, Routes, Route } from 'react-router-dom'
import WebSocketVerifyPage from './pages/WebSocketVerifyPage'
import DevCoLandingPage from './pages/DevCoLandingPage'
import DevCoLoginPage from './pages/DevCoLoginPage'
import DevCoCreateAccountPage from './pages/DevCoCreateAccountPage'

function App() {
    return (
        <BrowserRouter>
            <Routes>
                <Route path="/" element={<DevCoLandingPage />} />
                <Route path="/login" element={<DevCoLoginPage />} />
                <Route path="/verify" element={<WebSocketVerifyPage />} />
                <Route path="/create-account" element={<DevCoCreateAccountPage />} />
                {/* Add more routes here */}
            </Routes>
        </BrowserRouter>
    )
}

export default App
