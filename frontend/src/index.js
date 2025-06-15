import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';

// Vérifiez que le sélecteur correspond à votre HTML
const rootElement = document.getElementById('root');

if (rootElement) {
  const root = ReactDOM.createRoot(rootElement);
  root.render(
    <React.StrictMode>
      <App />
    </React.StrictMode>
  );
} else {
  console.error("Element with id 'root' not found");
}