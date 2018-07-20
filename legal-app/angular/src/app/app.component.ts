import { Component, OnInit } from '@angular/core';
import { LoginService } from './login.service';
import { Observable } from 'rxjs';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {
  isMenu:boolean;
  
  constructor(private _loginService:LoginService){
    //this.appTitle="Legal App";
  }

  ngOnInit(){
    //this.loginUser();
    this.isMenu=true;
  }



  // setMenuVisible(){
  //   console.log('Called');
  //   this.isMenu=(this.isMenu===true)?false:true;
  // }

}
