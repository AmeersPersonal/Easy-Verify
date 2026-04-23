import Card from '@mui/material/Card';
import NavBar from '../components/NavBar';
import { useNavigate } from 'react-router-dom';
import CardContent from '@mui/material/CardContent';
import Stack from '@mui/material/Stack';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';

function DevCoLandingPage() {
    const navigate = useNavigate();

    const cardSx = {
        bgcolor: '#121212',
        color: '#f5f5f5',
        border: '1px solid rgba(255,255,255,0.12)',
        borderRadius: 2,
        maxWidth: 1200,
        width: '100%',
        px: 2,
    };

    return <>
        <NavBar buttonLabel="Login" buttonAction={() => navigate('/login')} />
        <Box
            sx={{
                minHeight: 'calc(100vh - 64px)',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                px: 2,
            }}
        >
            <Card sx={cardSx}>
                <CardContent>
                    <Stack direction="row" spacing={2} alignItems="center" justifyContent="center" sx={{ width: '100%' }}>
                        <Typography variant="h3" sx={{ color: '#f5f5f5', textAlign: 'center', width: '100%' }}>
                            Website Main Page Contents...
                        </Typography>
                    </Stack>
                </CardContent>
            </Card>
        </Box>
    </>
}

export default DevCoLandingPage;