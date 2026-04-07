import { useState } from "react";
import { useVerification } from "../features/wsVerification/Verification";
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';

function WebSocketVerifyPage() {
    const [name, setName] = useState("");
    const { clickText, startVerify } = useVerification();

    const textFieldSx = {
        input: { color: 'rgba(255,255,255,0.87)' },
        label: { color: 'rgba(255,255,255,0.87)' },
        '& .MuiOutlinedInput-notchedOutline': { borderColor: 'rgba(255,255,255,0.5)' },
        '@media (prefers-color-scheme: light)': {
            input: { color: '#213547' },
            label: { color: '#213547' },
            '& .MuiOutlinedInput-notchedOutline': { borderColor: 'rgba(0,0,0,0.23)' },
        }
    };

    function changeName(event) {
        console.log("Name input changed:", event.target.value);
        setName(event.target.value);
    }

    function handleSubmit(event) {
        event.preventDefault();
        startVerify(name);
    }

    return (
        <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', minHeight: '100vh' }}>
            <Box
                component="form"
                onSubmit={handleSubmit}
                sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 3, textAlign: 'center' }}
            >
                <img src="/icon.png" width={200} height={200} />
                <Typography variant="h4">Access Content Below</Typography>
                <TextField
                    name="name"
                    label="Enter your name"
                    value={name}
                    onChange={changeName}
                    sx={textFieldSx}
                />
                <Button type="submit" variant="contained" size="large">Verify</Button>
                {clickText && <Typography variant="h6">{clickText}</Typography>}
            </Box>
        </Box>
    );
}

export default WebSocketVerifyPage;
