import { ChangeDetectorRef, Component, DestroyRef, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { SearchSection } from '../../shared/components/search-section/search-section';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { catchError, of } from 'rxjs';

// Proposal interface
export interface RouteProposal {
    id: string;
    shipment_id: string;
    action: 'stick' | 'propose_switch';
    current: {
        route_id: string;
        eta_minutes: number;
        toll_cost_usd: number;
        path: string[];
        p_delay: number;
    };
    proposal?: {
        route_id: string;
        eta_minutes: number;
        toll_cost_usd: number;
        path: string[];
        p_delay: number;
    };
    rationale: string;
    requires_approval: boolean;
    created_at: string;
}

// Response interface
export interface ProposalsResponse {
    proposals: RouteProposal[];
    count: number;
}

@Component({
    selector: 'app-proposals',
    standalone: true,
    imports: [CommonModule, SearchSection],
    templateUrl: './proposals.html',
    styleUrls: ['./proposals.css']
})
export class ProposalsPage {
    private readonly changeDetectorRef = inject(ChangeDetectorRef);
    destroyRef = inject(DestroyRef);

    proposals: RouteProposal[] = [];
    filteredProposals: RouteProposal[] = [...this.proposals];

    searchQuery = '';
    loading = true;
    error: string | null = null;

    selectedAction: string | null = null;
    actionOptions = [
        { label: 'All', value: null },
        { label: 'Propose Switch', value: 'propose_switch' },
        { label: 'Stick', value: 'stick' },
    ];

    ngOnInit(): void {
        this.loadProposals();
    }

    public loadProposals(): void {
        this.loading = true;
        this.error = null;

        // Fetch proposals from the new API
        fetch('/api/agentic/proposals/', {
            method: 'GET',
            credentials: 'include',
            headers: {
                'Content-Type': 'application/json',
            }
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.json();
            })
            .then((data: ProposalsResponse) => {
                this.proposals = data.proposals || [];
                this.filterProposals();
                this.loading = false;
                this.changeDetectorRef.markForCheck();
            })
            .catch(err => {
                console.error('Failed to load proposals', err);
                this.error = 'Failed to load route proposals';
                this.proposals = [];
                this.filteredProposals = [];
                this.loading = false;
                this.changeDetectorRef.markForCheck();
            });
    }

    applySearch(q: string) {
        this.searchQuery = q ?? '';
        this.filterProposals();
    }

    applyFilter(action: string | null) {
        this.selectedAction = action ?? null;
        this.filterProposals();
    }

    private filterProposals() {
        const q = this.searchQuery.trim().toLowerCase();

        this.filteredProposals = this.proposals.filter(proposal => {
            const matchesAction = !this.selectedAction || proposal.action === this.selectedAction;

            const haystack = [
                proposal.id,
                proposal.shipment_id,
                proposal.action,
                proposal.rationale,
                proposal.current?.route_id,
                proposal.proposal?.route_id
            ]
                .filter(Boolean)
                .join(' ')
                .toLowerCase();

            const matchesQuery = !q || haystack.includes(q);
            return matchesAction && matchesQuery;
        });
    }

    acceptProposal(proposal: RouteProposal) {
        if (!proposal.proposal) return;

        // Apply the proposal using the existing API
        fetch(`/api/agentic/shipments/${proposal.shipment_id}/apply/`, {
            method: 'POST',
            credentials: 'include',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                proposed_route_id: proposal.proposal.route_id,
                path: proposal.proposal.path
            })
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.json();
            })
            .then((response) => {
                console.log('Route proposal applied successfully:', response);
                this.loadProposals(); // Reload to update the list
            })
            .catch(err => {
                console.error('Failed to apply route proposal:', err);
                alert('Failed to apply route proposal. Please try again.');
            });
    }

    rejectProposal(proposal: RouteProposal) {
        // For now, just reload the proposals
        // In the future, you might want to mark it as rejected in the database
        this.loadProposals();
    }

    formatTime(minutes: number): string {
        const hours = Math.floor(minutes / 60);
        const mins = minutes % 60;
        return hours > 0 ? `${hours}h ${mins}m` : `${mins}m`;
    }

    formatDelayRisk(pDelay: number): string {
        return `${(pDelay * 100).toFixed(1)}%`;
    }
}
