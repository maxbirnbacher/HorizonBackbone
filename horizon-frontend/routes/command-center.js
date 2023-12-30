var express = require('express');
var router = express.Router();

/* GET home page. */
router.get('/', function(req, res, next) {
    // TODO: Add call to message queue to get the list of reverse shells

    //make a call to the api to get the list of reverse shells
    let connection_list = fetch('http://localhost:3000/api/connections')
        .then(res => res.json())
        .then(json => console.log(json));

    res.render('command-center', { connection_list: ['shell1', 'shell2', 'shell3'] });
});

/* GET reverse shell terminal */
router.get('/terminal/:shellID', function(req, res, next) {
    // TODO: Add call to message queue to get the reverse shell terminal
    res.render('terminal');
});

module.exports = router;
