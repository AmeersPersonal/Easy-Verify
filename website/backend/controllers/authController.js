const authService = require("../services/authService");
require("../config/dotenv");

async function login(req, res) {
    try {
        const { email, password } = req.body;
        if (!email || !password) {
            return res.status(400).json({ message: "email and password are required" });
        }

        const jwtSecret = process.env.JWT_SECRET?.trim();
        if (!jwtSecret) {
            return res.status(500).json({ message: "JWT_SECRET is not configured" });
        }

        const result = await authService.loginUser({
            email,
            password,
            jwtSecret,
        });

        if (!result.ok) {
            return res.status(result.status).json({ message: result.message });
        }

        return res.status(result.status).json(result.data);
    } catch (error) {
        console.log(error.message)
        return res.status(500).json({ message: "Login failed", error: error.message });
    }
}

async function register(req, res) {
    try {
        const { username, email, password } = req.body;
        const name = username || email?.split("@")[0] || "";

        if (!email || !password) {
            return res.status(400).json({ message: "email and password are required" });
        }

        const result = await authService.registerUser({
            name,
            email,
            password,
        });

        if (!result.ok) {
            return res.status(result.status).json({ message: result.message });
        }

        return res.status(result.status).json(result.data);
    } catch (error) {
        console.log(error.message)
        return res.status(500).json({ message: "Registration failed", error: error.message });
    }
}

async function setVerification(req, res) {
    try {
        const { userId, verified } = req.body;
        const normalizedUserId = Number(userId);

        if (!Number.isInteger(normalizedUserId) || normalizedUserId <= 0 || typeof verified === "undefined") {
            return res.status(400).json({ message: "userId and verified are required" });
        }

        const result = await authService.setUserVerification({
            userId: normalizedUserId,
            verified,
        });

        if (!result.ok) {
            return res.status(result.status).json({ message: result.message });
        }

        return res.status(result.status).json(result.data);
    } catch (error) {
        return res.status(500).json({ message: "Verification update failed", error: error.message });
    }
}

async function verificationStatus(req, res) {
    try {
        const { email } = req.query;
        if (!email) {
            return res.status(400).json({ message: "email is required" });
        }

        const result = await authService.getUserVerificationStatus({ email });
        if (!result.ok) {
            return res.status(result.status).json({ message: result.message });
        }

        return res.status(result.status).json(result.data);
    } catch (error) {
        return res.status(500).json({ message: "Verification status failed", error: error.message });
    }
}

async function validateEmail(req, res) {
    try {
        const { email } = req.query;
        if (!email) {
            return res.status(400).json({ message: "email is required" });
        }

        const result = await authService.validateEmailInCompany({ email });
        return res.status(result.status).json(result.data);
    } catch (error) {
        return res.status(500).json({ message: "Email validation failed", error: error.message });
    }
}

module.exports = {
    login,
    register,
    setVerification,
    validateEmail,
    verificationStatus,
};
