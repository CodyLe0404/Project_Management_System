<route>
{
  path: "/403",
  meta: {
    layout: "default",
    hidden: true,
    title: "Access Denied"
  }
}
</route>

<template>
    <div class="flex items-center justify-center min-h-[calc(100vh-4rem)]">
        <div class="text-center">
            <h1 class="text-9xl font-bold text-surface-200 dark:text-surface-700">403</h1>
            <h2 class="text-2xl font-bold mt-4 mb-2 text-surface-900 dark:text-surface-0">Access Denied</h2>
            <p class="text-surface-600 dark:text-surface-400 mb-8 max-w-md mx-auto">
                You do not have the required permissions to view this page. Please contact your administrator if you believe this is an error.
            </p>
            <div class="flex gap-4 justify-center">
                <Button label="Go Home" icon="pi pi-home" @click="goHome" />
                <Button label="Go Back" icon="pi pi-arrow-left" severity="secondary" outlined @click="goBack" />
            </div>
        </div>
    </div>
</template>

<script setup>
import { useRouter } from 'vue-router';
import { Button } from 'primevue';

const router = useRouter();

const goHome = () => {
    router.push('/');
};

const goBack = () => {
    router.go(-1);
};
</script>
