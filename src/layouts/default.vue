<template>
  <div class="flex min-h-screen bg-surface-50 dark:bg-surface-900">
    <!-- Sidebar -->
    <aside 
        class="bg-surface-0 dark:bg-surface-800 border-r border-surface-200 dark:border-surface-700 flex flex-col fixed inset-y-0 left-0 z-50 transition-transform duration-300 transform" 
        :class="{ 
            '-translate-x-full': !sidebarOpenMobile, 
            'translate-x-0': sidebarOpenMobile, 
            'lg:translate-x-0': sidebarOpenDesktop, 
            'lg:-translate-x-full': !sidebarOpenDesktop,
            'w-72': true 
        }"
    >

        <div class="p-6 h-16 flex items-center justify-between border-b border-surface-200 dark:border-surface-700">
            <span class="text-2xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-primary-500 to-indigo-500">
                TESTING
            </span>
            <!-- Sidebar Toggle (Inside) - Always visible when Sidebar is Open -->
            <Button icon="pi pi-bars" text rounded @click="toggleSidebar" />
        </div>
        
        <div class="flex-1 overflow-y-auto py-4 px-3">
            <PanelMenu :model="items" class="w-full border-none" />
        </div>

        <!-- User Profile & Logout -->
        <div class="p-4 border-t border-surface-200 dark:border-surface-700 bg-surface-50 dark:bg-surface-800/50">
            <div class="flex items-center gap-3 mb-3">
                <div class="w-10 h-10 rounded-full bg-primary-100 dark:bg-primary-900 flex items-center justify-center text-primary-600 dark:text-primary-300 font-bold">
                    {{ userInitials }}
                </div>
                <div class="flex-1 min-w-0">
                    <p class="text-sm font-medium text-surface-900 dark:text-surface-0 truncate">
                        {{ authStore.user?.displayName || 'User' }}
                    </p>
                    <p class="text-xs text-surface-500 dark:text-surface-400 truncate">
                        ID: {{ authStore.user?.userId || 'N/A' }}
                    </p>
                </div>
            </div>
            <Button label="Logout" icon="pi pi-sign-out" severity="danger" outlined class="w-full" @click="confirmLogout" />
        </div>
    </aside>

    <!-- Content -->
    <main 
        class="flex-1 transition-all duration-300 overflow-y-auto"
        :class="{ 'lg:ml-72': sidebarOpenDesktop, 'lg:ml-0': !sidebarOpenDesktop }"
    >
        <!-- Topbar -->
        <header class="h-16 bg-surface-0/80 backdrop-blur-md border-b border-surface-200 sticky top-0 z-40 px-6 flex items-center justify-between">
            <div class="flex items-center gap-4">
                <!-- Toggle Button (Outside) - Hidden on Desktop if Sidebar is Open -->
                <div :class="{ 'lg:hidden': sidebarOpenDesktop }">
                    <Button 
                        icon="pi pi-bars" 
                        text 
                        @click="toggleSidebar" 
                    />
                </div>
                
                <span class="font-bold text-lg">Dashboard</span>
            </div>
            
            <div class="w-8"></div>
        </header>

        <div class="p-4 w-full">
            <router-view v-slot="{ Component }">
                <transition name="fade" mode="out-in">
                    <component :is="Component" />
                </transition>
            </router-view>
        </div>
    </main>
    
    <ConfirmDialog />
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';
import { PanelMenu, Button, ConfirmDialog } from 'primevue';
import { useConfirm } from 'primevue/useconfirm';
import { getMenuItems } from '../utils/menu';
import generatedRoutes from 'virtual:generated-pages';
import { useAuthStore } from '../stores/auth';

const router = useRouter();
const authStore = useAuthStore();
const confirm = useConfirm();

// State for Mobile and Desktop sidebars
const sidebarOpenMobile = ref(false);
const sidebarOpenDesktop = ref(true);

function toggleSidebar() {
    if (window.innerWidth >= 1024) { // lg breakpoint
        sidebarOpenDesktop.value = !sidebarOpenDesktop.value;
    } else {
        sidebarOpenMobile.value = !sidebarOpenMobile.value;
    }
}

const userInitials = computed(() => {
    const name = authStore.user?.displayName || 'User';
    return name.substring(0, 2).toUpperCase();
});

// Generate menu items from routes (with permission check)
const items = computed(() => {
    const dynamicItems = getMenuItems(generatedRoutes, router.push, authStore.hasPermission);
    return [
        {
            label: 'Dashboard',
            icon: 'pi pi-home',
            command: () => router.push('/')
        },
        ...dynamicItems
    ];
});

function confirmLogout() {
  confirm.require({
      message: 'Are you sure you want to log out?',
      header: 'Confirmation',
      icon: 'pi pi-exclamation-triangle',
      rejectProps: {
          label: 'Cancel',
          severity: 'secondary',
          outlined: true
      },
      acceptProps: {
          label: 'Logout',
          severity: 'danger'
      },
      accept: () => {
          authStore.logout();
      }
  });
}
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
