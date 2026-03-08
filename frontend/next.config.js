/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'export',
  compress: true,
  images: { unoptimized: true },
  trailingSlash: true,
}

module.exports = nextConfig
