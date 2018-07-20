import { Pipe, PipeTransform } from '@angular/core';

@Pipe({
  name: 'casefilter'
})
export class CasefilterPipe implements PipeTransform {

  transform(caseList: any, diaryNumber?: any): any {
    return diaryNumber ? caseList.filter(sal => sal["ta_hdn_diary_num"] === diaryNumber) : caseList;
  }

}
