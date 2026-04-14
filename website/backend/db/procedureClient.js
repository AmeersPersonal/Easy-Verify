const pool = require("../config/database");

async function callProcedure(name, params = []) {
    const placeholders = params.map(() => "?").join(", ");
    const sql = `CALL ${name}(${placeholders})`;

    const [raw] = await pool.query(sql, params);

    // mysql2 returns nested arrays for SELECT resultsets from procedures.
    if (Array.isArray(raw) && Array.isArray(raw[0])) {
        return raw[0];
    }

    return raw;
}

module.exports = {
    callProcedure,
    pool,
};
