# Backend Template (Controllers + DB Layer)

This backend is structured as:

- routes: map HTTP paths to controller handlers
- controllers: handle req/res, validation, and status codes
- services: business and auth logic
- repositories: DB-facing methods where stored procedure names live
- db: generic procedure caller and connection pool

## Folder Layout

- server.js
- config/dotenv.js
- config/database.js
- routes/authRoutes.js
- controllers/authController.js
- services/authService.js
- repositories/userRepository.js
- db/procedureClient.js

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
DB_HOST=127.0.0.1
DB_USER=root
DB_PASSWORD=
DB_NAME=easyverify
```

## Run

```bash
npm run start
```

## Stored Procedure Pattern

Repository methods call procedures through db/procedureClient.js.

Example:

```js
await callProcedure("insert_user", [username, email, passwordHash, 0]);
const rows = await callProcedure("get_user", [email]);
```

## Endpoint Template

- POST /api/auth/register
- POST /api/auth/login
- GET /api/health
