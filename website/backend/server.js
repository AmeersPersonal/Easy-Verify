const express = require('express')
//const fs = require("fs")
//const https = require("https")

const app = express();
app.use(express.json());

// define routes
app.get('/api/verification', (req, res) => {
    res.send("another test");
});

// https://express-validator.github.io/docs/guides/getting-started //use this 
const validateRequest = (req, res, next) => {
    console.log(req.body);


    next(); //keep moving after validation
}

app.post('/api/post', validateRequest, (req, res) => {

    //console.dir(req.body);
    res.json({Response: "Test"});
});

app.listen(3000)

// define listeners

// userclass
// sign in (UID)
// 