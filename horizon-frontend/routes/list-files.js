var express = require('express');
var router = express.Router();

/* GET home page. */
router.get('/', function(req, res, next) {
    //allow cross origin requests
    res.header("Access-Control-Allow-Origin", "*");
    res.header("Access-Control-Allow-Headers",
        "Origin, X-Requested-With, Content-Type, Accept");

    // TODO: Add call to message queue to get the file list
    const file_list = ['file1.txt', 'file2.txt', 'file3.txt']; // Replace with your actual file list data

    res.render('list-files', { file_list: file_list });
});
/* GET raw file content */
router.get('/raw/:fileID', function(req, res, next) {
        // TODO: Add call to message queue to get the file content
        var rawFileContent = "This is the raw file content";
        res.render(rawFileContent);
});

module.exports = router;
