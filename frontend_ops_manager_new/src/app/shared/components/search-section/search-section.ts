import { Component, EventEmitter, inject, Input, OnInit, Output } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, ReactiveFormsModule } from '@angular/forms';
import { Select } from 'primeng/select';
import { InputText } from 'primeng/inputtext';
import { InputIcon } from 'primeng/inputicon';
import { IconField } from 'primeng/iconfield';

export interface SelectOption {
  label: string;
  value: any;
}

@Component({
  selector: 'search-section',
  imports: [CommonModule, Select, InputText, ReactiveFormsModule, InputIcon, IconField],
  templateUrl: './search-section.html',
  styleUrls: ['./search-section.css']
})

export class SearchSection implements OnInit {
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


  private formBuilder = inject(FormBuilder);
  protected searchForm = this.formBuilder.group({
    'search': [''],
    'category': ['']
  });

  ngOnInit(): void {
    // Initialize form with current values
    this.searchForm.patchValue({
      search: this.searchQuery,
      category: this.selected
    });

    // Listen to form changes and emit events
    this.searchForm.get('search')?.valueChanges.subscribe((value) => {
      this.onSearchInput(value || '');
    });

    this.searchForm.get('category')?.valueChanges.subscribe((value) => {
      this.onSelectChange(value);
    });
  }

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
