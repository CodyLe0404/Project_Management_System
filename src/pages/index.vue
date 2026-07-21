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
        <!-- <div class="flex gap-2">
            <Button label="Refresh" icon="pi pi-refresh" severity="secondary" outlined />
            <Button label="New Project" icon="pi pi-plus" />
        </div> -->
    </div>

    <div v-if="loading" class="mb-6 text-surface-500">Loading project summary...</div>
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
        <Card v-for="stat in stats" :key="stat.title" class="border-l-4" :class="stat.colorClass">
            <template #content>
                <div class="flex justify-between items-start">
                    <div>
                        <span class="block text-surface-500 font-medium mb-1">{{ stat.title }}</span>
                        <div class="text-2xl font-bold text-surface-900">{{ stat.value }}</div>
                    </div>
                </div>
                <div v-if="stat.trend !== null" class="mt-4 flex items-center">
                    <span :class="stat.trend > 0 ? 'text-green-500' : 'text-red-500'" class="font-medium text-sm flex items-center gap-1">
                        <i :class="stat.trend > 0 ? 'pi pi-arrow-up' : 'pi pi-arrow-down'" class="text-xs"></i>
                        {{ Math.abs(stat.trend) }}%
                    </span>
                    <span class="text-surface-400 text-sm ml-2">since last month</span>
                </div>
            </template>
        </Card>
    </div>

    
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { Card } from 'primevue'
import { getProjectSummary } from '../services/projectService'
import { useAuthStore } from '../stores/auth';

const authStore = useAuthStore();

const loading = ref(false)
const stats = ref([
  { title: 'Total Projects', value: '0', trend: null, colorClass: 'border-blue-500' },
//   { title: 'Projects Completed', value: '0', trend: null, colorClass: 'border-green-500' },
//   { title: 'Projects On Going', value: '0', trend: null, colorClass: 'border-orange-500' },
  { title: 'Ahead of Schedule', value: '0', trend: null, colorClass: 'border-purple-500' },
  { title: 'On Time', value: '0', trend: null, colorClass: 'border-cyan-500' },
  { title: 'Delayed', value: '0', trend: null, colorClass: 'border-red-500' },
  { title: 'Not Yet Start', value: '0', trend: null, colorClass: 'border-yellow-500' },
  { title: 'No Plan', value: '0', trend: null, colorClass: 'border-slate-500' }
])
//
const loadProjectSummary = async () => {
  loading.value = true

  try {
    const summary = await getProjectSummary(authStore.user.userId)

    // console.log('Project Summary:', summary)
    stats.value = [
      { title: 'Total Projects', value: summary.total_projects ?? 0, trend: null, colorClass: 'border-blue-500' },
    //   { title: 'Projects Completed', value: summary.completed_projects ?? 0, trend: null, colorClass: 'border-green-500' },
    //   { title: 'Projects On Going', value: summary.on_going_projects ?? 0, trend: null, colorClass: 'border-orange-500' },
      { title: 'Ahead of Schedule', value: summary.ahead_of_schedule_projects ?? 0, trend: null, colorClass: 'border-purple-500' },
      { title: 'On Time', value: summary.on_time_projects ?? 0, trend: null, colorClass: 'border-cyan-500' },
      { title: 'Delayed', value: summary.delayed_projects ?? 0, trend: null, colorClass: 'border-red-500' },
      { title: 'Not Yet Start', value: summary.not_yet_start_projects ?? 0, trend: null, colorClass: 'border-yellow-500' },
      { title: 'No Plan', value: summary.no_plan_projects ?? 0, trend: null, colorClass: 'border-slate-500' }
    ]
  }
  catch (error) {
    console.error('Failed to load project summary', error)
  }
  finally {
    loading.value = false
  }
}

onMounted(loadProjectSummary)
</script>
