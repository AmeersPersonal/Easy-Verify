const { callProcedure } = require("../db/procedureClient");

async function getUserByIdentifier(identifier) {
    const rows = await callProcedure("get_user", [identifier]);
    return rows[0] || null;
}

async function insertUser({ username, email, passwordHash, isPersistent }) {
    await callProcedure("insert_user", [username, email, passwordHash, isPersistent ? 1 : 0]);
}

async function updateLastLogin(userId) {
    await callProcedure("update_last_login", [userId]);
}

module.exports = {
    getUserByIdentifier,
    insertUser,
    updateLastLogin,
};
