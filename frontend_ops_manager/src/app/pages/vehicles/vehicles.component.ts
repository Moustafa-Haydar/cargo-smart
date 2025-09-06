import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-vehicles',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="page-container">
      <h1>Vehicles</h1>
      <div class="content">
        <!-- Vehicles content will go here -->
        <p>Vehicles management dashboard</p>
      </div>
    </div>
  `,
  styles: [`
    .page-container {
      padding: 2rem;
    }
    
    .content {
      background: white;
      border-radius: 8px;
      padding: 1.5rem;
      box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
  `]
})
export class VehiclesComponent {}
