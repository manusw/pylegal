var express = require('express');
// var requestP = require('request');
// var JSSoup = require('jssoup').default
var scCaseModel = require('../models/scCaseDetailModel');
var scAddCaseModel = require('../models/scAddCaseModel');

var scCaseRouter = express.Router();

scCaseRouter
    .route('/scCaseDetail')
    .get(function (request, response) {
        console.log('GET Api to get list of user.....');
        scCaseModel.find(function (error, cases) {
            if (error) {
                response.status(500).send(error);
                return;
            }
            else {
                console.log('Fetching records.......');
                console.log(cases);
                response.json(cases);
            }
        }).sort({ _id: 1 }).limit(1000);
    });


scCaseRouter
    .route('/getUserCaseList/:email')
    .get(function (request, response) {
        console.log('GET Api to get list of user cases.....');
      //  console.log(request);
        var emailID = request.params.email;
        scAddCaseModel.findOne({ "userId": emailID }, function (error, userCaseList) {
            if (error) {
                response.status(500).send(error);
                return;
            }
            else {

               // console.log(userCaseList);
            //    console.log(userCaseList[0].userCases);

            //    console.log(userCaseList[0].userCases);
                var usercases=userCaseList.userCases
              //  console.log(usercas);
               var userCaseDetail=[];

                var lookup=0;
               usercases.forEach(function(usercas) {
                console.log(usercas.caseNumber+usercas.caseYear)
                d_num=usercas.caseNumber+usercas.caseYear;
                scCaseModel.findOne({ 'ta_hdn_diary_num': d_num },  function (error, cdetail) {
                    if (error) {
                        response.status(500).send(error);
                        return;
                    }
                    
                    userCaseDetail.push(cdetail)
                    if(++lookup == usercases.length)
                    {
                     //  console.log('i is '+ lookup + '   '+userCaseDetail.length +'json '+JSON.stringify(userCaseDetail))
                       response.json(userCaseDetail);
                    }
                    
                //    console.log(userCaseDetail)
                  //  console.log(userCaseDetail.length);
                  //  
                  });

                });
               // console.log(userCaseDetail)


             /*   var userCases = new Array();
                var userCaseResponse = new Array();
                if (userCaseList !== null && userCaseList !== undefined) {
                    userCases = userCaseList[0].userCases;
                    console.log(userCases);
                    //for (var i = 0; i < userCases.length; i++) {
                        //console.log('-----' + userCases[i].caseNumber + userCases[i].caseYear);
                        scCaseModel.find(
                            { 'ta_hdn_diary_num':{$all:[userCases[0].caseNumber + userCases[0].caseYear,userCases[1].caseNumber + userCases[1].caseYear,'268']}  },
                            function (error, uCase) {
                                if (error) {
                                    response.status(500).send(error);
                                    return;
                                }
                                else {
                                    userCaseResponse.push(uCase[0]);
                                    console.log(userCaseResponse.length);
                                }
                                response.json(uCase);
                            }
                        );
                    //}
                   
                }*/ // manu commenting previous code 
            }
        });


        // scCaseModel.find({'ta_hdn_diary_num':hdnDiaryNumber},function (error, cases) {
        //     if (error) {
        //         response.status(500).send(error);
        //         return;
        //     }
        //     else {
        //         console.log('Fetching records.......');
        //         console.log(cases);
        //         response.json(cases);
        //     }
        // }).sort({ _id: 1 }).limit(1000);
    });

scCaseRouter
    .route('/scAddCase')
    .post(function (request, response) {

        var isEmailExist = false;
        var emailID = request.body.userId;

        //Checking whether the email is exist or not
        scAddCaseModel.find({ "userId": emailID }, function (error, userExist) {
            if (error) {
                response.status(500).send(error);
                return;
            }
            else {
                console.log(userExist.length);
                if (userExist !== null && userExist !== undefined && userExist !== "" && userExist.length > 0) {
                    console.log('if');
                    if (emailID === userExist[0].userId) {
                        console.log('if');
                        isEmailExist = true;
                        //Update existing record
                        var userCase = new scAddCaseModel(request.body);
                        scAddCaseModel.findOneAndUpdate(
                            { "userId": emailID },
                            {
                                $addToSet: {
                                    "userCases": {
                                        'caseNumber': userCase.userCases[0].caseNumber,
                                        'caseYear': userCase.userCases[0].caseYear
                                    }
                                }
                            },
                            { upsert: true },
                            function (error, userCase) {
                                if (error) {
                                    response.status(500).send(error);
                                    return;
                                }
                                else {
                                    console.log('Fetching records.......');
                                    //console.log(userCase);
                                    response.status(200).send({ "id": "exist", "msg": "updated" });
                                }
                            });
                    }
                    else {
                        console.log('else');
                        isEmailExist = false;
                        //create new record
                        var userCase = new scAddCaseModel(request.body);
                        userCase.save();
                        response.status(200).send({ "id": "new", "msg": "created" });
                    }
                }
                else {
                    console.log('else');
                    isEmailExist = false;
                    var userCase = new scAddCaseModel(request.body);
                    userCase.save();
                    response.status(200).send({ "id": "new", "msg": "created" });
                }
            }
        });

        // function(result){
        //     if (isEmailExist === true) {
        //         console.log('true------------>>>>>>'+isEmailExist);

        //     }
        //     else {
        //         console.log('false------------>>>>>>'+isEmailExist);

        //     }
        // }


        // response.status(200).send(userCase);
    });

scCaseRouter
    .route('/userCases')
    .get(function (request, response) {
        scAddCaseModel.find({ "userId": "ma@ma.com" }, function (error, userCase) {
            if (error) {
                response.status(500).send(error);
                return;
            }
            else {
                console.log('Fetching records.......');
                console.log(userCase);
                response.json(userCase);
            }
        }).sort({ _id: 1 }).limit(3);
    });

module.exports = scCaseRouter;