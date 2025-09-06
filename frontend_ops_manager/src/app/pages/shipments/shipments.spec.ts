import { ComponentFixture, TestBed } from '@angular/core/testing';

import { Shipments } from './shipments';

describe('Shipments', () => {
  let component: Shipments;
  let fixture: ComponentFixture<Shipments>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [Shipments]
    })
    .compileComponents();

    fixture = TestBed.createComponent(Shipments);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
