var express = require('express');
var requestP = require('request');
var JSSoup = require('jssoup').default
var caseModel = require('../models/caseModel');

var caseRouter = express.Router(); //initializing Router

caseRouter
    .route('/getCaseDetails')
    .post(function (request, response) {
        console.log('POST Api to create an user....');
        console.log(request.body);
        var caseDetail = new caseModel(request.body);

        var caseType = caseDetail.caseType;
        var caseNumber = caseDetail.caseNumber;
        var caseYear = caseDetail.caseYear;

        //SC CODE
        var headers = {
            'Origin': 'https://sci.nic.in',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.9',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Accept': '*/*',
            'Referer': 'https://sci.nic.in/case-status',
            'X-Requested-With': 'XMLHttpRequest',
            'Connection': 'keep-alive',
            'Cookie': 'has_js=1'
        };

        var dataString = 'ct=' + caseType + '&cn=' + caseNumber + '&cy=' + caseYear;

        var options = {
            url: 'https://sci.nic.in/php/case_status/case_status_process.php',
            method: 'POST',
            headers: headers,
            body: dataString,
            strictSSL: false
        };

        function callback(error, res, body) {
            console.log('Callback fun called!!!!');
            if (error) {
                console.log(error);
            }
            if (!error && res.statusCode == 200) {
                //console.log(body);
                var soup = new JSSoup(body);
                // console.log('----------PRINT START--------');
                var tag = soup.find('table');
                // console.log('----------TAG START--------');
                //console.log(tag.prettify());

                response.status(200).send(tag.prettify());
            }

        }

        requestP(options, callback);
        //SC CODE END

        //user.save();

    });



module.exports = caseRouter;