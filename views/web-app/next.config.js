/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  output: 'standalone', // Enable for Docker deployment
  
  // Allow access from any network interface (0.0.0.0)
  // This enables access via localhost, 192.168.x.x, and public IP
  experimental: {
    allowMiddlewareResponseBody: true,
  },
  
  env: {
    API_URL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost',
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
