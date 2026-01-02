<route>
{
  meta: {
    title: "Dashboard",
    icon: "pi pi-home"
  }
}
</route>

<template>
  <div>
    <div class="flex items-center justify-between mb-8">
        <div>
            <h1 class="text-3xl font-bold text-surface-900 dark:text-surface-0">Dashboard</h1>
            <p class="text-surface-500 mt-1">Overview of your system performance.</p>
        </div>
        <div class="flex gap-2">
            <Button label="Refresh" icon="pi pi-refresh" severity="secondary" outlined />
            <Button label="New Project" icon="pi pi-plus" />
        </div>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <Card v-for="stat in stats" :key="stat.title" class="border-l-4" :class="stat.colorClass">
            <template #content>
                <div class="flex justify-between items-start">
                    <div>
                        <span class="block text-surface-500 font-medium mb-1">{{ stat.title }}</span>
                        <div class="text-2xl font-bold text-surface-900">{{ stat.value }}</div>
                    </div>
                </div>
                <div class="mt-4 flex items-center">
                    <span :class="stat.trend > 0 ? 'text-green-500' : 'text-red-500'" class="font-medium text-sm flex items-center gap-1">
                        <i :class="stat.trend > 0 ? 'pi pi-arrow-up' : 'pi pi-arrow-down'" class="text-xs"></i>
                        {{ Math.abs(stat.trend) }}%
                    </span>
                    <span class="text-surface-400 text-sm ml-2">since last month</span>
                </div>
            </template>
        </Card>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <!-- Main Chart Area (Placeholder) -->
        <div class="lg:col-span-2">
            <Card class="h-full">
                <template #title>Activity Overview</template>
                <template #content>
                    <div class="h-64 flex items-center justify-center bg-surface-50 rounded border border-dashed border-surface-200">
                        <span class="text-surface-400">Chart Component Placeholder</span>
                    </div>
                </template>
            </Card>
        </div>

        <!-- Recent Transactions -->
        <div>
            <Card class="h-full">
                <template #title>Recent Files</template>
                <template #content>
                    <ul class="list-none p-0 m-0 flex flex-col gap-4">
                        <li v-for="i in 5" :key="i" class="flex items-center gap-3 p-2 hover:bg-surface-50 rounded transition-colors cursor-pointer">
                            <div class="w-10 h-10 rounded-full bg-primary-100 dark:bg-primary-900 flex items-center justify-center text-primary-600 dark:text-primary-300">
                                <i class="pi pi-file"></i>
                            </div>
                            <div class="flex-1">
                                <h6 class="m-0 font-medium text-surface-800">Document_{{ i }}.pdf</h6>
                                <span class="text-xs text-surface-400">Modified 2h ago</span>
                            </div>
                            <Button icon="pi pi-chevron-right" text rounded severity="secondary" size="small" />
                        </li>
                    </ul>
                </template>
            </Card>
        </div>
    </div>
  </div>
</template>

<script setup>
import { Card, Button } from 'primevue';

const stats = [
    { title: 'Total Users', value: '12,320', trend: 15, colorClass: 'border-blue-500' },
    { title: 'Revenue', value: '$45,230', trend: 8.5, colorClass: 'border-green-500' },
    { title: 'Active Projects', value: '85', trend: -2.3, colorClass: 'border-orange-500' },
    { title: 'System Load', value: '42%', trend: 5, colorClass: 'border-purple-500' },
];
</script>
