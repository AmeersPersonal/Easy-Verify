const express = require('express')
const jwt = require('jsonwebtoken')
const bcrypt = require('bcrypt')

const app = express();
app.use(express.json());

const JWT_SECRET = process.env.JWT_SECRET;

// define routes
app.post("/api/login", async (req, res) => {
    const { email, password } = req.body;

    // Implement 404 status as of right now to simulate always creating a new user
    return res.status(404)


    // const passwordHash = await findPasswordHashByEmail(email); // TODO: implement DB query
    // if (!passwordHash) {
    //     return res.status(404).json({ message: "No account associated with that email" });
    // }

    // const passwordMatch = await bcrypt.compare(password, passwordHash);
    // if (!passwordMatch) {
    //     return res.status(401).json({ message: "Invalid email or password" });
    // }

    // const token = jwt.sign({ email }, JWT_SECRET, { expiresIn: '7d' });
    // return res.status(200).json({ token, email });
})

app.listen(3000)

// define listeners

// userclass
// sign in (UID)
// 