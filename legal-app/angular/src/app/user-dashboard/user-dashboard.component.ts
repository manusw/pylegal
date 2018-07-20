import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { DashboardService } from '../dashboard.service';

@Component({
  selector: 'app-user-dashboard',
  templateUrl: './user-dashboard.component.html',
  styleUrls: ['./user-dashboard.component.css']
})
export class UserDashboardComponent implements OnInit {
  email:String;
  userInfo:any;
  name:String;
  show:boolean;

  constructor(private router:Router, private _dashboardService:DashboardService) { }

  ngOnInit() {
    this.show=false;
    var getUserAuth=localStorage.getItem('userAuth');
    if(getUserAuth==="" || getUserAuth===null || getUserAuth===undefined){
      this.router.navigateByUrl('/login');
    }
    else{
      this.email=getUserAuth;
      this.fetchUserDetails();
    }
  }

  logout(){
    var getUserAuth=localStorage.getItem('userAuth');
    if(getUserAuth!==""){
      localStorage.setItem('userAuth','');
      this.router.navigateByUrl('/login');
    }
    else{
      this.router.navigateByUrl('/login');
    }
  }

  fetchUserDetails(){
    this._dashboardService.fetchUserDetails(this.email).subscribe(
      data=>{
        this.userInfo=data
        console.log(this.userInfo);
        this.name=this.userInfo.firstName+' '+this.userInfo.lastName;
      },
      error=>{console.log('error: '+error)}
    );
}

}
