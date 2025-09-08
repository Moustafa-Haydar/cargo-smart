import { Component, signal } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { CommonModule } from '@angular/common';
import { SidebarComponent } from './shared/components/sidebar/sidebar.component';
import { SelectModule } from 'primeng/select';

@Component({
    selector: 'app-root',
    standalone: true,
    imports: [CommonModule, RouterOutlet, SidebarComponent, SelectModule],
    templateUrl: './app.html',
    styleUrl: './app.css'
})
export class App {
    protected readonly title = signal('frontend_ops_manager');
}