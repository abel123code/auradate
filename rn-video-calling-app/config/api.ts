/**
 * API Configuration
 * Centralized configuration for API endpoints
 */

// Update this URL to your current server (ngrok, render, etc.)
export const API_BASE_URL = 'https:\e957caeafc4b.ngrok-free.app';

// Alternative URLs for different environments
export const API_URLS = {
  production: 'https://mission-two-server.onrender.com',
  development: 'https://3e8b6d5e0948.ngrok-free.app', // Example ngrok URL
  local: 'http://localhost:3001'
};

// Current environment (change this as needed)
export const CURRENT_ENV = 'production' as keyof typeof API_URLS;

// Get the current API URL
export const getApiUrl = () => API_URLS[CURRENT_ENV];

// Export the current API URL as default
export default API_BASE_URL;
