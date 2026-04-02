import NavBar from '../components/NavBar';
import { useNavigate } from 'react-router-dom';

function DevCoLandingPage() {
    const navigate = useNavigate();

    return <>
        <NavBar buttonLabel="Login" buttonAction={() => navigate('/login')} />
    </>
}

export default DevCoLandingPage;