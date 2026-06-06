<route>
{
  meta: {
    title: "Analytics Overview",
    icon: "pi pi-chart-bar",
    hidden: true
  }
}
</route>

<template>
    <div>
        <div class="flex items-center justify-between mb-6">
            <h1 class="text-2xl font-bold">Analytics Overview</h1>
            <Button label="Refresh" icon="pi pi-refresh" outlined @click="refreshStats" />
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            <StatCard 
                v-for="(stat, index) in stats" 
                :key="index"
                :title="stat.title"
                :value="stat.value"
                :trend="stat.trend"
            />
        </div>
    </div>
</template>

<script setup>
import { Button } from 'primevue';
import StatCard from '../../components/Analytics/StatCard.vue';
import { useAnalytics } from '../../composables/Analytics/useAnalytics';

const { stats, refreshStats } = useAnalytics();
</script>
