import Card from '@mui/material/Card';
import NavBar from '../components/NavBar';
import { useNavigate } from 'react-router-dom';
import CardContent from '@mui/material/CardContent';
import Stack from '@mui/material/Stack';
import Typography from '@mui/material/Typography';

function DevCoLandingPage() {
    const navigate = useNavigate();

    const cardSx = {
        bgcolor: '#121212',
        color: '#f5f5f5',
        border: '1px solid rgba(255,255,255,0.12)',
        borderRadius: 2,
        maxWidth: 680, 
        margin: '40px auto', 
        px: 2
    };

    return <>
        <NavBar buttonLabel="Login" buttonAction={() => navigate('/login')} />
        <Card sx={cardSx}>
            <CardContent>
                <Stack direction="row" spacing={2} alignItems="center">
                    <Typography variant="body1" sx={{ color: '#f5f5f5' }}>
                        This would be the website main page with information related to it.
                    </Typography>
                </Stack>
            </CardContent>
        </Card>
    </>
}

export default DevCoLandingPage;