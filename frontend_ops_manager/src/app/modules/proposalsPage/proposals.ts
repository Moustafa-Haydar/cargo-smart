import { ChangeDetectorRef, Component, DestroyRef, inject, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { SearchSection } from '../../shared/components/search-section/search-section';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { catchError, map, of, tap } from 'rxjs';
import { AgentProposal, ProposalsResponse } from '../../shared/models/logistics.model';
import { ProposalsRepository } from './proposal.repository';

@Component({
    selector: 'app-proposals',
    standalone: true,
    imports: [CommonModule, SearchSection],
    templateUrl: './proposals.html',
    styleUrls: ['./proposals.css']
})
export class ProposalsPage implements OnInit {
    private repo = inject(ProposalsRepository);
    private readonly changeDetectorRef = inject(ChangeDetectorRef);

    destroyRef = inject(DestroyRef);

    proposals: AgentProposal[] = [];
    filteredProposals: AgentProposal[] = [];
    loading = true;

    searchQuery = '';
    error: string | null = null;
    successMessage: string | null = null;

    selectedAction: string | null = null;
    actionOptions = [
        { label: 'All', value: null },
        { label: 'Propose Switch', value: 'propose_switch' },
        { label: 'Stick', value: 'stick' },
    ];

    ngOnInit(): void {
        // load data first, then filter
        this.repo.getProposals().pipe(takeUntilDestroyed(this.destroyRef), map(res => res.proposals ?? []))
            .subscribe({
                next: (data) => {
                    this.proposals = data ?? [];
                    this.filterProposals();
                    this.loading = false;
                    this.changeDetectorRef.markForCheck();
                },
                error: (err) => {
                    console.error('Failed to load proposals', err);
                    this.proposals = [];
                    this.filteredProposals = [];
                    this.loading = false;
                }
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

    // Formatting helpers for template
    formatTime(minutes?: number | null): string {
        const total = Number(minutes ?? 0);
        const hours = Math.floor(total / 60);
        const mins = total % 60;
        return hours > 0 ? `${hours}h ${mins}m` : `${mins}m`;
    }

    formatDelayRisk(pDelay?: number | null): string {
        const v = Number(pDelay ?? 0);
        return `${(v * 100).toFixed(1)}%`;
    }

    acceptProposal(proposal: AgentProposal) {
        // Set loading state
        (proposal as any).accepting = true;
        this.changeDetectorRef.markForCheck();

        // Simulate API call with a delay
        setTimeout(() => {
            // Show success message
            this.successMessage = 'Proposal accepted successfully!';
            this.clearMessages();

            // Remove the proposal from the list
            this.proposals = this.proposals.filter(p => p.id !== proposal.id);
            this.filterProposals();
            this.changeDetectorRef.markForCheck();
        }, 1000); // 1 second delay to show loading state
    }

    rejectProposal(proposal: AgentProposal) {
        // For now, just remove from the list
        // You can implement a proper reject API call later
        this.proposals = this.proposals.filter(p => p.id !== proposal.id);
        this.filterProposals();
        this.changeDetectorRef.markForCheck();
    }

    // Helper method to check if proposal is accepting
    isAccepting(proposal: AgentProposal): boolean {
        return (proposal as any).accepting === true;
    }

    // Clear messages after a delay
    private clearMessages() {
        setTimeout(() => {
            this.error = null;
            this.successMessage = null;
            this.changeDetectorRef.markForCheck();
        }, 5000); // Clear after 5 seconds
    }
}
