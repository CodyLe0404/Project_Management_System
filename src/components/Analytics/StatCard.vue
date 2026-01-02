<template>
    <div class="p-4 bg-surface-0 dark:bg-surface-800 rounded shadow-sm border border-surface-200 dark:border-surface-700">
        <div class="text-surface-500 mb-2">{{ title }}</div>
        <div class="text-2xl font-bold text-primary-500">{{ value }}</div>
        <div v-if="trend" :class="trend > 0 ? 'text-green-500' : 'text-red-500'" class="text-sm mt-1 flex items-center gap-1">
            <i :class="trend > 0 ? 'pi pi-arrow-up' : 'pi pi-arrow-down'"></i>
            <span>{{ Math.abs(trend) }}% vs last month</span>
        </div>
    </div>
</template>

<script setup>
defineProps({
    title: String,
    value: String,
    trend: Number
});
</script>
