require("./dotenv");
const fs = require("fs");
const path = require("path");
const sqlite3 = require("sqlite3").verbose();

const defaultDbPath = path.resolve(
    __dirname,
    "..",
    "..",
    "..",
    "client",
    "src",
    "util",
    "db",
    "easyverify.db"
);
const dbPath = process.env.SQLITE_DB_PATH ? path.resolve(process.env.SQLITE_DB_PATH) : defaultDbPath;

if (!fs.existsSync(path.dirname(dbPath))) {
    fs.mkdirSync(path.dirname(dbPath), { recursive: true });
}

const db = new sqlite3.Database(dbPath);

function run(sql, params = []) {
    return new Promise((resolve, reject) => {
        db.run(sql, params, function onRun(err) {
            if (err) {
                reject(err);
                return;
            }

            resolve({ lastID: this.lastID, changes: this.changes });
        });
    });
}

function get(sql, params = []) {
    return new Promise((resolve, reject) => {
        db.get(sql, params, (err, row) => {
            if (err) {
                reject(err);
                return;
            }

            resolve(row || null);
        });
    });
}

function all(sql, params = []) {
    return new Promise((resolve, reject) => {
        db.all(sql, params, (err, rows) => {
            if (err) {
                reject(err);
                return;
            }

            resolve(rows);
        });
    });
}

async function initializeDatabase() {
    await run("PRAGMA foreign_keys = ON");
}

const dbReady = initializeDatabase();

module.exports = {
    all,
    db,
    dbPath,
    dbReady,
    get,
    run,
};