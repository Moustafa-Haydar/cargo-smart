import { ComponentFixture, TestBed } from '@angular/core/testing';

import { Routes } from './routes';

describe('Routes', () => {
  let component: Routes;
  let fixture: ComponentFixture<Routes>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [Routes]
    })
    .compileComponents();

    fixture = TestBed.createComponent(Routes);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
