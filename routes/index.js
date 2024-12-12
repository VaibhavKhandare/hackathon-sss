var express = require('express');
var router = express.Router();

/* GET home page. */
router.get('/', function(req, res, next) {
    res.set('Access-Control-Allow-Origin', '*');
    res.set('Access-Control-Request-Method', '*');
    res.set('Access-Control-Allow-Methods', 'OPTIONS, POST, GET');
    res.set('Access-Control-Allow-Headers', '*');
  res.render('index', { title: 'Express' });
});

module.exports = router;
