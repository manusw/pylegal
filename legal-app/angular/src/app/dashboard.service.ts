import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class DashboardService {

  constructor(private http:HttpClient) { }

  fetchUserDetails(email){
    let body=JSON.stringify({email:email});
    return this.http.get<Object>('http://localhost:8080/api/user/'+email);
  }
}
