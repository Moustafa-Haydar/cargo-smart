import { Component, EventEmitter, inject, Input, OnInit, Output } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, ReactiveFormsModule } from '@angular/forms';
import { Select } from 'primeng/select';

export interface SelectOption {
  label: string;
  value: any;
}

@Component({
  selector: 'app-filter',
  imports: [CommonModule, Select, ReactiveFormsModule],
  templateUrl: './filter.html',
  styleUrls: ['./filter.css']
})

export class FilterComponent implements OnInit {
  // Two-way bound dropdown value
  @Input() selected: any = null;
  @Output() selectedChange = new EventEmitter<any>();

  // Inputs for dropdown
  @Input({ required: true }) options: SelectOption[] = [];
  @Input() placeHolder = 'Filter…';

  // Filter change event
  @Output() filterChange = new EventEmitter<any>();

  private formBuilder = inject(FormBuilder);
  protected filterForm = this.formBuilder.group({
    'category': ['']
  });

  ngOnInit(): void {
    // Initialize form with current values
    this.filterForm.patchValue({
      category: this.selected
    });

    // Listen to form changes and emit events
    this.filterForm.get('category')?.valueChanges.subscribe((value) => {
      this.onSelectChange(value);
    });
  }

  onSelectChange(value: any) {
    this.selected = value ?? null;
    this.selectedChange.emit(this.selected);      // <-- required for [(selected)]
    this.filterChange.emit(this.selected);
  }

  clearFilter() {
    this.onSelectChange(null);
  }
}
