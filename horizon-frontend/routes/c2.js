var express = require('express');
var router = express.Router();

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
    // make a get request to the agent-api for agent details
    axios.get('/api/agents/' + req.params.agentID, {
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

    res.render('agent');
});

// //route to view agent page without id
// router.get('/agent', function(req, res, next) {
//     res.render('agent');
// });


router.get('/broadcast', function(req, res, next) {
    res.render('broadcast');
});
  
module.exports = router;
  