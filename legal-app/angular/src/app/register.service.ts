import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { URLSearchParams } from '@angular/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class RegisterService {

  constructor(private http:HttpClient) { }

  createUser(firstName,lastName,phoneNumber,email,password){
    let body=JSON.stringify({id:this.guid(),firstName:firstName, lastName:lastName,phoneNumber:phoneNumber, email:email,password:password,isActive:'true'});
    const httpOptions = {
      headers: new HttpHeaders({
        'Content-Type':  'application/json'
      })
    };
    console.log(JSON.parse(body));
    return this.http.post<Object>('http://localhost:8080/api/createUser/',body,httpOptions);
  }

  guid() {
    function s4() {
      return Math.floor((1 + Math.random()) * 0x10000)
        .toString(16)
        .substring(1);
    }
    return s4() + s4() + '-' + s4() + '-' + s4() + '-' + s4() + '-' + s4() + s4() + s4();
  }
}
