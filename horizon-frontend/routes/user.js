var express = require('express');
var router = express.Router();

/* GET login */
router.get('/login', function(req, res, next) {
    res.render('login');
});

/* GET logout */
router.get('/logout', function(req, res, next) {
    res.render('logout');
});

/* GET signup */
router.get('/signup', function(req, res, next) {
    res.render('signup');
});

module.exports = router;
