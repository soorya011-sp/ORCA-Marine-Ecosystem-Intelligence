import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],

  preview: {
    host: "0.0.0.0",
    allowedHosts: [
      "orca-marine-ecosystem-intelligence-2.onrender.com",
    ],
  },
});