var express = require('express');
var router = express.Router();

/* GET home page. */
router.get('/', function(req, res, next) {
    //allow cross origin requests
    res.header("Access-Control-Allow-Origin", "*");
    res.header("Access-Control-Allow-Headers",
        "Origin, X-Requested-With, Content-Type, Accept");

    const file_list = [{
        "name": "file1.txt",
        "size": "1.2kb",
        "date": "2020-01-01"
    }, {
        "name": "file2.txt",
        "size": "2.3kb",
        "date": "2020-01-02"
    }, {
        "name": "file3.txt",
        "size": "3.4kb",
        "date": "2020-01-03"
    }]; // Replace with your actual file list data

    res.render('list-files', { file_list: file_list });
});
/* GET raw file content */
router.get('/raw/:fileID', function(req, res, next) {
        var rawFileContent = "This is the raw file content";
        res.render(rawFileContent);
});

module.exports = router;
