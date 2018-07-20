import { Component, OnInit, Output } from '@angular/core';
import { LoginService } from '../login.service';
import { EventEmitter } from 'events';
import { Router } from '@angular/router';

@Component({
  selector: 'app-user-login',
  templateUrl: './user-login.component.html',
  styleUrls: ['./user-login.component.css']
})
export class UserLoginComponent implements OnInit {

  email:String;
  password:String;
  status:String;
  responseObj:any;

  @Output() userAuthChange=new EventEmitter();

  constructor(private _loginService:LoginService, private router:Router) { 
    
  }

  ngOnInit() {
    
  }

  authChange(){
    console.log('child');
    this.userAuthChange.emit('true');
  }

  login(){
    console.log('Login Called!');
      this._loginService.loginUser(this.email,this.password).subscribe(
        data=>{
          console.log(data);
          this.responseObj=data
          if(this.responseObj.loginStatus==="Successful!"){
            this.router.navigateByUrl('/dashboard');
            localStorage.setItem('userAuth',''+this.email);
          }
        },
        error=>{console.log('error: '+error)}
      );
  }

}
