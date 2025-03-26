import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      // Proxy API requests to the FastAPI backend
      '/query': 'http://localhost:8000',
      '/query-stream': 'http://localhost:8000',
      '/clear-cache': 'http://localhost:8000',
      '/data': 'http://localhost:8000',
      '/health': 'http://localhost:8000',
      '/dev-version': 'http://localhost:8000'
    }
  }
}) 