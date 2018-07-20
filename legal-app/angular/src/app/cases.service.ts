import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class CasesService {

  constructor(private http:HttpClient) { }

  getAllCases(){
    //let body=JSON.stringify({email:email,password:password});
    return this.http.get<Object>('http://localhost:8080/api/scCaseDetail/');
  }
}
