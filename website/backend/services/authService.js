const bcrypt = require("bcrypt");
const jwt = require("jsonwebtoken");
const userRepository = require("../repositories/userRepository");

async function loginUser({ identifier, password, jwtSecret }) {
    const user = await userRepository.getUserByIdentifier(identifier);
    if (!user) {
        return { ok: false, status: 404, message: "No account associated with that username/email" };
    }

    const passwordMatch = await bcrypt.compare(password, user.pw);
    if (!passwordMatch) {
        return { ok: false, status: 401, message: "Invalid username/email or password" };
    }

    await userRepository.updateLastLogin(user.id);

    const token = jwt.sign({ userId: user.id, email: user.email }, jwtSecret, { expiresIn: "7d" });
    return {
        ok: true,
        status: 200,
        data: {
            token,
            user: {
                id: user.id,
                username: user.username,
                email: user.email,
            },
        },
    };
}

async function registerUser({ username, email, password, isPersistent }) {
    const existing = await userRepository.getUserByIdentifier(email);
    if (existing) {
        return { ok: false, status: 409, message: "Email or username is already in use" };
    }

    const passwordHash = await bcrypt.hash(password, 10);
    await userRepository.insertUser({ username, email, passwordHash, isPersistent });

    return {
        ok: true,
        status: 201,
        data: { message: "User created" },
    };
}

module.exports = {
    loginUser,
    registerUser,
};
