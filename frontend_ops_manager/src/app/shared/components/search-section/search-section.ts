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
imports: [CommonModule, Select, InputText, ReactiveFormsModule, InputIcon, IconField ],
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
    'search' : [''],
    'category' : ['']
  });

  ngOnInit(): void {
      // will be called on every initialize
      this.searchForm.valueChanges.subscribe((value) => {
        console.log(value);
      })
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
