import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError, map } from 'rxjs/operators';

export interface LoginRequest {
    username: string;
    password: string;
}

export interface User {
    id: string;
    first_name: string;
    last_name: string;
    username: string;
    email: string;
}

export interface LoginResponse {
    ok: boolean;
    user: User;
}

export interface ApiError {
    message: string;
    errors?: { [key: string]: string[] };
}

@Injectable({
    providedIn: 'root'
})
export class LoginRepository {
    private readonly API_BASE_URL = 'http://localhost:8000';

    constructor(private http: HttpClient) { }

    /**
     * Authenticate user with username and password
     * Uses cookie-based session authentication
     */
    login(credentials: LoginRequest): Observable<LoginResponse> {
        const url = `${this.API_BASE_URL}/accounts/login/`;

        return this.http.post<LoginResponse>(url, credentials, {
            withCredentials: true
        }).pipe(
            map(response => {
                if (response.ok && response.user) {
                    localStorage.setItem('user', JSON.stringify(response.user));
                    localStorage.setItem('isAuthenticated', 'true');
                }
                console.log(response);
                return response;
            })
        );
    }

    logout(): Observable<any> {
        const url = `${this.API_BASE_URL}/accounts/logout/`;

        return this.http.post(url, {}, {
            withCredentials: true
        }).pipe(
            map(() => {
                localStorage.removeItem('user');
                localStorage.removeItem('isAuthenticated');
                return true;
            })
        );
    }

}