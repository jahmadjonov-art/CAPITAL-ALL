import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// GitHub Pages serves this app from
// https://<user>.github.io/CAPITAL-ALL/budget/ — it moved down one level on
// 2026-09-18 when the front page at /CAPITAL-ALL/ became a list of the two
// sites published here. Every asset URL needs that prefix. If you ever move to
// a custom domain or another host, set BASE_PATH=/ in the build environment.
const base = process.env.BASE_PATH || '/CAPITAL-ALL/budget/'

export default defineConfig({
  base,
  plugins: [react()],
  server: { port: 5173 },
  build: { outDir: 'dist', sourcemap: false },
})
