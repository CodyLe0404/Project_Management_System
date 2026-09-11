import { createRouter, createWebHistory } from 'vue-router'
import { setupLayouts } from 'virtual:generated-layouts'
import generatedRoutes from 'virtual:generated-pages'
import { useAuthStore } from './stores/auth';

const routes = setupLayouts(generatedRoutes)

// Aliases and parameterized routes for Failure Cost module
routes.push(
    { path: '/failure-cost', redirect: '/02_Fcost/fcostDashboard' },
    { path: '/failure-cost/dashboard', redirect: '/02_Fcost/fcostDashboard' },
    { path: '/failure-cost/entry', redirect: '/02_Fcost/fcostEntry' },
    { path: '/failure-cost/entry/:id', redirect: to => ({ path: '/02_Fcost/fcostEntry', query: { id: to.params.id } }) },
    { path: '/02_Fcost/fcostEntry/:id', redirect: to => ({ path: '/02_Fcost/fcostEntry', query: { id: to.params.id } }) },
    { path: '/failure-cost/list', redirect: '/02_Fcost/fcostList' }
);

export const router = createRouter({
    history: createWebHistory(),
    routes,
})

// Navigation Guard
router.beforeEach((to, from, next) => {
    const authStore = useAuthStore();

    // 1. Check Auth requirement
    if (to.path !== '/login' && !authStore.isAuthenticated) {
        return next('/login');
    }

    // 2. Prevent logged-in users from visiting login
    if (to.path === '/login' && authStore.isAuthenticated) {
        return next('/');
    }

    // 3. Check specific permission
    if (to.meta.permission) {
        if (!authStore.hasPermission(to.meta.permission)) {
            // User lacks permission -> Redirect to 403
            return next('/403');
        }
    }

    next();
});
