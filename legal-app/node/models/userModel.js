var mongoose=require("mongoose");
var Schema=mongoose.Schema; //creating schema 

var userSchema=new Schema({
    "id":{
        type:String,
        unique:true,
        required:true
    },
    "firstName":{
        type:String,
        required:true
    },
    "lastName":{
        type:String,
        required:true
    },
    "phoneNumber":{
        type:String,
        required:true
    },
    "email":{
        type:String,
        required:true
    },
    "password":{
        type:String,
        required:true
    },
    "isActive":{
        type:Boolean,
        required:true,
        default:false
    }
}, {collection:"userData"});

module.exports=mongoose.model('userModel',userSchema);