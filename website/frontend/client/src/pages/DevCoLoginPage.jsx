import LoginForm from '../components/login/LoginForm';
import NavBar from '../components/NavBar';
import { useNavigate } from 'react-router-dom';

function DevCoLoginPage() {
    const navigate = useNavigate();

    return <>
        <NavBar buttonLabel="Landing Page" buttonAction={() => navigate('/')} />
        <LoginForm/>
    </>
}

export default DevCoLoginPage;