import { useState } from "react";
import { useNavigate } from "react-router-dom";
import Box from '@mui/material/Box';
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';
import Typography from '@mui/material/Typography';

export default function LoginForm() {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError("");

        const res = await fetch("/api/login", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email, password }),
        });

        if (res.status === 404) {
            navigate("/create-account", { state: { email } });
        }

        // if (res.status === 200) {
        //     const { token } = await res.json();
        //     localStorage.setItem("token", token);
        //     // navigate("/dashboard");
        // } else if (res.status === 401) {
        //     setError("Invalid email or password.");
        // } else if (res.status === 404) {
        //     navigate("/create-account", { state: { email } });
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
            <Typography variant="h5">Login</Typography>
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
            <Button type="submit" variant="contained">Login</Button>
        </Box>
    );
}