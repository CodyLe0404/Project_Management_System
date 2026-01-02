import { createApp } from 'vue'
import { createPinia } from 'pinia'
import PrimeVue from 'primevue/config'
import Aura from '@primevue/themes/aura'
import ConfirmationService from 'primevue/confirmationservice';
import './styles/main.css'
import App from './App.vue'
import { router } from './router'
import { EnCoApiClientService } from './services/EnCo/EnCoApiClientService.js';

const app = createApp(App)

// Setup API Client
const apiClient = new EnCoApiClientService(import.meta.env.VITE_API_BASE_URL);
app.provide('apiClient', apiClient);

app.use(router)
app.use(createPinia())
app.use(ConfirmationService)
app.use(PrimeVue, {
    theme: {
        preset: Aura,
        options: {
            darkModeSelector: '.dark', // Explicitly control dark mode with a class
        }
    }
})

app.mount('#app')
