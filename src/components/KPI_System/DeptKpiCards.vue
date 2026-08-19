<template>
  <!-- KPI Cards & Metrics Grid -->
  <section class="relative z-10 grid grid-cols-1 md:grid-cols-3 gap-6">
    <!-- Total Tasks Card -->
    <div class="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl p-6 shadow-sm hover:shadow-md transition-all duration-300 flex flex-col justify-between group">
      <div class="flex items-center justify-between">
        <span class="text-xs font-semibold uppercase text-slate-500 dark:text-slate-400 tracking-wider">Total Project</span>
        <div class="p-2 rounded-lg bg-indigo-50 dark:bg-indigo-950/40 text-indigo-600 dark:text-indigo-400 group-hover:scale-110 transition-transform duration-300">
          <i class="pi pi-list"></i>
        </div>
      </div>
      <div class="mt-4">
        <div class="text-4xl font-extrabold tracking-tight text-slate-900 dark:text-white">
          {{ totalProject }}
        </div>
        <div class="mt-3 flex items-center gap-3 text-xs text-slate-600 dark:text-slate-400">
          <span class="flex items-center gap-1 bg-slate-100 dark:bg-slate-800 px-2.5 py-1 rounded-md font-medium border border-slate-200/40 dark:border-slate-700/40">
            <span class="w-1.5 h-1.5 rounded-full bg-indigo-600"></span>
            Total Main Task: {{ totalMainTask }}
          </span>
          <span class="flex items-center gap-1 bg-slate-100 dark:bg-slate-800 px-2.5 py-1 rounded-md font-medium border border-slate-200/40 dark:border-slate-700/40">
            <span class="w-1.5 h-1.5 rounded-full bg-indigo-300"></span>
            Total Subtask: {{ totalSubTask }}
          </span>
        </div>
      </div>
    </div>

    <!-- Electrical On-Time Percentage Card -->
    <div 
      class="border rounded-2xl p-6 shadow-sm hover:shadow-md transition-all duration-300 flex flex-col justify-between group"
      :class="onTimeStatusColorClass.bg"
    >
      <div class="flex items-center justify-between">
        <span class="text-xs font-semibold uppercase text-slate-500 dark:text-slate-400 tracking-wider">Electrical subtask On-Time %</span>
        <div class="p-2 rounded-lg text-white group-hover:scale-110 transition-transform duration-300" :class="onTimeStatusColorClass.badge">
          <i class="pi pi-check-circle"></i>
        </div>
      </div>
      <div class="mt-4">
        <div class="text-4xl font-extrabold tracking-tight flex items-baseline gap-1" :class="onTimeStatusColorClass.text">
          {{ subTaskOnTimeElectrical }}%
        </div>
        <p class="text-xs text-slate-500 dark:text-slate-400 mt-3 font-medium">
          On Time of Total.
        </p>
      </div>
    </div>

    <!-- Mechanical On-Time Percentage Card -->
    <div 
      class="border rounded-2xl p-6 shadow-sm hover:shadow-md transition-all duration-300 flex flex-col justify-between group"
      :class="onTimeStatusColorClass.bg"
    >
      <div class="flex items-center justify-between">
        <span class="text-xs font-semibold uppercase text-slate-500 dark:text-slate-400 tracking-wider">Mechanical subtask On-Time %</span>
        <div class="p-2 rounded-lg text-white group-hover:scale-110 transition-transform duration-300" :class="onTimeStatusColorClass.badge">
          <i class="pi pi-check-circle"></i>
        </div>
      </div>
      <div class="mt-4">
        <div class="text-4xl font-extrabold tracking-tight flex items-baseline gap-1" :class="onTimeStatusColorClass.text">
          {{ subTaskOnTimeMechanical }}%
        </div>
        <p class="text-xs text-slate-500 dark:text-slate-400 mt-3 font-medium">
          On Time of Total.
        </p>
      </div>
    </div>
  </section>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
  deptKpiSummaryData: {
    type: Object,
    required: true
  }
});

const totalProject = computed(() => {
  return props.deptKpiSummaryData.project
})

const totalMainTask = computed(() => {
  return props.deptKpiSummaryData.mainTask.total
})

const totalSubTask = computed(() => {

  const mechanical =
    props.deptKpiSummaryData.subTask["Design (M)"].total

  const electrical =
    props.deptKpiSummaryData.subTask["Design (E)"].total

  return mechanical + electrical
})

const subTaskOnTimeMechanical = computed(() => {
  const percent = props.deptKpiSummaryData.subTask["Design (M)"]
  if (percent.total === 0) {
    return 0
  }
  return Math.round((percent.onTime / percent.total) * 100 * 100) / 100
})

const subTaskOnTimeElectrical = computed(() => {
  const percent =props.deptKpiSummaryData.subTask["Design (E)"]
  if (percent.total === 0) {
    return 0
  }
  return Math.round((percent.onTime / percent.total) * 100 * 100) / 100
})

const totalTasks = computed(() => props.totalMainTasks + props.totalSubTasks);

// Dynamic Class Color Binding according to requirements (>90% Green, 70-90% Yellow, <70% Red)
const onTimeStatusColorClass = computed(() => {
  const pct = props.onTimePercentage;
  if (pct > 90) {
    return {
      text: 'text-emerald-600 dark:text-emerald-400',
      bg: 'bg-emerald-50 dark:bg-emerald-950/20 border-emerald-200 dark:border-emerald-800/40 text-emerald-800 dark:text-emerald-200',
      badge: 'bg-emerald-500'
    };
  } else if (pct >= 70) {
    return {
      text: 'text-amber-600 dark:text-amber-400',
      bg: 'bg-amber-50 dark:bg-amber-950/20 border-amber-200 dark:border-amber-800/40 text-amber-800 dark:text-amber-200',
      badge: 'bg-amber-500'
    };
  } else {
    return {
      text: 'text-rose-600 dark:text-rose-400',
      bg: 'bg-rose-50 dark:bg-rose-950/20 border-rose-200 dark:border-rose-800/40 text-rose-800 dark:text-rose-200',
      badge: 'bg-rose-500'
    };
  }
});
</script>
