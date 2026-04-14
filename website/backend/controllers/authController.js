const authService = require("../services/authService");

async function login(req, res) {
    try {
        const { email, username, password } = req.body;

        const identifier = email || username;
        if (!identifier || !password) {
            return res.status(400).json({ message: "identifier and password are required" });
        }

        if (!process.env.JWT_SECRET) {
            return res.status(500).json({ message: "JWT_SECRET is not configured" });
        }

        const result = await authService.loginUser({
            identifier,
            password,
            jwtSecret: process.env.JWT_SECRET,
        });

        if (!result.ok) {
            return res.status(result.status).json({ message: result.message });
        }

        return res.status(result.status).json(result.data);
    } catch (error) {
        return res.status(500).json({ message: "Login failed", error: error.message });
    }
}

async function register(req, res) {
    try {
        const { username, email, password, isPersistent = false } = req.body;

        if (!username || !email || !password) {
            return res.status(400).json({ message: "username, email, and password are required" });
        }

        const result = await authService.registerUser({
            username,
            email,
            password,
            isPersistent,
        });

        if (!result.ok) {
            return res.status(result.status).json({ message: result.message });
        }

        return res.status(result.status).json(result.data);
    } catch (error) {
        return res.status(500).json({ message: "Registration failed", error: error.message });
    }
}

module.exports = {
    login,
    register,
};
