import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
// ✅ Adjust the path to match your actual file name (logistics.model vs logistics.models)
import { Shipment, Milestone } from '../../models/logistics.model';
import { Card } from 'primeng/card';

@Component({
  selector: 'shipment-card',
  standalone: true,
  imports: [CommonModule, Card],
  templateUrl: './shipment-card.html',
  styleUrls: ['./shipment-card.css']
})
export class ShipmentCard {
  @Input({ required: true }) shipment!: Shipment;

  // --- Convenience getters to keep your existing template props working ---
  get shipmentId(): string { return this.shipment.ref_no ?? this.shipment.id; }
  get type(): string { return this.shipment.shipment_type; }
  get origin(): string { return this.shipment.origin?.name ?? '-'; }
  get destination(): string { return this.shipment.destination?.name ?? '-'; }

  // --- Status mapping (domain -> UI) ---
  get isDelayed(): boolean {
    const ms = this.shipment.milestones ?? [];
    // delayed if any upcoming milestone has a predictive_eta in the past
    return ms.some(m => !m.actual && !!m.predictive_eta && new Date(m.predictive_eta) < new Date());
  }

  get uiStatus(): 'Delivered' | 'In-Transit' | 'Planned' | 'Delayed' {
    if (this.isDelayed) return 'Delayed';
    switch (this.shipment.status) {
      case 'DELIVERED':   return 'Delivered';
      case 'IN_TRANSIT':  return 'In-Transit';
      case 'DELAYED': return 'Delayed';
      case 'CREATED':     return 'Planned';
      default:            return 'In-Transit';
    }
  }

  // Color variables assume you have these CSS vars defined in your theme
  getStatusColor(): string {
    if (this.uiStatus === 'Delayed') return 'var(--orange)';
    switch (this.shipment.status) {
      case 'DELIVERED':  return 'var(--green)';
      case 'IN_TRANSIT': return 'var(--blue)';
      case 'CREATED':    return 'var(--slate-400)'; // fallback color for planned
      default:           return 'var(--blue)';
    }
  }

  // Progress %
  get progressPercentage(): number {
    if (typeof this.shipment.progress_pct === 'number') return this.shipment.progress_pct;
    switch (this.shipment.status) {
      case 'DELIVERED':  return 100;
      case 'IN_TRANSIT': return 50;
      case 'CREATED':    return 0;
      default:           return 0;
    }
  }

  getProgressBackground(): string {
    const color = this.getStatusColor();
    const pct = this.progressPercentage;
    return `linear-gradient(to right, ${color} ${pct}%, var(--background-color) ${pct}%)`;
    // If you use a dedicated progress bar element, bind [style.width.%]="progressPercentage" instead.
  }

  // --- ETA / Delivery dates & remaining days ---
  private get predictedEtaISO(): string | undefined {
    const ms = this.shipment.milestones ?? [];
    const next = ms.find(m => !m.actual && m.predictive_eta);
    return next?.predictive_eta ?? undefined;
  }

  get eta(): string | undefined {
    return this.predictedEtaISO;
  }

  get deliveryDate(): string | undefined {
    return this.shipment.delivered_at ?? undefined;
  }

  get daysRemaining(): number | undefined {
    const iso = this.predictedEtaISO;
    if (!iso) return undefined;
    const now = Date.now();
    const etaMs = new Date(iso).getTime();
    const diff = etaMs - now;
    if (diff <= 0) return 0;
    return Math.ceil(diff / (1000 * 60 * 60 * 24));
  }
}
