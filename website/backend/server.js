const express = require('express')

const app = express();

// define routes
app.get('/api/verification', (req, res) => {
    res.send("This is an API");
});

app.listen(3000)

// define listeners

// userclass
// sign in (UID)
// 