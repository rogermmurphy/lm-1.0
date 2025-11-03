/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  output: 'standalone', // Enable for Docker deployment
  env: {
    API_URL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost',
  },
}

module.exports = nextConfig
