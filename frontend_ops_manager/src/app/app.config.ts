import { ApplicationConfig, provideBrowserGlobalErrorListeners, provideZonelessChangeDetection } from '@angular/core';
import { provideAnimationsAsync } from '@angular/platform-browser/animations/async';
import { provideRouter } from '@angular/router';
import { provideHttpClient, withFetch } from '@angular/common/http';
import { providePrimeNG } from 'primeng/config';
import Aura from '@primeuix/themes/aura';

import { routes } from './app.routes';
import { provideClientHydration, withEventReplay } from '@angular/platform-browser';
import { definePreset } from '@primeuix/themes';
import { date } from '@primeuix/themes/aura/datepicker';

export const appConfig: ApplicationConfig = {
  providers: [
    provideHttpClient(),
    provideBrowserGlobalErrorListeners(),
    provideZonelessChangeDetection(),
    provideRouter(routes),
    provideClientHydration(withEventReplay()),
    provideHttpClient(withFetch()),
    provideAnimationsAsync(),
        providePrimeNG({
            theme: {
                options: {
                  darkModeSelector: false
                },
                preset: definePreset(Aura, {
                  semantic: {
                    primary: {
                      50:'{cyan.50}',
                      100:'{cyan.100}',
                      200:'{cyan.200}',
                      300:'{cyan.300}',
                      400:'{cyan.400}',
                      500:'{cyan.500}',
                      600:'{cyan.600}',
                      700:'{cyan.700}',
                      800:'{cyan.800}',
                      900:'{cyan.900}',
                      950:'{cyan.950}',
                    }
                  },
                // components: {
                //   tag: {
                //     colorScheme: {
                //       light: {
                //         success: {
                //           color: '#ffffff'
                //         },
                //         danger: {
                //           color: '#ffffff'
                //         },
                //         warn: {
                //           color: '#ffffff'
                //         },
                //       }
                      
                //     },
                    
                //   }
                // }
                })
            }
        })
  ]
};