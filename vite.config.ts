import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// https://vitejs.dev/config/
export default defineConfig({
  root: "view",
  plugins: [react()],
  base: "/waltzboard",
  build: {
    outDir: "../waltzboard/api/static",
  },
});
