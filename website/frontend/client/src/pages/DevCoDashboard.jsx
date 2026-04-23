import { useEffect, useMemo, useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import Box from '@mui/material/Box';
import NavBar from '../components/NavBar';
import Verified from '../components/Verified';

function DevCoDashboard() {
    const navigate = useNavigate();
    const location = useLocation();
    const [account, setAccount] = useState(() => {
        const storedUser = localStorage.getItem('user');
        return storedUser ? JSON.parse(storedUser) : null;
    });
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState('');

    const email = useMemo(() => {
        if (location.state?.email) {
            return location.state.email;
        }
        if (account?.email) {
            return account.email;
        }
        const storedEmail = localStorage.getItem('accountEmail');
        return storedEmail || '';
    }, [account, location.state]);

    useEffect(() => {
        if (!email) {
            setError('No account email found. Please login again.');
            return;
        }

        localStorage.setItem('accountEmail', email);

        const fetchStatus = async () => {
            setIsLoading(true);
            setError('');

            try {
                const res = await fetch(`/api/auth/verify-status?email=${encodeURIComponent(email)}`);
                const payload = await res.json().catch(() => ({}));

                if (!res.ok) {
                    setError(payload?.message || 'Unable to load verification status.');
                    return;
                }

                const nextAccount = {
                    id: account?.id ?? null,
                    name: account?.name ?? '',
                    email,
                    verified: Boolean(payload?.verified),
                };

                setAccount(nextAccount);
                localStorage.setItem('user', JSON.stringify(nextAccount));
            } catch (_err) {
                setError('Unable to reach server.');
            } finally {
                setIsLoading(false);
            }
        };

        fetchStatus();
    }, [email]);

    return (
        <>
            <NavBar buttonLabel="Logout" buttonAction={() => {
                localStorage.removeItem('token');
                localStorage.removeItem('user');
                localStorage.removeItem('accountEmail');
                navigate('/');
            }} />
            <Box sx={{ maxWidth: 680, margin: '40px auto', px: 2 }}>
                <Verified account={account} isLoading={isLoading} error={error} />
            </Box>
        </>
    );
}

export default DevCoDashboard;