var mongoose=require("mongoose");
var Schema=mongoose.Schema; //creating schema 

var scCaseDetailSchema=new Schema({
    "_id":{
        type:String,
        unique:true
    },
    "ta_master_court":{
        type:String,
        unique:true
    },
    "ta_diary_num":{
        type:String,
        unique:true
    },
    "ta_diary_year":{
        type:String,
        unique:true
    },
    "diary_case_status":{
        type:String,
        unique:true
    },
    "ta_diary_num_details":{
        type:String,
        unique:true
    },
    "ta_diary_heading":{
        type:String,
        unique:true
    },
    "Diary No":{
        type:String,
        unique:true
    },
    "Case No":{
        type:String,
        unique:true
    },
    "Present/Last Listed On":{
        type:String,
        unique:true
    },
    "Status/Stage":{
        type:String,
        unique:true
    },
    "DispType":{
        type:String,
        unique:true
    },
    "Category":{
        type:String,
        unique:true
    },
    "Act":{
        type:String,
        unique:true
    },
    "Petitioner(s)":{
        type:String,
        unique:true
    },
    "Respondent(s)":{
        type:String,
        unique:true
    },
    "Pet Advocate(s)":{
        type:String,
        unique:true
    },
    "Resp Advocate(s)":{
        type:String,
        unique:true
    },
    "U/Section":{
        type:String,
        unique:true
    },
    "ta_hdn_diary_num":{
        type:String,
        unique:true
    }
}, {collection:"casedetail"});

module.exports=mongoose.model('scCaseDetailModel',scCaseDetailSchema);