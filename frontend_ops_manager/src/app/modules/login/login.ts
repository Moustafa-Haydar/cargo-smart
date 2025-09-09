import { CommonModule } from '@angular/common';
import { Component, inject, OnInit } from '@angular/core';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { PasswordModule } from 'primeng/password';
import { InputTextModule } from 'primeng/inputtext';
import { ButtonModule } from 'primeng/button';
import { LoginRepository, LoginRequest } from './login.repository';
import { Subject, takeUntil } from 'rxjs';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [
    CommonModule,
    ReactiveFormsModule,
    PasswordModule,
    InputTextModule,
    ButtonModule
  ],
  templateUrl: './login.html',
  styleUrls: ['./login.css']
})

export class Login implements OnInit {
  private destroy$ = new Subject<void>();
  
  private loginRepository = inject(LoginRepository);
  private router = inject(Router);

  private formBuilder = inject(FormBuilder);
  authForm = this.formBuilder.nonNullable.group({
    'username': ['', [Validators.required, Validators.minLength(3)]],
    'password': ['', [Validators.required, Validators.minLength(4)]],
  });

    ngOnInit(): void {
        this.authForm.valueChanges.pipe(takeUntil(this.destroy$)).subscribe(v => {
        // dev log; remove in prod
        console.log('form:', v, 'valid:', this.authForm.valid);
        });
    }

  onSubmit() {
    const credentials: LoginRequest = this.authForm.getRawValue();

    console.log('Credentials:', credentials);

    this.loginRepository.login(credentials)
        .pipe(takeUntil(this.destroy$))
        .subscribe({
        next: (res) => {
            console.log('Login response:', res);
            // If your repo returns the body, check your own field (e.g., res.success)
            // If your repo uses observe:'response', you can check res.ok
            
        },
        error: (error) => {
            console.error('Login failed:', error);
        }
    });
  }
}