import { Injectable, inject } from '@angular/core';
import { CanActivate, Router, ActivatedRouteSnapshot, RouterStateSnapshot } from '@angular/router';
import { Observable, of } from 'rxjs';
import { map, catchError } from 'rxjs/operators';
import { HttpClient } from '@angular/common/http';

@Injectable({
    providedIn: 'root'
})
export class AuthGuard implements CanActivate {
    private router = inject(Router);
    private http = inject(HttpClient);

    canActivate(
        route: ActivatedRouteSnapshot,
        state: RouterStateSnapshot
    ): Observable<boolean> {
        console.log('AuthGuard: Checking authentication for route:', state.url);
        // Check if user is authenticated by calling the backend
        return this.http.get('/api/accounts/me/', { withCredentials: true }).pipe(
            map((response: any) => {
                console.log('AuthGuard: Me endpoint response:', response);
                if (response && response.authenticated === true && response.user) {
                    console.log('AuthGuard: User is authenticated');
                    return true;
                }
                console.log('AuthGuard: User is not authenticated, redirecting to login');
                // If not authenticated, redirect to login
                this.router.navigate(['/login'], {
                    queryParams: { returnUrl: state.url }
                });
                return false;
            }),
            catchError((error) => {
                console.log('AuthGuard: Error checking authentication:', error);
                // If API call fails, redirect to login
                this.router.navigate(['/login'], {
                    queryParams: { returnUrl: state.url }
                });
                return of(false);
            })
        );
    }
}
