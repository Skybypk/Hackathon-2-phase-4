/** @type {import('next').NextConfig} */
const nextConfig = {
  // Enable React Strict Mode for better development experience
  reactStrictMode: true,
  
  // Configure environment variables
  env: {
    // Backend API URL - can be overridden via environment variable
    // Default is localhost:8000 for local development
    BACKEND_URL: process.env.BACKEND_URL || 'http://localhost:8000',
  },
  
  // For Docker production builds
  output: 'standalone',
}

module.exports = nextConfig
