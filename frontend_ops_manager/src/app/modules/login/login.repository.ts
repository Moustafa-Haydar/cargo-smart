import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError, map, switchMap, tap } from 'rxjs/operators';

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


    login(credentials: LoginRequest) {
        return this.http.get('/accounts/csrf/', { withCredentials: true }).pipe(
            switchMap(() =>
                this.http.post<LoginResponse>('/accounts/login/', credentials, {
                    withCredentials: true
                })
                ),
            tap((res) => {
                if ((res as any)?.user) {
                    localStorage.setItem('user', JSON.stringify((res as any).user));
                    localStorage.setItem('isAuthenticated', 'true');
                    
                }
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