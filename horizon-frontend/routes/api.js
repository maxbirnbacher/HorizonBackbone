var express = require('express');
var router = express.Router();
var axios = require('axios');

/* make a post request to the user-api for login */
router.post('/login', function(req, res, next) {
    // hash the password
    const reqPassword = req.body.password;

    // Hash the password with sha256
    hashedPass = crypto
            .createHash('sha256')
            .update(reqPassword)
            .digest('hex');

    // make a post request to the user-api for login
    axios.post('http://localhost:8002/users/login', {
        username: req.body.username,
        password: hashedPass
    })
    .then(function (response) {
        if (response.status === 200) {
            //login successful, save the token
            localStorage.setItem('token', response.data.access_token);
            res.redirect('/');
        } else {
            //login failed
            console.log('login failed');
            res.redirect('/login');
        }
    })
    .catch(function (error) {
        console.log(error);
    });
});