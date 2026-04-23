import { useNavigate } from 'react-router-dom';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import Typography from '@mui/material/Typography';
import Stack from '@mui/material/Stack';
import Button from '@mui/material/Button';
import Chip from '@mui/material/Chip';
import CircularProgress from '@mui/material/CircularProgress';
import Alert from '@mui/material/Alert';

export default function Verified({ account, isLoading, error }) {
    const navigate = useNavigate();
    const cardSx = {
        bgcolor: '#121212',
        color: '#f5f5f5',
        border: '1px solid rgba(255,255,255,0.12)',
        borderRadius: 2,
    };

    if (isLoading) {
        return (
            <Card sx={cardSx}>
                <CardContent>
                    <Stack direction="row" spacing={2} alignItems="center">
                        <CircularProgress size={20} sx={{ color: '#90caf9' }} />
                        <Typography variant="body1" sx={{ color: '#f5f5f5' }}>
                            Loading account status...
                        </Typography>
                    </Stack>
                </CardContent>
            </Card>
        );
    }

    return (
        <Card sx={cardSx}>
            <CardContent>
                <Stack spacing={2}>
                    <Typography variant="h5" sx={{ color: '#f5f5f5' }}>
                        Account Dashboard
                    </Typography>

                    {error && (
                        <Alert
                            severity="error"
                            sx={{
                                bgcolor: 'rgba(211, 47, 47, 0.15)',
                                color: '#ffcdd2',
                                border: '1px solid rgba(244, 67, 54, 0.35)',
                                '& .MuiAlert-icon': { color: '#ef5350' },
                            }}
                        >
                            {error}
                        </Alert>
                    )}

                    <Typography variant="body1" sx={{ color: '#e0e0e0' }}>
                        Verification Status:
                    </Typography>

                    <Chip
                        color={account?.verified ? 'success' : 'warning'}
                        label={account?.verified ? 'true' : 'false'}
                        sx={{
                            width: 'fit-content',
                            textTransform: 'lowercase',
                            fontWeight: 600,
                            '.MuiChip-label': { color: '#101010' },
                        }}
                    />

                    <Button
                        variant="contained"
                        sx={{ bgcolor: '#1e88e5', '&:hover': { bgcolor: '#1565c0' } }}
                        onClick={() => navigate('/verify', { state: { email: account?.email } })}
                    >
                        Verify Account
                    </Button>
                </Stack>
            </CardContent>
        </Card>
    );
}
