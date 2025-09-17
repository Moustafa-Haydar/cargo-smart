import { ChangeDetectorRef, Component, DestroyRef, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouteCard } from '../../shared/components/route-card/route-card';
import { Route, Shipment } from '../../shared/models/logistics.model';
import { SearchSection } from '../../shared/components/search-section/search-section';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { map, catchError, of, forkJoin } from 'rxjs';

import { RoutesRepository, RouteProposal, ProposalsResponse } from './routes.repository';

@Component({
  selector: 'app-routes',
  standalone: true,
  imports: [CommonModule, SearchSection],
  templateUrl: './routes.html',
  styleUrls: ['./routes.css']
})
export class RoutesPage {
  private routesRepo = inject(RoutesRepository);
  private readonly changeDetectorRef = inject(ChangeDetectorRef);

  destroyRef = inject(DestroyRef);

  // state
  shipments: Array<Shipment & { proposals: RouteProposal[] | null }> = [];
  filteredShipments: Array<Shipment & { proposals: RouteProposal[] | null }> = [...this.shipments];

  searchQuery = '';
  loading = true;
  error: string | null = null;

  // filter state (mirror shipments page)
  selectedCarrier: string | null = null;
  carrierOptions = [
    { label: 'All', value: null },
    { label: 'VAMOSYS', value: 'VAMOSYS' },
    { label: 'KRC LOGISTICS', value: 'KRC LOGISTICS' },
    { label: 'CONSENT TRACK', value: 'CONSENT TRACK' },
  ];

  ngOnInit(): void {
    this.loadShipmentsWithProposals();
  }

  loadShipmentsWithProposals(): void {
    this.loading = true;
    this.error = null;

    this.routesRepo.getShipmentsWithProposals()
      .pipe(
        takeUntilDestroyed(this.destroyRef),
        map(shipments => {
          // For each shipment, get its pre-evaluated proposals from n8n
          const proposalRequests = shipments.map(shipment =>
            this.routesRepo.getRouteProposal(shipment.id).pipe(
              map((response: ProposalsResponse) => {
                // Handle both single proposal and multiple proposals response
                let proposals: RouteProposal[] = [];
                if (response.proposals && response.proposals.length > 0) {
                  // Multiple proposals
                  proposals = response.proposals;
                } else if (response.action) {
                  // Single proposal (backward compatibility)
                  proposals = [{
                    action: response.action,
                    current: response.current,
                    proposal: response.proposal,
                    rationale: response.rationale || '',
                    requires_approval: response.requires_approval || false
                  }];
                }
                return { ...shipment, proposals };
              }),
              catchError(() => of({ ...shipment, proposals: null }))
            )
          );
          return forkJoin(proposalRequests);
        })
      )
      .subscribe({
        next: (requestsObservable) => {
          requestsObservable.subscribe({
            next: (results) => {
              this.shipments = results.filter(result => result !== undefined) as Array<Shipment & { proposals: RouteProposal[] | null }>;
              this.filterShipments();
              this.loading = false;
              this.changeDetectorRef.markForCheck();
            },
            error: (err) => {
              console.error('Failed to load pre-evaluated proposals', err);
              this.error = 'Failed to load route proposals';
              this.loading = false;
              this.changeDetectorRef.markForCheck();
            }
          });
        },
        error: (err) => {
          console.error('Failed to load shipments with proposals', err);
          this.error = 'Failed to load shipments';
          this.shipments = [];
          this.filteredShipments = [];
          this.loading = false;
          this.changeDetectorRef.markForCheck();
        }
      });
  }

  applySearch(q: string) {
    this.searchQuery = q ?? '';
    this.filterShipments();
  }

  applyFilter(carrier: string | null) {
    this.selectedCarrier = carrier ?? null;
    this.filterShipments();
  }

  private filterShipments() {
    const q = this.searchQuery.trim().toLowerCase();

    this.filteredShipments = this.shipments.filter(shipment => {
      // Carrier filter
      const matchesCarrier = !this.selectedCarrier || shipment.carrier_name === this.selectedCarrier;

      const haystack = [
        shipment.id,
        shipment.ref_no,
        shipment.carrier_name,
        shipment.origin?.name,
        shipment.destination?.name
      ]
        .filter(Boolean)
        .join(' ')
        .toLowerCase();

      const matchesQuery = !q || haystack.includes(q);
      return matchesCarrier && matchesQuery;
    });
  }

  // Handle accepting a route proposal
  acceptProposal(shipment: Shipment & { proposals: RouteProposal[] | null }, proposal: RouteProposal) {
    if (!proposal.proposal) return;

    this.routesRepo.applyRouteProposal(shipment.id, proposal.proposal)
      .pipe(takeUntilDestroyed(this.destroyRef))
      .subscribe({
        next: (response) => {
          console.log('Route proposal applied successfully:', response);
          // Reload shipments to get updated data
          this.loadShipmentsWithProposals();
        },
        error: (err) => {
          console.error('Failed to apply route proposal:', err);
          alert('Failed to apply route proposal. Please try again.');
        }
      });
  }

  // Handle rejecting a route proposal
  rejectProposal(shipment: Shipment & { proposals: RouteProposal[] | null }, proposal: RouteProposal) {
    // Simply reload to get fresh proposals
    this.loadShipmentsWithProposals();
  }
}