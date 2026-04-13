import CreateAccountForm from '../components/login/CreateAccountForm';
import NavBar from '../components/NavBar';
import { useNavigate, useLocation } from 'react-router-dom';

function DevCoCreateAccountPage() {
    const navigate = useNavigate();
    const { state } = useLocation();

    return <>
        <NavBar buttonLabel="Landing Page" buttonAction={() => navigate('/')} />
        <CreateAccountForm prefillEmail={state?.email} />
    </>
}

export default DevCoCreateAccountPage;