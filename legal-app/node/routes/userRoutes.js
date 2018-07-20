var express=require('express');
var md5=require('md5');
var userModel=require('../models/userModel');
// //initializing Router
// app.use(function (req, res, next) {
//     console.log('Middle layer');
//     // Website you wish to allow to connect
//     res.setHeader('Access-Control-Allow-Origin', 'http://localhost:8888');

//     // Request methods you wish to allow
//     res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS, PUT, PATCH, DELETE');

//     // Request headers you wish to allow
//     res.setHeader('Access-Control-Allow-Headers', 'X-Requested-With,content-type');

//     // Set to true if you need the website to include cookies in the requests sent
//     // to the API (e.g. in case you use sessions)
//     res.setHeader('Access-Control-Allow-Credentials', true);

//     // Pass to next layer of middleware
//     next();
// });


var userRouter=express.Router(); 
userRouter
    .route('/createUser')
    .post(function(request, response){
        var user = new userModel(request.body);
        user.password=md5(request.body.password);
        user.save();
        response.status(200).send(user);
    });

userRouter
    .route('/userList')
    .get(function(request, response){
        console.log('GET Api to get list of user.....');
        userModel.find(function(error, users){
            if(error){
                response.status(500).send(error);
                return;
            }
            else{
                console.log('Fetching records.......');
                console.log(users);
                response.json(users);
            }
        })
    });

userRouter
    .route('/user/:email')
    .get(function(request, response){
        console.log('GET Api to get user is available or not.....');
        var emailID=request.params.email;
        userModel.findOne({email:emailID},function(error, users){
            if(error){
                response.status(500).send(error);
                return;
            }
            else{
                if(users!==null && users!==undefined && users!==""){
                    if(emailID===users.email){
                        response.json(users);
                    }
                    else{
                        response.json({exist:false});
                    }
                }
                else{
                    response.json({exist:false});
                }
            }
        })
    });

userRouter
    .route('/login/:email/:password')
    .get(function(request, response){
        console.log('GET Api to login user.....');
        var emailID=request.params.email;
        var password=request.params.password;
        password=md5(password);
        userModel.findOne({email:emailID, password:password},function(error, users){
            if(error){
                response.status(500).send(error);
                return;
            }
            else{
                if(users!==null && users!==undefined && users!==""){
                    if(emailID===users.email && password===users.password){
                        response.json({loginStatus:"Successful!"});
                    }
                    else{
                        response.json({loginStatus:"Invalid Credentials!"});
                    }
                }
                else{
                    response.json({loginStatus:"Invalid Credentials!"});
                }
            }
        })
    });
module.exports=userRouter;