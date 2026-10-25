import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    // Запросы /api проксируются на FastAPI, чтобы не настраивать CORS в разработке.
    proxy: { "/api": "http://localhost:8000" },
  },
});
