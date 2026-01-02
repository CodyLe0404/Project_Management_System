import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import Pages from 'vite-plugin-pages'
import Layouts from 'vite-plugin-vue-layouts'

// https://vite.dev/config/
export default defineConfig({
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
})
