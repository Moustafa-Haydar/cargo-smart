import { CommonModule } from '@angular/common';
import { Component, inject, OnInit } from '@angular/core';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { Router, ActivatedRoute } from '@angular/router';
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
    ButtonModule,
  ],
  templateUrl: './login.html',
  styleUrls: ['./login.css']
})

export class Login {
  private destroy$ = new Subject<void>();

  private loginRepository = inject(LoginRepository);
  private router = inject(Router);
  private route = inject(ActivatedRoute);

  private formBuilder = inject(FormBuilder);
  protected authForm = this.formBuilder.nonNullable.group({
    'username': ['', [Validators.required, Validators.minLength(3)]],
    'password': ['', [Validators.required, Validators.minLength(4)]],
  });

  onSubmit() {
    if (this.authForm.invalid) {
      this.authForm.markAllAsTouched();
      return;
    }

    const credentials: LoginRequest = this.authForm.getRawValue();
    console.log('Credentials:', credentials);

    this.loginRepository.login(credentials)
      .pipe(takeUntil(this.destroy$))
      .subscribe({
        next: (res) => {
          const ok = (res as any)?.user || (res as any)?.success === true;
          if (ok) {
            // Get return URL from query params, default to live-map
            const returnUrl = this.route.snapshot.queryParams['returnUrl'] || '/live-map';
            this.router.navigate([returnUrl]);
          } else {
            console.error('Login failed: unexpected response');
          }
        },
        error: (error) => {
          console.error('Login failed:', error);
        }
      });
  }
}