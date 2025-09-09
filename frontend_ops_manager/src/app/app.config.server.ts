import { mergeApplicationConfig, ApplicationConfig } from '@angular/core';
import { appConfig } from './app.config';
import { provideServerRendering } from '@angular/ssr';

const serverConfig: ApplicationConfig = {
  providers: [provideServerRendering()]
};

export const config: ApplicationConfig = mergeApplicationConfig(appConfig, serverConfig);
