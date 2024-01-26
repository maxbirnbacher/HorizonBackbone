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
    res.render('agent');
});

router.get('/broadcast', function(req, res, next) {
    res.render('broadcast');
});
  
module.exports = router;
  