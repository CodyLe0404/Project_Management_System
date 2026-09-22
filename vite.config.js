import { defineConfig } from 'vite'
import fs from 'node:fs'
import path from 'node:path'
import vue from '@vitejs/plugin-vue'
import Pages from 'vite-plugin-pages'
import Layouts from 'vite-plugin-vue-layouts'

function getApiBaseFromConfig() {
  const configPath = path.resolve(process.cwd(), 'backend/config.ini')
  const config = fs.readFileSync(configPath, 'utf8')
  const apiSection = config.match(/\[API\]([\s\S]*?)(?=\r?\n\s*\[[^\]]+\]|$)/i)?.[1]
  const apiUrl = apiSection?.match(/^\s*link_access\s*=\s*(.+?)\s*$/im)?.[1]

  if (!apiUrl) {
    throw new Error(`Missing [API] link_access in ${configPath}`)
  }

  return apiUrl.replace(/\/$/, '')
}

// https://vite.dev/config/
export default defineConfig(({ mode }) => ({
  define: {
    'import.meta.env.VITE_API_BASE': JSON.stringify(
      process.env.VITE_API_BASE || getApiBaseFromConfig()
    ),
  },
  plugins: [
    vue(),
    Pages({
      dirs: 'src/pages',
    }),
    Layouts({
      layoutsDirs: 'src/layouts',
      defaultLayout: 'default',
    }),
  ],
  build: {
    rollupOptions: {
      output: {
        manualChunks(id) {
          if (id.includes('node_modules')) {
            if (id.includes('primevue') || id.includes('primeicons')) {
              return 'primevue';
            }
            if (id.includes('chart.js') || id.includes('vue-chartjs')) {
              return 'chart';
            }
            if (id.includes('vue') || id.includes('pinia') || id.includes('vue-router')) {
              return 'vendor';
            }
            if (id.includes('pako')) {
              return 'pako';
            }
            // default fallback for other node_modules
            return 'vendor-libs';
          }
        }
      }
    },
    chunkSizeWarningLimit: 1000 // Increased slightly to 1MB to reduce noise for moderate chunks
  }
}))
