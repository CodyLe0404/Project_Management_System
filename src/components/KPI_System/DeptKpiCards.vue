<template>
  <!-- KPI Cards & Metrics Grid -->
  <section class="relative z-10 grid grid-cols-1 md:grid-cols-3 gap-6">
    <!-- Total Tasks Card -->
    <div class="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl p-6 shadow-sm hover:shadow-md transition-all duration-300 flex flex-col justify-between group">
      <div class="flex items-center justify-between">
        <span class="text-xs font-semibold uppercase text-slate-500 dark:text-slate-400 tracking-wider">Total Tasks</span>
        <div class="p-2 rounded-lg bg-indigo-50 dark:bg-indigo-950/40 text-indigo-600 dark:text-indigo-400 group-hover:scale-110 transition-transform duration-300">
          <i class="pi pi-list"></i>
        </div>
      </div>
      <div class="mt-4">
        <div class="text-4xl font-extrabold tracking-tight text-slate-900 dark:text-white">
          {{ totalTasks }}
        </div>
        <div class="mt-3 flex items-center gap-3 text-xs text-slate-600 dark:text-slate-400">
          <span class="flex items-center gap-1 bg-slate-100 dark:bg-slate-800 px-2.5 py-1 rounded-md font-medium border border-slate-200/40 dark:border-slate-700/40">
            <span class="w-1.5 h-1.5 rounded-full bg-indigo-600"></span>
            Mains: {{ totalMainTasks }}
          </span>
          <span class="flex items-center gap-1 bg-slate-100 dark:bg-slate-800 px-2.5 py-1 rounded-md font-medium border border-slate-200/40 dark:border-slate-700/40">
            <span class="w-1.5 h-1.5 rounded-full bg-indigo-300"></span>
            Subs: {{ totalSubTasks }}
          </span>
        </div>
      </div>
    </div>

    <!-- Project On-Time Percentage Card -->
    <div 
      class="border rounded-2xl p-6 shadow-sm hover:shadow-md transition-all duration-300 flex flex-col justify-between group"
      :class="onTimeStatusColorClass.bg"
    >
      <div class="flex items-center justify-between">
        <span class="text-xs font-semibold uppercase text-slate-500 dark:text-slate-400 tracking-wider">Project On-Time %</span>
        <div class="p-2 rounded-lg text-white group-hover:scale-110 transition-transform duration-300" :class="onTimeStatusColorClass.badge">
          <i class="pi pi-check-circle"></i>
        </div>
      </div>
      <div class="mt-4">
        <div class="text-4xl font-extrabold tracking-tight flex items-baseline gap-1" :class="onTimeStatusColorClass.text">
          {{ onTimePercentage }}%
        </div>
        <p class="text-xs text-slate-500 dark:text-slate-400 mt-3 font-medium">
          Based on <span class="font-bold text-slate-700 dark:text-slate-350">{{ onTimeProjectsCount }}</span> on-time or ahead projects out of <span class="font-bold text-slate-700 dark:text-slate-350">{{ totalProjectsCount }}</span> total.
        </p>
      </div>
    </div>

    <!-- Project Statistics Card -->
    <div class="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl p-6 shadow-sm hover:shadow-md transition-all duration-300 flex flex-col justify-between group">
      <div class="flex items-center justify-between">
        <span class="text-xs font-semibold uppercase text-slate-500 dark:text-slate-400 tracking-wider">Portfolio Volume</span>
        <div class="p-2 rounded-lg bg-emerald-50 dark:bg-emerald-950/40 text-emerald-600 dark:text-emerald-400 group-hover:scale-110 transition-transform duration-300">
          <i class="pi pi-briefcase"></i>
        </div>
      </div>
      <div class="mt-4">
        <div class="text-4xl font-extrabold tracking-tight text-slate-900 dark:text-white">
          {{ totalProjectsCount }}
        </div>
        <div class="mt-3 flex flex-wrap items-center gap-1.5 text-[10px] md:text-xs">
          <span class="px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 font-semibold">
            On Time: {{ onTimeProjectsCount }}
          </span>
          <span class="px-2 py-0.5 rounded bg-amber-500/10 text-amber-600 dark:text-amber-400 font-semibold">
            Active: {{ activeProjectsCount }}
          </span>
          <span class="px-2 py-0.5 rounded bg-rose-500/10 text-rose-600 dark:text-rose-400 font-semibold">
            Delay: {{ delayedProjectsCount }}
          </span>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
  totalMainTasks: {
    type: Number,
    required: true
  },
  totalSubTasks: {
    type: Number,
    required: true
  },
  onTimePercentage: {
    type: Number,
    required: true
  },
  onTimeProjectsCount: {
    type: Number,
    required: true
  },
  totalProjectsCount: {
    type: Number,
    required: true
  },
  activeProjectsCount: {
    type: Number,
    required: true
  },
  delayedProjectsCount: {
    type: Number,
    required: true
  }
});

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
