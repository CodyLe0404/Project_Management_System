import { createRouter, createWebHistory } from 'vue-router'
import { setupLayouts } from 'virtual:generated-layouts'
import generatedRoutes from 'virtual:generated-pages'
import { useAuthStore } from './stores/auth';

const routes = setupLayouts(generatedRoutes)

export const router = createRouter({
    history: createWebHistory(),
    routes,
})

// Navigation Guard
// router.beforeEach((to, from, next) => {
//     const authStore = useAuthStore();

//     // 1. Check Auth requirement
//     if (to.path !== '/login' && !authStore.isAuthenticated) {
//         return next('/login');
//     }

//     // 2. Prevent logged-in users from visiting login
//     if (to.path === '/login' && authStore.isAuthenticated) {
//         return next('/');
//     }

//     // 3. Check specific permission
//     if (to.meta.permission) {
//         if (!authStore.hasPermission(to.meta.permission)) {
//             // User lacks permission -> Redirect to 403
//             return next('/403');
//         }
//     }

//     next();
// });
