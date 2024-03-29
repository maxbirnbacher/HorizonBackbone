var express = require('express');
var router = express.Router();
const fs = require('fs');
const path = require('path');
var axios = require('axios');

router.get('/campaigns', function(req, res, next) {
    res.render('campaigns');
});

router.get('/campaigns/:campaignID', function(req, res, next) {
    res.render('campaign');
});

router.get('/agents', function(req, res, next) {
    res.render('agents');
});

router.get('/agent/:agentID', function(req, res, next) {
    console.log("trying to render agent page")
    console.log('agentID: ' + req.params.agentID);
    // make a get request to the agent-api for agent details
    console.log('http://c2-api:8001/c2/get-connection/' + req.params.agentID);
    axios.get('http://c2-api:8001/c2/get-connection/' + req.params.agentID, {
    })
    .then(function (response) {
        console.log(response.data.connection);
        if (response.data.connection) {
            res.render('agent', {agent: response.data.connection});
        } else {
            console.log('No data returned from API');
        }
    })
});

//route to view agent page without id
router.get('/agent', function(req, res, next) {
    console.log('Entering /agent route');
    try {
        // find the agent.ejs file
        const viewPath = path.join(__dirname, '../views/agent.ejs');

        fs.access(viewPath, fs.constants.F_OK, (err) => {
            console.log(`Agent view ${err ? 'does not exist' : 'exists'}`);
        });

        res.render(viewPath, {agent: 'test'});
    } catch (err) {
        console.log(err);
    }
});


router.get('/broadcast', function(req, res, next) {
    res.render('broadcast');
});
  
module.exports = router;
  