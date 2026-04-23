const { get, run, dbReady } = require("../config/database");

async function getCompanyByEmail(email) {
    await dbReady;
    return get(
        `
            SELECT id, name, email, pw, verified
            FROM companyx
            WHERE email = ?
            LIMIT 1
        `,
        [email]
    );
}

async function companyIdExists(userId) {
    await dbReady;
    const row = await get(
        `
            SELECT 1 AS exists_flag
            FROM companyx
            WHERE id = ?
            LIMIT 1
        `,
        [userId]
    );

    return Boolean(row);
}

async function addCompanyUser({ email, name, passwordHash}) {
    await dbReady;
    const result = await run(
        `
            INSERT INTO companyx (name, email, pw, verified)
            VALUES (?, ?, ?, 0)
        `,
        [name, email, passwordHash]
    );

    return result.lastID;
}

async function updateCompanyVerificationById(userId, verified) {
    await dbReady;
    await run(
        `
            UPDATE companyx
            SET verified = ?
            WHERE id = ?
        `,
        [verified ? 1 : 0, userId]
    );
}

async function isCompanyVerified(email) {
    await dbReady;
    const row = await get(
        `
            SELECT verified
            FROM companyx
            WHERE email = ?
            LIMIT 1
        `,
        [email]
    );

    return row ? Boolean(row.verified) : false;
}

async function companyEmailExists(email) {
    await dbReady;
    const row = await get(
        `
            SELECT 1 AS exists_flag
            FROM companyx
            WHERE email = ?
            LIMIT 1
        `,
        [email]
    );

    return Boolean(row);
}

module.exports = {
    addCompanyUser,
    companyIdExists,
    companyEmailExists,
    getCompanyByEmail,
    isCompanyVerified,
    updateCompanyVerificationById,
};
