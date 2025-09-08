// login.component.ts
import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './login.html',
  styleUrls: ['./login.css']
})
export class Login {
  username = '';
  password = '';
  showPassword = false;
  loading = false;
  error: string | null = null;

  handleLogin() {
    this.loading = true;
    this.error = null;

    // Example: call your login API here
    console.log('Login attempt', { username: this.username, password: this.password });

    setTimeout(() => {
      if (this.username === 'admin' && this.password === 'admin123') {
        console.log('Login successful');
        // TODO: redirect to dashboard
      } else {
        this.error = 'Invalid username or password';
      }
      this.loading = false;
    }, 1000);
  }

  handleForgotPassword() {
    console.log('Forgot password clicked');
    // TODO: implement forgot password logic
  }
}
