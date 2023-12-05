var express = require('express');
var router = express.Router();

/* GET home page. */
router.get('/', function(req, res, next) {
    // TODO: Add call to message queue to get the list of reverse shells
    res.render('command-center');
});

/* GET reverse shell terminal */
router.get('/terminal/:shellID', function(req, res, next) {
    // TODO: Add call to message queue to get the reverse shell terminal
    res.render('terminal');
});

module.exports = router;
