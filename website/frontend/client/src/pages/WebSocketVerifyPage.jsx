import { useVerification } from "../features/wsVerification/Verification";
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';

function WebSocketVerifyPage() {
    const {startVerify, _, verifyStatus,isVerifying } = useVerification();

    function handleSubmit(event) {
        event.preventDefault();
        startVerify();
    }

    return (
        <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', minHeight: '100vh' }}>
          <img src="/icon.png" width={200} height={200} />
          <Typography variant="h4">Access Content Below</Typography>
          {isVerifying &&
            (verifyStatus ? (
              <Typography variant="h6">✅</Typography>
            ) : (
              <img src="/loading.svg" width={200} height={200} />
            ))}

            <Box
                component="form"
                onSubmit={handleSubmit}
                sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 3, textAlign: 'center' }}
            >
            <Button type="submit" variant="contained" size="large">Verify</Button>

            {isVerifying ? (
              verifyStatus ? (
                <Typography variant="body1" color="success.main">
                  Success!
                </Typography>
              ) : (
                <Typography variant="body1" color="text.secondary">
                  Verifying...
                </Typography>
              )
            ) : (
              <Typography variant="body1" color="primary">
                Click to Verify
              </Typography>
            )}
          </Box>
        </Box>
    );
}

export default WebSocketVerifyPage;
