const bcrypt = require("bcrypt");
const jwt = require("jsonwebtoken");
const userRepository = require("../repositories/userRepository");

async function loginUser({ email, password, jwtSecret }) {
    const companyUser = await userRepository.getCompanyByEmail(email);
    if (!companyUser) {
        return { ok: false, status: 404, message: "No account associated with that email" };
    }

    const passwordMatch = await bcrypt.compare(password, companyUser.pw);
    if (!passwordMatch) {
        return { ok: false, status: 401, message: "Invalid email or password" };
    }

    const token = jwt.sign({ companyId: companyUser.id, email: companyUser.email }, jwtSecret, { expiresIn: "7d" });
    return {
        ok: true,
        status: 200,
        data: {
            token,
            user: {
                id: companyUser.id,
                name: companyUser.name,
                email: companyUser.email,
                verified: Boolean(companyUser.verified),
            },
        },
    };
}

async function registerUser({ name, email, password }) {
    const exists = await userRepository.companyEmailExists(email);
    if (exists) {
        return { ok: false, status: 409, message: "Email is already in use" };
    }

    const passwordHash = await bcrypt.hash(password, 10);
    const userId = await userRepository.addCompanyUser({ email, name, passwordHash});

    return {
        ok: true,
        status: 201,
        data: {
            message: "Company user created",
            user: {
                id: userId,
                name,
                email,
                verified: false,
            },
        },
    };
}

async function setUserVerification({ userId, verified }) {
    const exists = await userRepository.companyIdExists(userId);
    if (!exists) {
        return { ok: false, status: 404, message: "No account associated with that user ID" };
    }

    await userRepository.updateCompanyVerificationById(userId, verified);

    return {
        ok: true,
        status: 200,
        data: {
            userId,
            verified: Boolean(verified),
            verifiedValue: verified ? 1 : 0,
        },
    };
}

async function getUserVerificationStatus({ email }) {
    const exists = await userRepository.companyEmailExists(email);
    if (!exists) {
        return { ok: false, status: 404, message: "No account associated with that email" };
    }

    const verified = await userRepository.isCompanyVerified(email);
    return {
        ok: true,
        status: 200,
        data: {
            email,
            verified,
            verifiedValue: verified ? 1 : 0,
        },
    };
}

async function validateEmailInCompany({ email }) {
    const exists = await userRepository.companyEmailExists(email);
    return {
        ok: true,
        status: 200,
        data: {
            email,
            exists,
        },
    };
}

module.exports = {
    getUserVerificationStatus,
    loginUser,
    registerUser,
    setUserVerification,
    validateEmailInCompany,
};
