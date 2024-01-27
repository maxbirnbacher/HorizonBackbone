var express = require('express');
var router = express.Router();
var axios = require('axios');
var crypto = require('crypto');

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

router.get('/agents/all', function(req, res, next) {
    axios.get('http://localhost:8001/c2/list-connections', {
        // headers: {
        //     Authorization: 'Bearer ' + localStorage.getItem('token')
        // }
    })
    .then(function (response) {
        // Check if response.data is an array
        console.log(response.data.connection_list);
        if (response.data.connection_list.length > 0) {
            res.json(response.data.connection_list);
        } else {
            console.log('No data returned from API');
        }
    
    })
    .catch(function (error) {
        console.log(error);
    });
});

router.get('/agents/:agentID', function(req, res, next) {
    // make a get request to the agent-api for agent details
    axios.get('http://localhost:8001/c2/get-connection//' + req.params.agentID, {
    })
    .then(function (response) {
        // Check if response.data is an array
        console.log(response.data);
        if (response.data.length > 0) {
            res.render('agent', {agent: response.data});
        } else {
            console.log('No data returned from API');
        }
    
    })
    .catch(function (error) {
        console.log(error);
    });
});


module.exports = router;