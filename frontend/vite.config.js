import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  // base: prefijo de las rutas de los archivos (JS/CSS) en el build.
  // Cuando desplegamos el frontend por separado (Vercel) queremos
  // que los assets se sirvan desde la raíz '/' — no desde '/static/'.
  // Detectamos si estamos en Vercel con la variable de entorno
  // `VERCEL` y cambiamos el base en consecuencia.
  base: process.env.VERCEL ? '/' : '/static/',
  plugins: [react()],
  server: {
    port: 5173,
    // PROXY: cualquier petición a /api... hecha desde el navegador
    // (ej: fetch('/api/')) se reenvía a Django, que corre en el 8000.
    // Así el frontend puede hablar con el backend SIN problemas de CORS.
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
    },
  },
})
