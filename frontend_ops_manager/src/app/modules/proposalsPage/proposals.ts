import { ChangeDetectorRef, Component, DestroyRef, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { SearchSection } from '../../shared/components/search-section/search-section';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { catchError, of } from 'rxjs';
import { AgentProposal, ProposalsResponse } from '../../shared/models/logistics.model';
import { ProposalsRepository } from './proposal.repository';

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
    private readonly repo = inject(ProposalsRepository);

    proposals: AgentProposal[] = [];
    filteredProposals: AgentProposal[] = [...this.proposals];

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
        this.repo.getProposals()
            .pipe(
                catchError(err => {
                    console.error('Failed to load proposals', err);
                    this.error = 'Failed to load route proposals';
                    this.proposals = [];
                    this.filteredProposals = [];
                    this.loading = false;
                    this.changeDetectorRef.markForCheck();
                    return of({ proposals: [], count: 0 } as ProposalsResponse);
                }),
                takeUntilDestroyed(this.destroyRef)
            )
            .subscribe((data: ProposalsResponse) => {
                this.proposals = data.proposals || [];
                this.filterProposals();
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

    acceptProposal(proposal: AgentProposal) {
        if (!proposal.proposal) return;
        this.repo.applyProposal(
            proposal.shipment_id,
            proposal.proposal.route_id,
            proposal.proposal.path || null
        )
            .pipe(
                catchError(err => {
                    console.error('Failed to apply route proposal:', err);
                    alert('Failed to apply route proposal. Please try again.');
                    return of(null);
                }),
                takeUntilDestroyed(this.destroyRef)
            )
            .subscribe(() => {
                this.loadProposals();
            });
    }

    rejectProposal(proposal: AgentProposal) {
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
