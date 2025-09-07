import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';

interface ShipmentStatus {
    status: 'Delivered' | 'In-Transit' | 'Delayed';
    percentage: number;
}

@Component({
    selector: 'app-shipment-card',
    standalone: true,
    imports: [CommonModule],
    templateUrl: './shipment-card.component.html',
    styleUrls: ['./shipment-card.component.css']
})
export class ShipmentCardComponent {
    @Input() shipmentId: string = '';
    @Input() type: string = '';
    @Input() origin: string = '';
    @Input() destination: string = '';
    @Input() status: ShipmentStatus = {
        status: 'In-Transit',
        percentage: 0
    };
    @Input() eta?: string;
    @Input() deliveryDate?: string;
    @Input() daysRemaining?: number;

    getStatusColor(): string {
        switch (this.status.status) {
            case 'Delivered':
                return 'var(--green)';
            case 'Delayed':
                return 'var(--orange)';
            case 'In-Transit':
                return 'var(--blue)';
            default:
                return 'var(--blue)';
        }
    }

    getProgressBackground(): string {
        const color = this.getStatusColor();
        return `linear-gradient(to right, ${color} ${this.status.percentage}%, var(--background-color) ${this.status.percentage}%)`;
    }
}
