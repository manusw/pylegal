import { Component, OnInit } from '@angular/core';
import { RegisterService } from '../register.service';

@Component({
  selector: 'app-user-registration',
  templateUrl: './user-registration.component.html',
  styleUrls: ['./user-registration.component.css']
})
export class UserRegistrationComponent implements OnInit {
  firstName: String;
  lastName: String;
  phoneNumber: String;
  email: String;
  password: String;
  confirmPassword: String;
  validationCheck: boolean;
  autoGenerateId:String;

  constructor(private _registerService: RegisterService) { }

  ngOnInit() {
    this.validationCheck = true;
  }


  register() {
    if (this.firstName !== "" && this.firstName !== null && this.firstName !== undefined) {
      this.validationCheck = true;
    }
    else {
      this.validationCheck = false;
    }
    if (this.lastName !== "" && this.lastName !== null && this.lastName !== undefined) {
      this.validationCheck = true;
    }
    else {
      this.validationCheck = false;
    }
    if (this.phoneNumber !== "" && this.phoneNumber !== null && this.phoneNumber !== undefined) {
      this.validationCheck = true;
    }
    else {
      this.validationCheck = false;
    }
    if (this.email !== "" && this.email !== null && this.email !== undefined) {
      this.validationCheck = true;
    }
    else {
      this.validationCheck = false;
    }
    if (this.password !== "" && this.password !== null && this.password !== undefined) {
      this.validationCheck = true;
    }
    else {
      this.validationCheck = false;
    }
    if (this.confirmPassword !== "" && this.confirmPassword !== null && this.confirmPassword !== undefined) {
      this.validationCheck = true;
    }
    else {
      this.validationCheck = false;
    }

    if (this.password===this.confirmPassword){
      this.validationCheck = true;
    }
    else {
      this.validationCheck = false;
    }

    if (this.validationCheck) {
      this._registerService.createUser(this.firstName, this.lastName, this.phoneNumber, this.email, this.password).subscribe(
        data => {
          console.log(data);
          this.autoGenerateId=data["_id"];
        },
        error => { console.log(error) }
      );
    }
  }

}
