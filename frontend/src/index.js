import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import TokenProvider from './Contexts/TokenContexts';

const rootElement = document.getElementById('root');
const root = ReactDOM.createRoot(rootElement);

root.render(
    <TokenProvider>
        <App />
    </TokenProvider>
);
