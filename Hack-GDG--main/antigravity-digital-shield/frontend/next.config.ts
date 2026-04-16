import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  experimental: {
    serverActions: {
      // Raise the Server Action body size limit to match the backend MAX_MEDIA_SIZE (20 MB).
      // Default is 1 MB — file uploads hit this limit before reaching FastAPI,
      // resulting in ERR_CONNECTION_RESET / "TypeError: Failed to fetch" on the client.
      bodySizeLimit: "25mb",
    },
  },
};

export default nextConfig;
