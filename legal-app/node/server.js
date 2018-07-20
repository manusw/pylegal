var express = require('express');
var bodyParser=require('body-parser');
var mongoose=require('mongoose');
var usesRouter=require('./routes/userRoutes');
var caseRouter=require('./routes/caseRoutes');
var scCaseRouter=require('./routes/scCaseDetailRoutes');

var app=express();

var PORT=8080;
var HOSTNAME="localhost";
var DATABASE="mongo_scdetails";

mongoose.connect('mongodb://'+HOSTNAME+'/'+DATABASE);

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({extended:true}));
app.use(function(req, res, next) { 
    res.header("Access-Control-Allow-Origin", "*"); 
    res.header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept"); 
    next(); 
});
app.use('/api',usesRouter);
app.use('/api',caseRouter);
app.use('/api',scCaseRouter);

app.listen(PORT,function(){
    console.log('Legal API app listening at '+PORT);
})