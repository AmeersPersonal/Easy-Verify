import './App.css'
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import WebSocketVerifyPage from './pages/WebSocketVerifyPage'

function App() {
    return (
        <BrowserRouter>
            <Routes>
                {/* <Route path="/" element={<FakeCompanyPage />} /> */}
                <Route path="/" element={<WebSocketVerifyPage />} />
                {/* Add more routes here */}
            </Routes>
        </BrowserRouter>
    )
}

export default App
