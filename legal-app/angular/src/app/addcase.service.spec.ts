import { TestBed, inject } from '@angular/core/testing';

import { AddcaseService } from './addcase.service';

describe('AddcaseService', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [AddcaseService]
    });
  });

  it('should be created', inject([AddcaseService], (service: AddcaseService) => {
    expect(service).toBeTruthy();
  }));
});
