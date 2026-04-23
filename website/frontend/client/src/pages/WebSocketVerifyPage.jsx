import { Verifier } from "../features/wsVerification/Verification";
import Box from "@mui/material/Box";
import Typography from "@mui/material/Typography";
import Button from "@mui/material/Button";
import { useEffect, useRef, useState } from 'react';
import Card from "@mui/material/Card";
import { useLocation } from 'react-router-dom';


function WebSocketVerifyPage() {
    const location = useLocation();
    const storedUser = JSON.parse(localStorage.getItem('user') || '{}');
    const email = location.state?.email || storedUser?.email || localStorage.getItem('accountEmail') || 'unknown';
    const userId = location.state?.userId ?? storedUser?.id ?? null;
    const isUserIdConfigured = userId !== null && typeof userId !== 'undefined';
    const [submitError, setSubmitError] = useState('');

    const isVerifying = false;
    const isSocketOpen = false;
    const verifyStatus = false;

    const verifier = useRef(null);

    function handleSubmit(event) {
        event.preventDefault();
        setSubmitError('');

        if (!isUserIdConfigured) {
            setSubmitError('Please log in before verifying');
            return;
        }

        try {
            verifier.current = new Verifier();
            verifier.current.startConnect(String(userId));
            window.location.href = "easy-verify://verifyDemoClient";

        } catch (error) {
            console.log(error);
        }

    }
    useEffect(() => {

    }, [verifier.current]);

    return (
        <Box
            sx={{
                display: "flex",
                flexDirection: "column",
                alignItems: "center",
                justifyContent: "center",
                minHeight: "100vh",
            }}
        >
            <img src="/icon.png" width={200} height={200} />
            <Typography variant="h4">Access Content Below</Typography>
            <Card sx={{
                margin: '25px auto',
                padding: '15px',
                bgcolor: '#121212',
                color: '#f5f5f5',
            }}>
                <Typography variant="h5">This verification will use the email address: {email}</Typography>
            </Card>
            {isVerifying &&
                isSocketOpen &&
                (verifyStatus ? (
                    <Typography variant="h6">✅</Typography>
                ) : (
                    <img src="/loading.svg" width={200} height={200} />
                ))}

            <Box
                component="form"
                onSubmit={handleSubmit}
                sx={{
                    display: "flex",
                    flexDirection: "column",
                    alignItems: "center",
                    gap: 3,
                    textAlign: "center",
                }}
            >
                <Button type="submit" variant="contained" size="large">
                    Verify
                </Button>

                {submitError && (
                    <Typography variant="body1" color="error.main">
                        {submitError}
                    </Typography>
                )}

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
