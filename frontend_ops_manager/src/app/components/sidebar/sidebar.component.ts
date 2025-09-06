import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';

@Component({
  selector: 'app-sidebar',
  standalone: true,
  imports: [CommonModule, RouterModule],
  template: `
    <aside class="sidebar">
      <div class="logo">
        <h2>CargoSmart</h2>
      </div>
      <nav class="nav-menu">
        <a routerLink="/shipments" routerLinkActive="active" class="nav-link">
          <i class="fas fa-box"></i>
          <span>Shipments</span>
        </a>
        <a routerLink="/vehicles" routerLinkActive="active" class="nav-link">
          <i class="fas fa-truck"></i>
          <span>Vehicles</span>
        </a>
        <a routerLink="/routes" routerLinkActive="active" class="nav-link">
          <i class="fas fa-route"></i>
          <span>Routes</span>
        </a>
      </nav>
    </aside>
  `,
  styles: [`
    .sidebar {
      width: 250px;
      height: 100vh;
      background-color: #1a237e;
      color: white;
      padding: 1rem;
      position: fixed;
      left: 0;
      top: 0;
      box-shadow: 2px 0 5px rgba(0, 0, 0, 0.1);
      z-index: 1000;
    }

    .logo {
      padding: 1rem 0;
      border-bottom: 1px solid rgba(255, 255, 255, 0.1);
      margin-bottom: 1rem;
    }

    .logo h2 {
      margin: 0;
      font-size: 1.5rem;
      text-align: center;
    }

    .nav-menu {
      display: flex;
      flex-direction: column;
      gap: 0.5rem;
    }

    .nav-link {
      display: flex;
      align-items: center;
      gap: 1rem;
      padding: 0.75rem 1rem;
      color: white;
      text-decoration: none;
      border-radius: 0.5rem;
      transition: background-color 0.2s;
    }

    .nav-link:hover {
      background-color: rgba(255, 255, 255, 0.1);
    }

    .nav-link.active {
      background-color: rgba(255, 255, 255, 0.2);
    }

    .nav-link i {
      width: 20px;
      text-align: center;
    }
  `]
})
export class SidebarComponent { }