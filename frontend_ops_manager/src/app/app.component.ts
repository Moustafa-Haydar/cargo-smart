import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { SidebarComponent } from './components/sidebar/sidebar.component';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, RouterModule, SidebarComponent],
  template: `
    <div class="app-container">
      <app-sidebar></app-sidebar>
      <main class="main-content">
        <router-outlet></router-outlet>
      </main>
    </div>
  `,
  styles: [`
    :host {
      display: block;
      width: 100%;
      min-height: 100vh;
    }

    .app-container {
      display: flex;
      min-height: 100vh;
      position: relative;
    }

    .main-content {
      flex: 1;
      margin-left: 250px;
      padding: 2rem;
      background-color: #f5f5f5;
      min-height: 100vh;
    }
  `]
})
export class AppComponent {
  title = 'CargoSmart';
}