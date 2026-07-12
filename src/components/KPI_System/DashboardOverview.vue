<template>
  <div class="space-y-6">
    <!-- Top KPI Cards Grid -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
      
      <!-- Card 1: Overall On-Time Percentage -->
      <div class="relative overflow-hidden bg-white/90 backdrop-blur-md border border-slate-200 rounded-2xl p-6 shadow-xl transition-all duration-300 hover:shadow-primary-500/10 hover:border-slate-300 group">
        <!-- Glowing background accent -->
        <div class="absolute -right-10 -top-10 w-32 h-32 bg-primary-500/10 rounded-full blur-3xl group-hover:bg-primary-500/20 transition-all duration-500"></div>
        
        <div class="flex items-center justify-between mb-4">
          <h3 class="text-sm font-semibold text-slate-600 uppercase tracking-wider">Overall On-Time Performance</h3>
          <div class="p-2 rounded-lg bg-emerald-500/10 text-emerald-600">
            <i class="pi pi-percentage text-lg"></i>
          </div>
        </div>
        
        <div class="flex items-center gap-6">
          <!-- Circular Progress SVG -->
          <div class="relative w-20 h-20 flex-shrink-0">
            <svg class="w-full h-full transform -rotate-90" viewBox="0 0 36 36">
              <path
                class="text-slate-800"
                stroke-width="3"
                stroke="currentColor"
                fill="none"
                d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
              />
              <path
                class="text-emerald-500 transition-all duration-1000 ease-out"
                :stroke-dasharray="`${onTimePercentage}, 100`"
                stroke-width="3.2"
                stroke-linecap="round"
                stroke="currentColor"
                fill="none"
                d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
              />
            </svg>
            <div class="absolute inset-0 flex items-center justify-center">
              <span class="text-lg font-bold text-slate-900">{{ onTimePercentage }}%</span>
            </div>
          </div>

          <div>
            <div class="text-2xl font-bold text-slate-900">
              {{ onTimePercentage }}%
            </div>
            <div class="text-xs text-slate-600 mt-1">
              On-time + Ahead Tasks
            </div>
            <!-- Math Formula display requested in prompt -->
            <div class="text-[10px] font-mono text-slate-600 mt-2 bg-slate-100 p-1.5 rounded border border-slate-200 leading-relaxed">
              &eta; = ((OnTime + Ahead) / Total) &times; 100
            </div>
          </div>
        </div>
      </div>

      <!-- Card 2: Global Task Distribution -->
      <div class="relative overflow-hidden bg-white/90 backdrop-blur-md border border-slate-200 rounded-2xl p-6 shadow-xl transition-all duration-300 hover:shadow-indigo-500/10 hover:border-slate-300 group">
        <div class="absolute -right-10 -top-10 w-32 h-32 bg-indigo-500/10 rounded-full blur-3xl group-hover:bg-indigo-500/20 transition-all duration-500"></div>
        
        <div class="flex items-center justify-between mb-4">
          <h3 class="text-sm font-semibold text-slate-600 uppercase tracking-wider">Total Tasks Completed</h3>
          <div class="p-2 rounded-lg bg-indigo-500/10 text-indigo-400">
            <i class="pi pi-check-circle text-lg"></i>
          </div>
        </div>

        <div class="flex items-baseline gap-2">
          <span class="text-4xl font-extrabold text-slate-900">{{ taskStats.total }}</span>
          <span class="text-xs text-slate-600">total tasks across members</span>
        </div>

        <div class="mt-4 grid grid-cols-3 gap-2 text-center text-xs">
          <div class="bg-emerald-500/10 p-2 rounded-lg border border-emerald-500/20">
            <div class="text-emerald-600 font-bold text-sm">{{ taskStats.ahead }}</div>
            <div class="text-[10px] text-slate-600">Ahead</div>
          </div>
          <div class="bg-blue-500/10 p-2 rounded-lg border border-blue-500/20">
            <div class="text-blue-600 font-bold text-sm">{{ taskStats.onTime }}</div>
            <div class="text-[10px] text-slate-600">On Time</div>
          </div>
          <div class="bg-rose-500/10 p-2 rounded-lg border border-rose-500/20">
            <div class="text-rose-600 font-bold text-sm">{{ taskStats.delayed }}</div>
            <div class="text-[10px] text-slate-600">Delayed</div>
          </div>
        </div>
      </div>

      <!-- Card 3: Team Strength & Scope -->
      <div class="relative overflow-hidden bg-white/90 backdrop-blur-md border border-slate-200 rounded-2xl p-6 shadow-xl transition-all duration-300 hover:shadow-purple-500/10 hover:border-slate-300 group">
        <div class="absolute -right-10 -top-10 w-32 h-32 bg-purple-500/10 rounded-full blur-3xl group-hover:bg-purple-500/20 transition-all duration-500"></div>
        
        <div class="flex items-center justify-between mb-4">
          <h3 class="text-sm font-semibold text-slate-600 uppercase tracking-wider">Operational Scope</h3>
          <div class="p-2 rounded-lg bg-purple-500/10 text-purple-400">
            <i class="pi pi-users text-lg"></i>
          </div>
        </div>

        <div class="grid grid-cols-2 gap-4 h-full">
          <div class="flex flex-col justify-center">
            <span class="text-3xl font-extrabold text-slate-900">{{ members.length }}</span>
            <span class="text-xs text-slate-600 mt-1">Active Members</span>
          </div>
          <div class="flex flex-col justify-center border-l border-slate-200 pl-4">
            <span class="text-3xl font-extrabold text-slate-900">{{ totalUniqueProjects }}</span>
            <span class="text-xs text-slate-600 mt-1">Unique Projects</span>
          </div>
        </div>
      </div>

    </div>

    <!-- Global Project Summary Widget -->
    <div class="bg-white/90 backdrop-blur-md border border-slate-200 rounded-2xl p-6 shadow-xl">
      <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-6">
        <div>
          <h3 class="text-lg font-bold text-slate-900">Global Project Status Registry</h3>
          <p class="text-xs text-slate-600">Aggregated status breakdown for all assigned projects in the company</p>
        </div>
        <div class="flex items-center gap-2 bg-slate-100 px-3 py-1.5 rounded-lg border border-slate-200 text-xs">
          <span class="w-2.5 h-2.5 rounded-full bg-indigo-500 animate-pulse"></span>
          <span class="text-slate-700 font-medium">Active Tracked Allocations: {{ projectStats.totalAllocations }}</span>
        </div>
      </div>

      <!-- Status Progress Bar Widget -->
      <div class="space-y-4">
        <!-- Visual Multi-segment bar -->
        <div class="h-4 w-full bg-slate-100 rounded-full overflow-hidden flex border border-slate-200">
          <div
            v-for="status in statusList"
            :key="status.name"
            :style="{ width: `${projectStats.percentages[status.name] || 0}%` }"
            :class="status.barColor"
            class="h-full transition-all duration-500 relative group cursor-pointer"
            :title="`${status.name}: ${projectStats.counts[status.name] || 0} (${projectStats.percentages[status.name] || 0}%)`"
          >
          </div>
        </div>

        <!-- Legend and details Grid -->
        <div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-4 pt-2">
          <div 
            v-for="status in statusList" 
            :key="status.name"
            class="bg-slate-50 border border-slate-200 rounded-xl p-3 flex flex-col justify-between hover:border-slate-300 transition-colors"
          >
            <div class="flex items-center gap-2">
              <span class="w-2.5 h-2.5 rounded-full" :class="status.dotColor"></span>
              <span class="text-xs font-medium text-slate-700 truncate">{{ status.name }}</span>
            </div>
            <div class="mt-2 flex items-baseline justify-between">
              <span class="text-lg font-bold text-slate-900">{{ projectStats.counts[status.name] || 0 }}</span>
              <span class="text-[10px] text-slate-600 font-medium">{{ projectStats.percentages[status.name] || 0 }}%</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
  members: {
    type: Array,
    required: true,
  }
});

// Configure custom badges and colors for each allowed project status
const statusList = [
  { name: 'Ahead of schedule', dotColor: 'bg-emerald-500', barColor: 'bg-emerald-500', bgClass: 'bg-emerald-950/40 text-emerald-400 border-emerald-500/30' },
  { name: 'On Time', dotColor: 'bg-blue-500', barColor: 'bg-blue-500', bgClass: 'bg-blue-950/40 text-blue-400 border-blue-500/30' },
  { name: 'Doing', dotColor: 'bg-amber-500', barColor: 'bg-amber-500', bgClass: 'bg-amber-950/40 text-amber-400 border-amber-500/30' },
  { name: 'Not yet start', dotColor: 'bg-slate-500', barColor: 'bg-slate-500', bgClass: 'bg-slate-100 text-slate-700 border-slate-200' },
  { name: 'No plan', dotColor: 'bg-purple-500', barColor: 'bg-purple-500', bgClass: 'bg-purple-950/40 text-purple-400 border-purple-500/30' },
  { name: 'Delay', dotColor: 'bg-rose-500', barColor: 'bg-rose-500', bgClass: 'bg-rose-950/40 text-rose-400 border-rose-500/30' }
];

// 1. Task Statistics Aggregator
const taskStats = computed(() => {
  let total = 0;
  let ahead = 0;
  let onTime = 0;
  let delayed = 0;

  props.members.forEach(member => {
    // Standard task counts per member
    ahead += member.aheadOfSchedule || 0;
    onTime += member.onTime || 0;
    delayed += member.delayed || 0;
  });

  total = ahead + onTime + delayed;

  return { total, ahead, onTime, delayed };
});

// 2. Calculate Overall On-Time Percentage using requested formula
const onTimePercentage = computed(() => {
  const stats = taskStats.value;
  if (stats.total === 0) return 0;
  const percentage = ((stats.onTime + stats.ahead) / stats.total) * 100;
  return Math.round(percentage);
});

// 3. Unique project name calculator
const totalUniqueProjects = computed(() => {
  const projects = new Set();
  props.members.forEach(member => {
    if (member.projects) {
      member.projects.forEach(p => {
        if (p.projectName) {
          projects.add(p.projectName);
        }
      });
    }
  });
  return projects.size;
});

// 4. Project status aggregator for widget
const projectStats = computed(() => {
  const counts = {};
  statusList.forEach(s => {
    counts[s.name] = 0;
  });

  let totalAllocations = 0;
  props.members.forEach(member => {
    if (member.projects) {
      member.projects.forEach(p => {
        if (counts[p.projectStatus] !== undefined) {
          counts[p.projectStatus]++;
          totalAllocations++;
        }
      });
    }
  });

  // Percentages per status
  const percentages = {};
  statusList.forEach(s => {
    percentages[s.name] = totalAllocations > 0 
      ? Math.round((counts[s.name] / totalAllocations) * 100) 
      : 0;
  });

  return {
    counts,
    percentages,
    totalAllocations
  };
});
</script>

<style scoped>
/* Minor animation smooth transition settings */
.transition-all {
  transition-property: all;
  transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
  transition-duration: 300ms;
}
</style>
