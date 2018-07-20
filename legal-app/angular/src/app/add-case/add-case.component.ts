import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { DashboardService } from '../dashboard.service';
import { AddcaseService } from '../addcase.service';

@Component({
  selector: 'app-add-case',
  templateUrl: './add-case.component.html',
  styleUrls: ['./add-case.component.css']
})
export class AddCaseComponent implements OnInit {
  email: String;
  userInfo: any;
  name: String;
  diaryNumber:String;
  caseYear:String;
  addCaseResponse:any;
  success:boolean;
  info:boolean;
  warning:boolean;
  danger:boolean;
  successMsg:String;
  infoMsg:String;
  warningMsg:String;
  dangerMsg:String;

  constructor(private router: Router, private _dashboardService: DashboardService, private _addCaseService:AddcaseService) {

  }

  ngOnInit() {
    this.diaryNumber="";
    this.caseYear="";
    this.success=false;
    this.info=false;
    this.warning=false;
    this.danger=false;
    var getUserAuth = localStorage.getItem('userAuth');
    if (getUserAuth === "" || getUserAuth === null || getUserAuth === undefined) {
      this.router.navigateByUrl('/login');
    }
    else {
      this.email = getUserAuth;
      this.fetchUserDetails();
    }
  }

  logout() {
    var getUserAuth = localStorage.getItem('userAuth');
    if (getUserAuth !== "") {
      localStorage.setItem('userAuth', '');
      this.router.navigateByUrl('/login');
    }
    else {
      this.router.navigateByUrl('/login');
    }
  }

  fetchUserDetails() {
    this._dashboardService.fetchUserDetails(this.email).subscribe(
      data => {
        this.userInfo = data
        console.log(this.userInfo);
        this.name = this.userInfo.firstName + ' ' + this.userInfo.lastName;
      },
      error => { console.log('error: ' + error) }
    );
  }

  addCaseByDiaryNumber(){
    this._addCaseService.addCase(this.diaryNumber, this.caseYear).subscribe(
      data => {
        console.log(data);
        this.addCaseResponse=data;
        if(this.addCaseResponse.msg==="updated" || this.addCaseResponse.msg==="created"){
          this.success=true;
          this.successMsg="Case has been added.";
          this.diaryNumber="";
          this.caseYear="";
        }
        else{
          this.warning=true;
          this.warningMsg="Something went wrong, please try again.";
        }
      },
      error => { console.log(error) }
    );
  }


}
