import { BrowserRouter, Routes, Route } from 'react-router-dom'
import WebSocketVerifyPage from './pages/WebSocketVerifyPage'
import FakeCompanyLandingPage from './pages/FakeCompanyLandingPage'

function App() {
    return (
        <BrowserRouter>
            <Routes>
                <Route path="/" element={<FakeCompanyLandingPage />} />
                <Route path="/verify" element={<WebSocketVerifyPage />} />
                {/* Add more routes here */}
            </Routes>
        </BrowserRouter>
    )
}

export default App
