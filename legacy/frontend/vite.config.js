import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// GitHub Pages serves this project from https://<user>.github.io/CAPITAL-ALL/,
// so every asset URL needs that prefix. If you ever move to a custom domain or
// another host, set BASE_PATH=/ in the build environment.
const base = process.env.BASE_PATH || '/CAPITAL-ALL/'

export default defineConfig({
  base,
  plugins: [react()],
  server: { port: 5173 },
  build: { outDir: 'dist', sourcemap: false },
})
