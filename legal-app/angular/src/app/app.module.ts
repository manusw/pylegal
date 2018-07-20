import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { RouterModule, Routes } from '@angular/router';
import { HttpClientModule } from '@angular/common/http';

import { AppComponent } from './app.component';
import { UserLoginComponent } from './user-login/user-login.component';
import { UserRegistrationComponent } from './user-registration/user-registration.component';
import { LoginService } from './login.service';
import { UserDashboardComponent } from './user-dashboard/user-dashboard.component';
import { AddCaseComponent } from './add-case/add-case.component';
import { AllCaseDetailComponent } from './all-case-detail/all-case-detail.component';
import { CasefilterPipe } from './casefilter.pipe';

const appRoutes: Routes = [
  {
    path: 'login',
    component: UserLoginComponent,
  },
  {
    path:'register',
    component:UserRegistrationComponent
  },
  {
    path:'dashboard',
    component:UserDashboardComponent
  },
  {
    path:'dashboard/addcase',
    component:AddCaseComponent
  },
  {
    path:'dashboard/allcases',
    component:AllCaseDetailComponent
  }
]

@NgModule({
  declarations: [
    AppComponent,
    UserLoginComponent,
    UserRegistrationComponent,
    UserDashboardComponent,
    AddCaseComponent,
    AllCaseDetailComponent,
    CasefilterPipe
  ],
  imports: [
    BrowserModule,
    FormsModule,
    RouterModule.forRoot(
      appRoutes
    ),
    HttpClientModule
  ],
  providers: [LoginService],
  bootstrap: [AppComponent]
})
export class AppModule { }
