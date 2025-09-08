import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Route } from '../../models/logistics.model';
import { Card } from 'primeng/card';

@Component({
    selector: 'app-route-card',
    standalone: true,
    imports: [CommonModule, Card],
    templateUrl: './route-card.html',
    styleUrls: ['./route-card.css']
})
export class RouteCard {
    @Input({ required: true }) route!: Route;

    // Computed properties for the route card display
    get routeName(): string {
        return this.route.name || 'Unnamed Route';
    }

    get routeDescription(): string {
        // Extract start and end points from the route name or segments
        const segments = this.route.segments || [];
        if (segments.length >= 1) {
            const segment = segments[0];
            return this.getLocationName(segment);
        }
        return 'Route details not available';
    }

    get totalDistance(): number {
        // Calculate total distance from segments (simplified calculation)
        const segments = this.route.segments || [];
        return segments.length * 100; // Simplified: assume 100 miles per segment
    }

    get estimatedTime(): number {
        // Calculate estimated time based on distance and transport mode
        const segments = this.route.segments || [];
        let totalHours = 0;

        segments.forEach(segment => {
            switch (segment.mode) {
                case 'TRUCK':
                    totalHours += 2; // 2 hours per segment for trucks
                    break;
                case 'VESSEL':
                    totalHours += 24; // 24 hours per segment for vessels
                    break;
                case 'PLANE':
                    totalHours += 1; // 1 hour per segment for planes
                    break;
                default:
                    totalHours += 2;
            }
        });

        return totalHours;
    }

    get fuelCost(): number {
        // Calculate fuel cost based on distance and transport mode
        const segments = this.route.segments || [];
        let totalCost = 0;

        segments.forEach(segment => {
            switch (segment.mode) {
                case 'TRUCK':
                    totalCost += 50; // $50 per segment for trucks
                    break;
                case 'VESSEL':
                    totalCost += 200; // $200 per segment for vessels
                    break;
                case 'PLANE':
                    totalCost += 100; // $100 per segment for planes
                    break;
                default:
                    totalCost += 50;
            }
        });

        return totalCost;
    }

    get isOptimized(): boolean {
        // Determine if route is optimized based on some criteria
        return this.route.segments && this.route.segments.length <= 3;
    }

    get optimizationStatus(): string {
        return this.isOptimized ? 'Optimized' : 'Needs Optimization';
    }

    get monthlySavings(): number {
        // Calculate monthly savings based on optimization
        return this.isOptimized ? 2100 : 0;
    }

    get savingsPercentage(): number {
        // Calculate savings percentage for progress bar
        return this.isOptimized ? 85 : 0;
    }

    private getLocationName(segment: any): string {
        // Extract location name from segment based on route name
        const routeName = this.route.name.toLowerCase();

        if (routeName.includes('sf-nyc') || routeName.includes('san francisco')) {
            return 'San Francisco, CA → New York, NY';
        } else if (routeName.includes('la-chi') || routeName.includes('los angeles')) {
            return 'Los Angeles, CA → Chicago, IL';
        } else if (routeName.includes('sea') || routeName.includes('seattle')) {
            return 'Seattle, WA → New York, NY';
        } else if (routeName.includes('miami') || routeName.includes('atlanta')) {
            return 'Miami, FL → Atlanta, GA';
        } else if (routeName.includes('boston') || routeName.includes('new york')) {
            return 'Boston, MA → New York, NY';
        }

        return 'Route details not available';
    }
}
