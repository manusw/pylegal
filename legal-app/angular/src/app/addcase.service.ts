import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class AddcaseService {

  constructor(private http:HttpClient) { }

  addCase(diaryNumber, caseYear){
    //let body=JSON.stringify({email:email});
    var emailId=localStorage.getItem('userAuth');
    let body=JSON.stringify(
      {
        "userId":emailId,
          "userCases":[
            {
              "caseNumber":diaryNumber,
              "caseYear":caseYear
            }	
        ]
      }
    );
    const httpOptions = {
      headers: new HttpHeaders({
        'Content-Type':  'application/json'
      })
    };
    console.log(body);
    return this.http.post<Object>('http://localhost:8080/api/scAddCase/',body,httpOptions);
  }
}
