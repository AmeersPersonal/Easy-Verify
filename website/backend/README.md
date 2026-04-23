# Backend (Controllers + DB Layer)

This backend is structured as:

- routes: map HTTP paths to controller handlers
- controllers: handle req/res, validation, and status codes
- services: business and auth logic
- repositories: DB-facing methods where SQL queries live
- config/database.js: SQLite connection and query helpers

## Folder Layout

- server.js
- config/dotenv.js
- config/database.js
- routes/authRoutes.js
- controllers/authController.js
- services/authService.js
- repositories/userRepository.js

## Install

Run from the backend directory:

```bash
npm install
```

## Environment Variables

Add these values in .env:

```env
PORT=3000
JWT_SECRET=replace_me
SQLITE_DB_PATH=../../client/src/util/db/easyverify.db
```

If SQLITE_DB_PATH is not set, backend defaults to client/src/util/db/easyverify.db.

## Run

```bash
npm run start
```

## Repository Query Pattern

Repository methods run SQL directly through config/database.js.

Example:

```js
await run("INSERT INTO users (username, email, pw, is_persistent) VALUES (?, ?, ?, ?)", [username, email, passwordHash, 0]);
const user = await get("SELECT * FROM users WHERE email = ? OR username = ? LIMIT 1", [identifier, identifier]);
```

## Endpoint Template

- POST /api/auth/register
- POST /api/auth/login
- GET /api/health
