import { ComponentFixture, TestBed } from '@angular/core/testing';

import { VehicleCard } from './vehicle-card';

describe('VehicleCard', () => {
  let component: VehicleCard;
  let fixture: ComponentFixture<VehicleCard>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [VehicleCard]
    })
    .compileComponents();

    fixture = TestBed.createComponent(VehicleCard);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
