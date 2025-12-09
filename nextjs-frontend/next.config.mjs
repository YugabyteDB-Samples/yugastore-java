/** @type {import('next').NextConfig} */
const nextConfig = {
    images: {
        remotePatterns: [
            {
                protocol: 'http',
                hostname: 'ecx.images-amazon.com',
            },
            {
                protocol: 'https',
                hostname: 'ecx.images-amazon.com',
            },
            {
                protocol: 'http',
                hostname: 'images-na.ssl-images-amazon.com',
            },
            {
                protocol: 'https',
                hostname: 'images-na.ssl-images-amazon.com',
            }
        ],
        unoptimized: true
    }
};

export default nextConfig;
