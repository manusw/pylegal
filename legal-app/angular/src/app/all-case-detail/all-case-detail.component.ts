import { Component, OnInit } from '@angular/core';
import {CasesService} from '../cases.service';
import { DashboardService } from '../dashboard.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-all-case-detail',
  templateUrl: './all-case-detail.component.html',
  styleUrls: ['./all-case-detail.component.css']
})
export class AllCaseDetailComponent implements OnInit {

  constructor(private router: Router, private _CasesService:CasesService, private _dashboardService: DashboardService) { }
  email: String;
  userInfo: any;
  name: String;
  caseList:Object;
  diaryNumber:String;

  ngOnInit() {
    this.getAllCases();
    this.diaryNumber="";
    var getUserAuth = localStorage.getItem('userAuth');
    if (getUserAuth === "" || getUserAuth === null || getUserAuth === undefined) {
      this.router.navigateByUrl('/login');
    }
    else {
      this.email = getUserAuth;
      this.fetchUserDetails();
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

  getAllCases(){
    console.log('Fetching top 1000 cases!');
      this._CasesService.getAllCases().subscribe(
        data=>{
          console.log(data);
          this.caseList=data
        },
        error=>{console.log('error: '+error)}
      );
  }

}
