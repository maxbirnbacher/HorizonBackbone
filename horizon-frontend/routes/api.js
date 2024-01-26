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
        console.log(response.data.type);
        console.log(response.data);
        if (response.data.length > 0) {
            // calculate the last seen time from the timestamp in the format of "%Y-%m-%d %H:%M:%S"
            response.data.forEach(agent => {
                agent.lastSeen = new Date(agent.lastSeen * 1000).toLocaleString();
            });
            
            // get the id of the agent from the ObjectID
            response.data.forEach(agent => {
                agent.id = agent._id;
            });

            res.json(response.data);

        } else {
            console.log('No data returned from API');
        }
    
    })
    .catch(function (error) {
        console.log(error);
    });
});


module.exports = router;