var express = require('express');
var router = express.Router();

/* GET support page. */
router.get('/support', function(req, res, next) {
  res.render('support');
});

/* GET user management page. */
router.get('/user-management', function(req, res, next) {
  res.render('user-management');
});

/* GET extra modules page. */
router.get('/modules', function(req, res, next) {
  res.render('modules');
});


module.exports = router;