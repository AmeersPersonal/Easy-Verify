import { useState } from "react";
import { useNavigate } from "react-router-dom";
import Box from '@mui/material/Box';
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';
import Typography from '@mui/material/Typography';

export default function CreateAccountForm({ prefillEmail }) {
    const [email, setEmail] = useState(prefillEmail ?? "");
    const [password, setPassword] = useState("");
    const [confirmPassword, setConfirmPassword] = useState("");
    const [error, setError] = useState("");
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError("");

        if (password !== confirmPassword) {
            setError("Passwords do not match.");
            return;
        }

        navigate("/verify")

        // const res = await fetch("/api/create-account", {
        //     method: "POST",
        //     headers: { "Content-Type": "application/json" },
        //     body: JSON.stringify({ email, password }),
        // });

        // if (res.status === 201) {
        //     const { token } = await res.json();
        //     localStorage.setItem("token", token);
        //     navigate("/dashboard");
        // } else if (res.status === 409) {
        //     setError("An account with that email already exists.");
        // }
    };

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

    return (
        <Box
            component="form"
            onSubmit={handleSubmit}
            sx={{ display: 'flex', flexDirection: 'column', gap: 2, width: 360, margin: '80px auto'}}
        >
            <Typography variant="h5">Create Account</Typography>
            {error && <Typography color="error" variant="body2">{error}</Typography>}
            <TextField
                label="Email"
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
                sx={textFieldSx}
            />
            <TextField
                label="Password"
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                sx={textFieldSx}
            />
            <TextField
                label="Confirm Password"
                type="password"
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                required
                sx={textFieldSx}
            />
            <Button type="submit" variant="contained">Create Account</Button>
        </Box>
    );
}