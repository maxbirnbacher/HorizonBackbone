var express = require('express');
var router = express.Router();
var axios = require('axios');
const crypto = require('crypto');

/* GET login */
router.get('/login', function(req, res, next) {
    // hash the password
    const reqPassword = req.body.password;

    // Hash the password with sha256
    const hashedPass = crypto.createHash('sha256').update(reqPassword).digest('hex');

    async function login() {
        const response = await axios.get('http://user-api:8002/users/login', {
        username: req.body.username,
        password: hashedPass
    });

    if (response.status === 200) {
        //login successful, save the token
        localStorage.setItem('token', response.data.access_token);
        res.redirect('/');
    } else {
        //login failed
        console.log('login failed');
        res.redirect('/login');
    }
    }
});

/* GET logout */
router.get('/logout', function(req, res, next) {
    res.render('logout');
});

/* GET signup */
router.get('/signup', function(req, res, next) {
    const reqPassword = req.body.password;

    // Hash the password with sha256
    const hashedPass = crypto.createHash('sha256').update(reqPassword).digest('hex');

    async function signup() {
        const response = await axios.post('http://user-api:8002/users/signup', {
        username: req.body.username,
        password: hashedPass
    });

    if (response.status === 200) {
        //signup successful
        res.redirect('/login');
    } else {
        //signup failed
        console.log('signup failed');
        res.redirect('/signup');
    }
    }
});

module.exports = router;
