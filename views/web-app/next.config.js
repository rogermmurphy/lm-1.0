/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  output: 'standalone', // Enable for Docker deployment
  
  // Disable X-Powered-By header
  poweredByHeader: false,
  
  // Compress responses
  compress: true,
  
  env: {
    API_URL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost',
  },
  
  // Proxy API calls to nginx gateway (development only)
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: 'http://localhost:80/api/:path*',
      },
    ]
  },
  
  // CORS and security headers
  async headers() {
    return [
      {
        // Allow access from all origins (development/home network)
        source: '/:path*',
        headers: [
          { key: 'Access-Control-Allow-Origin', value: '*' },
          { key: 'Access-Control-Allow-Methods', value: 'GET,POST,PUT,DELETE,OPTIONS' },
          { key: 'Access-Control-Allow-Headers', value: 'X-Requested-With,Content-Type,Authorization' },
          { key: 'Access-Control-Allow-Credentials', value: 'true' },
        ],
      },
    ]
  },
}

module.exports = nextConfig
