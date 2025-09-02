import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import {AuthProvider} from "./Contexts/AuthContext";

const rootElement = document.getElementById('root');
const root = ReactDOM.createRoot(rootElement);

root.render(
    <AuthProvider>
        <App />
    </AuthProvider>
);
