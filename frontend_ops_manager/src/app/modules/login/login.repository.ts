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
        return this.http.get('/api/accounts/csrf/', { withCredentials: true }).pipe(
            switchMap(() => {
                const csrfToken = this.getCookie('csrftoken');
                return this.http.post<LoginResponse>(
                    '/api/accounts/login/',
                    credentials,
                    {
                        withCredentials: true,
                        headers: { 'X-CSRFToken': csrfToken }
                    }
                );
            }),
            tap(res => {
                console.log('Login repository response:', res);
                if (res?.ok === true && res?.user) {
                    localStorage.setItem('user', JSON.stringify(res.user));
                    localStorage.setItem('isAuthenticated', 'true');
                }
            })
        );
    }

    private getCookie(name: string): string {
        const matches = document.cookie.match(
            new RegExp('(?:^|; )' + name + '=([^;]*)')
        );
        return matches ? decodeURIComponent(matches[1]) : '';
    }


    logout(): Observable<any> {

        return this.http.post('/api/accounts/logout/', {
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