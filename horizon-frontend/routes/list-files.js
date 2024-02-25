var express = require('express');
var router = express.Router();

/* GET home page. */
router.get('/', function(req, res, next) {
    // request the files
    res.render('list-files');
});
/* GET raw file content */
router.get('/raw/:fileID', function(req, res, next) {
        var rawFileContent = "This is the raw file content";
        res.render(rawFileContent);
});

module.exports = router;
