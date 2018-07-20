var mongoose=require("mongoose");
var Schema=mongoose.Schema; //creating schema 

var caseSchema=new Schema({
    "id":{
        type:String,
        unique:true,
        required:true
    },
    "courtType":{
        type:String,
        required:true
    },
    "caseType":{
        type:String,
        required:true
    },
    "caseNumber":{
        type:String,
        required:true
    },
    "caseYear":{
        type:String,
        required:true
    },
    "userType":{
        type:String,
        required:true
    }
}, {collection:"caseData"});

module.exports=mongoose.model('caseModel',caseSchema);