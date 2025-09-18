import { CommonModule } from '@angular/common';
import { Component, inject, OnInit } from '@angular/core';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { Router, ActivatedRoute } from '@angular/router';
import { PasswordModule } from 'primeng/password';
import { InputTextModule } from 'primeng/inputtext';
import { ButtonModule } from 'primeng/button';
import { LoginRepository, LoginRequest } from './login.repository';
import { finalize, Subject, takeUntil } from 'rxjs';
import { ProgressSpinnerModule } from 'primeng/progressspinner';
import { MessageModule } from 'primeng/message';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [
    CommonModule,
    ReactiveFormsModule,
    PasswordModule,
    InputTextModule,
    ButtonModule,
    ProgressSpinnerModule,
    MessageModule
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

  loading = false;
  errorMessage = "";

  onSubmit() {
    if (this.authForm.invalid) {
      this.authForm.markAllAsTouched();
      return;
    }

    this.loading = true;
    this.errorMessage = "";

    const credentials: LoginRequest = this.authForm.getRawValue();

    this.loginRepository.login(credentials)
      .pipe(takeUntil(this.destroy$),
        finalize(() => this.loading = false))
      .subscribe({
        next: (res) => {
          console.log('Login response:', res);
          const ok = (res as any)?.ok === true && (res as any)?.user;
          if (ok) {
            // Get return URL from query params, default to live-map
            const returnUrl = this.route.snapshot.queryParams['returnUrl'] || '/live-map';
            console.log('Login successful, redirecting to:', returnUrl);

            // Use Angular router navigation
            this.router.navigateByUrl(returnUrl).then(success => {
              if (!success) {
                console.error('Navigation failed, trying window.location');
                window.location.href = returnUrl;
              }
            });
          } else {
            console.error('Login failed: unexpected response', res);
            this.errorMessage = "Invalid credentials. Please try again.";
            this.loading = false;
          }
        },
        error: (error) => {
          console.error('Login failed:', error);
          this.errorMessage = "Invalid username or password";
          this.loading = false;
        },
        complete: () => {
          this.loading = false;
        }
      });
  }
}