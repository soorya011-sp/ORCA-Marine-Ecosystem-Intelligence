import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import tailwindcss from "@tailwindcss/vite";

export default defineConfig({
  plugins: [
    react(),
    tailwindcss(),
  ],

  preview: {
    host: "0.0.0.0",
    allowedHosts: [
      "orca-marine-ecosystem-intelligence-2.onrender.com",
    ],
  },
});