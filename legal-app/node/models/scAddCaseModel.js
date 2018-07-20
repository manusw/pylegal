var mongoose=require("mongoose");
var Schema=mongoose.Schema; //creating schema 

var scAddCaseSchema=new Schema({
    "userId":{
        type:String,
        unique:true
    },
    "userCases":[{
        "caseNumber":{
            type:String
        },
        "caseYear":{
            type:String
        }
    }]
}, {collection:"userCases"});

module.exports=mongoose.model('scAddCaseModel',scAddCaseSchema);