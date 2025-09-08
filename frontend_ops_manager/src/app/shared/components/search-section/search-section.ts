import { Component, EventEmitter, Input, Output } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { SelectModule } from 'primeng/select';
// If you use PrimeNG select:

export interface SelectOption {
  label: string;
  value: any;
}

@Component({
  selector: 'search-section',
  standalone: true,
  imports: [CommonModule, FormsModule, SelectModule],
  templateUrl: './search-section.html',
  styleUrls: ['./search-section.css']
})
export class SearchSection {
  // Two-way bound text
  @Input() searchQuery = '';
  @Output() searchQueryChange = new EventEmitter<string>();

  // Two-way bound dropdown value
  @Input() selected: any = null;
  @Output() selectedChange = new EventEmitter<any>();

  // Inputs for dropdown
  @Input({ required: true }) options: SelectOption[] = [];
  @Input() placeHolder = 'Filter…';

  // Extra events (optional)
  @Output() search = new EventEmitter<string>();
  @Output() filterChange = new EventEmitter<any>();

  onSearchInput(value: string) {
    this.searchQuery = value ?? '';
    this.searchQueryChange.emit(this.searchQuery); // <-- required for [(searchQuery)]
    this.search.emit(this.searchQuery);
  }

  onSelectChange(value: any) {
    this.selected = value ?? null;
    this.selectedChange.emit(this.selected);      // <-- required for [(selected)]
    this.filterChange.emit(this.selected);
  }

  clearSearch() {
    this.onSearchInput('');
  }
}
