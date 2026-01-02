<route>
{
  meta: {
    title: "Sample Page",
    icon: "pi pi-star"
  }
}
</route>

<template>
    <div>
        <div class="flex items-center justify-between mb-6">
            <h1 class="text-2xl font-bold text-surface-900 dark:text-surface-0">Sample Page</h1>
            <Button label="Refresh" icon="pi pi-refresh" outlined />
        </div>
        <div class="h-64 bg-surface-50 rounded flex items-center justify-center text-surface-500">
            Sample Content
        </div>
    </div>
</template>

<script setup>
import { Button, Card } from 'primevue';
</script>
