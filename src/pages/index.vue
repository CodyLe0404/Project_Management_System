<route>
{
  meta: {
    title: "Dashboard",
    icon: "pi pi-home"
  }
}
</route>

<template>
  <div class="min-h-screen bg-slate-50 dark:bg-slate-950 text-slate-900 dark:text-slate-100 p-4 md:p-8 space-y-8 rounded-3xl border border-slate-200 dark:border-slate-800 shadow-2xl overflow-hidden relative transition-colors duration-300">
    <!-- Visual Gradient Accents -->
    <div class="absolute top-0 left-1/4 w-96 h-96 bg-indigo-500/10 dark:bg-indigo-500/5 rounded-full blur-3xl pointer-events-none"></div>
    <div class="absolute top-10 right-1/4 w-96 h-96 bg-blue-500/10 dark:bg-blue-500/5 rounded-full blur-3xl pointer-events-none"></div>

    <!-- Header Section -->
    <header class="relative flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-slate-200 dark:border-slate-800 pb-6 z-10">
      <div>
        <div class="flex items-center gap-2 text-indigo-600 dark:text-indigo-400 font-semibold text-xs tracking-wider uppercase mb-1">
          <i class="pi pi-home"></i>
          System Overview
        </div>
        <h1 class="text-3xl font-extrabold tracking-tight bg-clip-text text-transparent bg-gradient-to-r from-slate-900 via-indigo-900 to-indigo-600 dark:from-white dark:via-indigo-400 dark:to-blue-400">
          Executive Dashboard
        </h1>
        <p class="text-xs text-slate-500 dark:text-slate-400 mt-1 font-medium">
          Overview of system performance, project pipelines, and task distribution progress.
        </p>
      </div>

      <!-- Interactive Data Source Toggle -->
      <div class="flex flex-col sm:flex-row sm:items-center gap-3">
        <!-- Live Connection status indicator -->
        <div v-if="!isDemoMode" class="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-emerald-50 dark:bg-emerald-950/40 border border-emerald-200 dark:border-emerald-800/50 text-emerald-600 dark:text-emerald-400 text-xs font-semibold">
          <span class="relative flex h-2 w-2">
            <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
            <span class="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
          </span>
          Live Server Connected
        </div>
        <div v-else class="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-amber-50 dark:bg-amber-950/40 border border-amber-200 dark:border-amber-800/50 text-amber-600 dark:text-amber-400 text-xs font-semibold">
          <i class="pi pi-info-circle text-xs"></i>
          Demo Mode Active
        </div>

        <div class="inline-flex rounded-lg p-0.5 bg-slate-200 dark:bg-slate-800 border border-slate-300/30">
          <button 
            @click="setMode(true)" 
            :class="isDemoMode ? 'bg-white dark:bg-slate-900 shadow-sm text-indigo-600 dark:text-indigo-400' : 'text-slate-600 dark:text-slate-400 hover:text-slate-900'"
            class="px-3 py-1.5 rounded-md text-xs font-semibold transition-all duration-200"
          >
            Demo Dataset
          </button>
          <button 
            @click="setMode(false)" 
            :class="!isDemoMode ? 'bg-white dark:bg-slate-900 shadow-sm text-indigo-600 dark:text-indigo-400' : 'text-slate-600 dark:text-slate-400 hover:text-slate-900'"
            class="px-3 py-1.5 rounded-md text-xs font-semibold transition-all duration-200"
          >
            Live Database
          </button>
        </div>
      </div>
    </header>

    <!-- Error/Warning Banner if live fails -->
    <div v-if="connectionError" class="relative z-10 flex items-center justify-between p-4 bg-red-50 dark:bg-red-950/30 border border-red-200 dark:border-red-900/50 rounded-2xl text-red-600 dark:text-red-400 text-xs transition-all duration-300">
      <div class="flex items-center gap-3">
        <div class="p-2 rounded-lg bg-red-100 dark:bg-red-900/50 text-red-600 dark:text-red-400">
          <i class="pi pi-exclamation-triangle text-base"></i>
        </div>
        <div>
          <span class="font-bold">Live database unavailable</span>. Unable to connect to the backend server. Falling back to the local demo dataset.
        </div>
      </div>
      <button @click="connectionError = false" class="text-red-405 hover:text-red-600 px-2">
        <i class="pi pi-times"></i>
      </button>
    </div>

    <!-- Summary KPI Cards -->
    <div class="relative z-10 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
      <!-- Total Projects Card -->
      <div class="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl p-6 shadow-sm hover:shadow-md transition-all duration-300 group overflow-hidden relative">
        <div class="absolute top-0 left-0 w-1.5 h-full bg-blue-500"></div>
        <div class="flex justify-between items-start">
          <div>
            <span class="block text-slate-500 dark:text-slate-400 text-xs font-semibold uppercase tracking-wider mb-2">Total Projects</span>
            <div class="text-3xl font-extrabold text-slate-800 dark:text-white transition-colors group-hover:text-blue-600 dark:group-hover:text-blue-400">
              {{ currentSummary.total_project }}
            </div>
          </div>
          <div class="p-3 rounded-xl bg-blue-50 dark:bg-blue-950/50 text-blue-600 dark:text-blue-400 transition-colors group-hover:bg-blue-500 group-hover:text-white">
            <i class="pi pi-folder text-xl"></i>
          </div>
        </div>
        <p class="text-xs text-slate-400 dark:text-slate-500 mt-4 flex items-center gap-1">
          <i class="pi pi-info-circle"></i>
          Active & planned portfolios
        </p>
      </div>

      <!-- Total Tasks Card -->
      <div class="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl p-6 shadow-sm hover:shadow-md transition-all duration-300 group overflow-hidden relative">
        <div class="absolute top-0 left-0 w-1.5 h-full bg-indigo-500"></div>
        <div class="flex justify-between items-start">
          <div>
            <span class="block text-slate-500 dark:text-slate-400 text-xs font-semibold uppercase tracking-wider mb-2">Total Tasks</span>
            <div class="text-3xl font-extrabold text-slate-800 dark:text-white transition-colors group-hover:text-indigo-600 dark:group-hover:text-indigo-400">
              {{ currentSummary.total_task }}
            </div>
          </div>
          <div class="p-3 rounded-xl bg-indigo-50 dark:bg-indigo-950/50 text-indigo-600 dark:text-indigo-455 transition-colors group-hover:bg-indigo-500 group-hover:text-white">
            <i class="pi pi-list text-xl"></i>
          </div>
        </div>
        <p class="text-xs text-slate-400 dark:text-slate-500 mt-4 flex items-center gap-1">
          <i class="pi pi-chart-line"></i>
          Tasks distribution workload
        </p>
      </div>

      <!-- In Progress Card -->
      <div class="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl p-6 shadow-sm hover:shadow-md transition-all duration-300 group overflow-hidden relative">
        <div class="absolute top-0 left-0 w-1.5 h-full bg-amber-500"></div>
        <div class="flex justify-between items-start">
          <div>
            <span class="block text-slate-500 dark:text-slate-400 text-xs font-semibold uppercase tracking-wider mb-2">In Progress</span>
            <div class="text-3xl font-extrabold text-slate-800 dark:text-white transition-colors group-hover:text-amber-550 dark:group-hover:text-amber-400">
              {{ currentSummary.inprogress }}
            </div>
          </div>
          <div class="p-3 rounded-xl bg-amber-50 dark:bg-amber-950/50 text-amber-550 dark:text-amber-400 transition-colors group-hover:bg-amber-500 group-hover:text-white">
            <i class="pi pi-sync text-xl animate-spin-slow"></i>
          </div>
        </div>
        <p class="text-xs text-slate-400 dark:text-slate-500 mt-4 flex items-center gap-1">
          <i class="pi pi-clock"></i>
          Currently active execution
        </p>
      </div>

      <!-- Task Completion Rate Card -->
      <div class="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl p-6 shadow-sm hover:shadow-md transition-all duration-300 group overflow-hidden relative">
        <div class="absolute top-0 left-0 w-1.5 h-full bg-emerald-500"></div>
        <div class="flex justify-between items-start">
          <div>
            <span class="block text-slate-500 dark:text-slate-400 text-xs font-semibold uppercase tracking-wider mb-2">Completion Rate</span>
            <div class="text-3xl font-extrabold text-slate-800 dark:text-white transition-colors group-hover:text-emerald-600 dark:group-hover:text-emerald-400">
              {{ completionRate }}%
            </div>
          </div>
          <div class="p-3 rounded-xl bg-emerald-50 dark:bg-emerald-950/50 text-emerald-600 dark:text-emerald-400 transition-colors group-hover:bg-emerald-500 group-hover:text-white">
            <i class="pi pi-check-circle text-xl"></i>
          </div>
        </div>
        <!-- Progress Bar -->
        <div class="w-full bg-slate-100 dark:bg-slate-800 rounded-full h-1.5 mt-4 overflow-hidden">
          <div 
            class="bg-emerald-500 h-1.5 rounded-full transition-all duration-500" 
            :style="{ width: completionRate + '%' }"
          ></div>
        </div>
      </div>
    </div>

    <!-- Charts Section -->
    <div class="relative z-10 grid grid-cols-1 lg:grid-cols-12 gap-8">
      <!-- Task Status Distribution (Donut Chart) -->
      <div class="lg:col-span-5 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl p-6 shadow-sm flex flex-col justify-between">
        <div>
          <div class="flex items-center justify-between mb-2">
            <h3 class="font-bold text-slate-800 dark:text-slate-200">Task Status Distribution</h3>
            <span class="text-xs font-semibold text-slate-400 px-2 py-0.5 rounded bg-slate-50 dark:bg-slate-800 border border-slate-200/50 dark:border-slate-800">
              Doughnut
            </span>
          </div>
          <p class="text-xs text-slate-500 dark:text-slate-400 mb-6">Task volume breakdown across completion phases.</p>
        </div>

        <div class="relative h-60 w-full flex items-center justify-center mb-6">
          <canvas id="taskStatusChart"></canvas>
          <!-- Center Stat Overlay -->
          <div class="absolute inset-0 flex flex-col items-center justify-center pointer-events-none">
            <span class="text-2xl font-black text-slate-800 dark:text-white">{{ currentSummary.total_task }}</span>
            <span class="text-[10px] uppercase font-bold text-slate-400 tracking-wider">Total Tasks</span>
          </div>
        </div>

        <!-- Custom Legend Grid -->
        <div class="grid grid-cols-3 gap-3 border-t border-slate-100 dark:border-slate-800 pt-4">
          <div class="flex flex-col items-center text-center">
            <div class="flex items-center gap-1.5 text-slate-500 dark:text-slate-400 text-xs mb-1">
              <span class="w-2.5 h-2.5 rounded-full bg-slate-400 dark:bg-slate-500 inline-block"></span>
              <span>Not Started</span>
            </div>
            <span class="font-bold text-sm text-slate-800 dark:text-slate-200">{{ currentSummary.not_started }}</span>
            <span class="text-[10px] text-slate-400 mt-0.5">({{ getPercentage(currentSummary.not_started) }}%)</span>
          </div>
          <div class="flex flex-col items-center text-center">
            <div class="flex items-center gap-1.5 text-slate-500 dark:text-slate-400 text-xs mb-1">
              <span class="w-2.5 h-2.5 rounded-full bg-blue-500 inline-block"></span>
              <span>In Progress</span>
            </div>
            <span class="font-bold text-sm text-slate-800 dark:text-slate-200">{{ currentSummary.inprogress }}</span>
            <span class="text-[10px] text-slate-400 mt-0.5">({{ getPercentage(currentSummary.inprogress) }}%)</span>
          </div>
          <div class="flex flex-col items-center text-center">
            <div class="flex items-center gap-1.5 text-slate-500 dark:text-slate-400 text-xs mb-1">
              <span class="w-2.5 h-2.5 rounded-full bg-emerald-500 inline-block"></span>
              <span>Completed</span>
            </div>
            <span class="font-bold text-sm text-slate-800 dark:text-slate-200">{{ currentSummary.completed }}</span>
            <span class="text-[10px] text-slate-400 mt-0.5">({{ getPercentage(currentSummary.completed) }}%)</span>
          </div>
        </div>
      </div>

      <!-- Task Completion Ranges (Bar Chart) -->
      <div class="lg:col-span-7 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl p-6 shadow-sm flex flex-col justify-between">
        <div>
          <div class="flex items-center justify-between mb-2">
            <h3 class="font-bold text-slate-800 dark:text-slate-200">Completion Ranges</h3>
            <span class="text-xs font-semibold text-slate-400 px-2 py-0.5 rounded bg-slate-50 dark:bg-slate-800 border border-slate-200/50 dark:border-slate-800">
              Bar Chart
            </span>
          </div>
          <p class="text-xs text-slate-500 dark:text-slate-400 mb-6">Distribution of task progress levels in percentage ranges.</p>
        </div>

        <div class="relative h-64 w-full md:px-4">
          <canvas id="taskRangesChart"></canvas>
        </div>

        <!-- Footnote details -->
        <div class="border-t border-slate-100 dark:border-slate-800 pt-4 flex flex-wrap justify-between items-center gap-2 text-xs text-slate-400 dark:text-slate-500">
          <span class="flex items-center gap-1">
            <i class="pi pi-filter"></i>
            Shows volume of task progress completion ranges
          </span>
          <span class="font-medium text-indigo-500 dark:text-indigo-400">
            Peak Range: {{ peakRangeName }}
          </span>
        </div>
      </div>
    </div>

    <!-- Missing Data Table -->
    <section class="relative z-10 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl shadow-sm overflow-hidden">
      <div class="p-6 border-b border-slate-100 dark:border-slate-800">
        <div class="flex flex-col lg:flex-row lg:items-center justify-between gap-4">
          <div>
            <h2 class="font-bold text-slate-800 dark:text-slate-200">Items Missing Assignee Data</h2>
            <p class="text-xs text-slate-500 dark:text-slate-400 mt-1">Projects and tasks that need additional information.</p>
          </div>
          <label class="relative block w-full lg:w-80">
            <span class="sr-only">Search missing data</span>
            <i class="pi pi-search absolute left-3 top-1/2 -translate-y-1/2 text-slate-400"></i>
            <input
              v-model="missingDataSearch"
              type="search"
              placeholder="Search projects or tasks..."
              class="w-full rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-950 py-2.5 pl-9 pr-3 text-sm outline-none transition focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/20"
            />
          </label>
        </div>
      </div>

      <div class="overflow-x-auto">
        <table class="w-full min-w-[760px] text-left text-sm">
          <thead class="bg-slate-50 dark:bg-slate-950/70 text-xs uppercase tracking-wider text-slate-500 dark:text-slate-400">
            <tr>
              <th v-for="column in missingDataColumns" :key="column.key" scope="col" class="px-6 py-4 font-semibold">
                <button class="inline-flex items-center gap-2 hover:text-indigo-600 dark:hover:text-indigo-400" @click="sortMissingData(column.key)">
                  {{ column.label }}
                  <i :class="missingDataSortKey === column.key ? (missingDataSortDirection === 'asc' ? 'pi pi-sort-amount-up-alt' : 'pi pi-sort-amount-down') : 'pi pi-sort-alt'" aria-hidden="true"></i>
                </button>
              </th>
            </tr>
          </thead>
          <tbody class="divide-y divide-slate-100 dark:divide-slate-800">
            <tr v-for="(item, index) in paginatedMissingData" :key="`${item.project_id}-${item.task_no}-${index}`" class="transition-colors odd:bg-white even:bg-slate-50/70 hover:bg-indigo-50/70 dark:odd:bg-slate-900 dark:even:bg-slate-800/40 dark:hover:bg-indigo-950/40">
              <!-- <td class="px-6 py-4 font-medium text-slate-700 dark:text-slate-200">{{ item.project_id || '-' }}</td> -->
              <td class="px-6 py-4 text-slate-600 dark:text-slate-300">{{ item.project_number || '-' }}</td>
              <td class="px-6 py-4 text-slate-600 dark:text-slate-300">{{ item.project_name || '-' }}</td>
              <td class="px-6 py-4 text-slate-600 dark:text-slate-300">{{ item.task_no ?? '-' }}</td>
              <td class="px-6 py-4 text-slate-600 dark:text-slate-300">{{ item.main_task || '-' }}</td>
              <td class="px-6 py-4 text-slate-600 dark:text-slate-300">{{ item.sub_task || '-' }}</td>
              <td class="px-6 py-4 text-slate-600 dark:text-slate-300">{{ item.progress || '0' }}</td>
              <td class="px-6 py-4 text-slate-600 dark:text-slate-300">{{ item.status || '-' }}</td>
              <td class="px-6 py-4 text-slate-600 dark:text-slate-300">{{ item.assignee || '-' }}</td>
            </tr>
            <tr v-if="!paginatedMissingData.length">
              <td colspan="5" class="px-6 py-10 text-center text-sm text-slate-500 dark:text-slate-400">No matching items found.</td>
            </tr>
          </tbody>
        </table>
      </div>

      <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-t border-slate-100 dark:border-slate-800 px-6 py-4 text-xs text-slate-500 dark:text-slate-400">
        <span>Showing {{ missingDataRangeStart }}-{{ missingDataRangeEnd }} of {{ filteredMissingData.length }}</span>
        <div class="flex items-center gap-2">
          <button class="inline-flex items-center gap-2 rounded-lg border border-slate-200 dark:border-slate-700 px-3 py-2 font-semibold transition hover:border-indigo-400 hover:text-indigo-600 disabled:cursor-not-allowed disabled:opacity-40" :disabled="missingDataPage === 1" @click="missingDataPage--">
            <i class="pi pi-angle-left"></i> Previous
          </button>
          <span class="min-w-20 text-center font-semibold">Page {{ missingDataPage }} of {{ missingDataPageCount }}</span>
          <button class="inline-flex items-center gap-2 rounded-lg border border-slate-200 dark:border-slate-700 px-3 py-2 font-semibold transition hover:border-indigo-400 hover:text-indigo-600 disabled:cursor-not-allowed disabled:opacity-40" :disabled="missingDataPage === missingDataPageCount" @click="missingDataPage++">
            Next <i class="pi pi-angle-right"></i>
          </button>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount, watch, nextTick } from 'vue';
import { Chart, registerables } from 'chart.js';
import { getDashboardSummary, getItemMissingData } from '../services/projectService';
import { useAuthStore } from '../stores/auth';

// Register Chart.js components
Chart.register(...registerables);

const authStore = useAuthStore();

const isDemoMode = ref(false);
const loading = ref(false);
const connectionError = ref(false);

// Core Mock Data from User Request
const mockSummary = {
  total_project: 134,
  total_task: 337,
  not_started: 78,
  inprogress: 113,
  completed: 146,
  per_1_25: 17,
  per_26_50: 32,
  per_51_75: 35,
  per_76_99: 29,
  per_100: 100 // completed is 146 in prompt text, but in JSON per_100 is 100
};

// Database summary reactive storage
const apiSummary = ref(null);

const itemMissingDataApi = ref(null);

const demoMissingData = Array.from({ length: 14 }, () => ({
  project_id: '1001',
  project_number: 'L252A335',
  project_name: 'HYD_TR 6&7 Station',
  task_no: 101,
  main_task: 'LV'
}));
const missingDataColumns = [
  // { key: 'project_id', label: 'Project ID' },
  { key: 'project_number', label: 'Project Number' },
  { key: 'project_name', label: 'Project Name' },
  { key: 'task_no', label: 'Task No' },
  { key: 'main_task', label: 'Main Task' },
  { key: 'sub_task', label: 'Sub Task' },
  { key: 'progress', label: 'Progress' },
  { key: 'status', label: 'Status' },
  { key: 'assignee', label: 'Assignee' }
];
const missingDataSearch = ref('');
const missingDataPage = ref(1);
const missingDataPageSize = 10;
const missingDataSortKey = ref('project_id');
const missingDataSortDirection = ref('asc');

const missingDataRows = computed(() => {
  const response = itemMissingDataApi.value;
  if (Array.isArray(response)) return response;
  if (Array.isArray(response?.data)) return response.data;
  return demoMissingData;
});

const filteredMissingData = computed(() => {
  const query = missingDataSearch.value.trim().toLowerCase();
  const rows = query
    ? missingDataRows.value.filter((item) => missingDataColumns.some(({ key }) => String(item[key] ?? '').toLowerCase().includes(query)))
    : [...missingDataRows.value];

  return rows.sort((left, right) => {
    const leftValue = left[missingDataSortKey.value] ?? '';
    const rightValue = right[missingDataSortKey.value] ?? '';
    const comparison = typeof leftValue === 'number' && typeof rightValue === 'number'
      ? leftValue - rightValue
      : String(leftValue).localeCompare(String(rightValue), undefined, { numeric: true, sensitivity: 'base' });
    return missingDataSortDirection.value === 'asc' ? comparison : -comparison;
  });
});

const missingDataPageCount = computed(() => Math.max(1, Math.ceil(filteredMissingData.value.length / missingDataPageSize)));
const paginatedMissingData = computed(() => {
  const start = (missingDataPage.value - 1) * missingDataPageSize;
  return filteredMissingData.value.slice(start, start + missingDataPageSize);
});
const missingDataRangeStart = computed(() => filteredMissingData.value.length ? (missingDataPage.value - 1) * missingDataPageSize + 1 : 0);
const missingDataRangeEnd = computed(() => Math.min(missingDataPage.value * missingDataPageSize, filteredMissingData.value.length));

const sortMissingData = (key) => {
  if (missingDataSortKey.value === key) {
    missingDataSortDirection.value = missingDataSortDirection.value === 'asc' ? 'desc' : 'asc';
  } else {
    missingDataSortKey.value = key;
    missingDataSortDirection.value = 'asc';
  }
};

watch([missingDataSearch, filteredMissingData], () => {
  if (missingDataPage.value > missingDataPageCount.value) missingDataPage.value = missingDataPageCount.value;
  if (missingDataSearch.value) missingDataPage.value = 1;
});

// Active summary computed based on toggle mode
const currentSummary = computed(() => {
  if (isDemoMode.value || !apiSummary.value) {
    return mockSummary;
  }
  
  // Adapt apiSummary values ensuring fallbacks
  const totalTask = apiSummary.value.total_task ?? 0;
  const completed = apiSummary.value.completed ?? 0;
  
  return {
    total_project: apiSummary.value.total_project ?? 0,
    total_task: totalTask,
    not_started: apiSummary.value.not_started ?? 0,
    inprogress: apiSummary.value.inprogress ?? 0,
    completed: completed,
    per_1_25: apiSummary.value.per_1_25 ?? 0,
    per_26_50: apiSummary.value.per_26_50 ?? 0,
    per_51_75: apiSummary.value.per_51_75 ?? 0,
    per_76_99: apiSummary.value.per_76_99 ?? 0,
    per_100: apiSummary.value.per_100 ?? completed // Use per_100 if returned, else fallback to completed
  };
});

// Calculate overall completion rate
const completionRate = computed(() => {
  const total = currentSummary.value.total_task;
  if (!total) return 0;
  return ((currentSummary.value.completed / total) * 100).toFixed(1);
});

// Peak range calculation for visual display
const peakRangeName = computed(() => {
  const s = currentSummary.value;
  const ranges = [
    { name: '1% - 25%', val: s.per_1_25 },
    { name: '26% - 50%', val: s.per_26_50 },
    { name: '51% - 75%', val: s.per_51_75 },
    { name: '76% - 99%', val: s.per_76_99 },
    { name: '100%', val: s.per_100 }
  ];
  let max = ranges[0];
  for (let i = 1; i < ranges.length; i++) {
    if (ranges[i].val > max.val) {
      max = ranges[i];
    }
  }
  return `${max.name} (${max.val} tasks)`;
});

// Helper for percentages
const getPercentage = (value) => {
  const total = currentSummary.value.total_task;
  if (!total) return 0;
  return ((value / total) * 100).toFixed(1);
};

// Chart instances
let statusChartInstance = null;
let rangesChartInstance = null;

// Doughnut chart options and data generator
const getStatusChartConfig = () => {
  const s = currentSummary.value;
  
  // Match requested color palettes:
  // Not Started: Gray/Red (Slate gray or coral red #f43f5e / #94a3b8)
  // In Progress: Blue/Yellow (#3b82f6 / #f59e0b)
  // Completed: Green (#10b981)
  const isDark = document.documentElement.classList.contains('dark');
  
  return {
    type: 'doughnut',
    data: {
      labels: ['Not Started', 'In Progress', 'Completed'],
      datasets: [{
        data: [s.not_started, s.inprogress, s.completed],
        backgroundColor: [
          '#94a3b8', // Gray for Not Started (Gray/Red requested: Slate Gray selected)
          '#3b82f6', // Vibrant Blue for In Progress
          '#10b981'  // Emerald Green for Completed
        ],
        borderWidth: isDark ? 2 : 0,
        borderColor: isDark ? '#0f172a' : '#ffffff',
        hoverOffset: 8
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      cutout: '72%',
      plugins: {
        legend: {
          display: false // Using custom legends below the chart
        },
        tooltip: {
          backgroundColor: isDark ? '#0f172a' : '#1e293b',
          titleColor: '#ffffff',
          bodyColor: '#ffffff',
          padding: 10,
          cornerRadius: 10,
          displayColors: true,
          callbacks: {
            label: function(context) {
              const val = context.raw;
              const total = context.dataset.data.reduce((a, b) => a + b, 0);
              const pct = ((val / total) * 100).toFixed(1);
              return ` ${context.label}: ${val} (${pct}%)`;
            }
          }
        }
      }
    }
  };
};

// Bar chart options and data generator
const getRangesChartConfig = () => {
  const s = currentSummary.value;
  const isDark = document.documentElement.classList.contains('dark');
  
  return {
    type: 'bar',
    data: {
      labels: ['0%', '1% - 25%', '26% - 50%', '51% - 75%', '76% - 99%', '100%'],
      datasets: [{
        label: 'Task Count',
        data: [s.not_started, s.per_1_25, s.per_26_50, s.per_51_75, s.per_76_99, s.per_100],
        backgroundColor: isDark ? 'rgba(99, 102, 241, 0.85)' : 'rgba(79, 70, 229, 0.9)', // Indigo theme bar
        hoverBackgroundColor: isDark ? '#818cf8' : '#4338ca',
        borderRadius: 8,
        barThickness: 32,
        maxBarThickness: 48
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          display: false
        },
        tooltip: {
          backgroundColor: isDark ? '#0f172a' : '#1e293b',
          titleColor: '#ffffff',
          bodyColor: '#ffffff',
          padding: 10,
          cornerRadius: 10
        }
      },
      scales: {
        x: {
          grid: {
            display: false
          },
          ticks: {
            color: isDark ? '#94a3b8' : '#64748b',
            font: {
              family: 'Inter, sans-serif',
              size: 11,
              weight: '500'
            }
          }
        },
        y: {
          beginAtZero: true,
          grid: {
            color: isDark ? 'rgba(51, 65, 85, 0.4)' : 'rgba(226, 232, 240, 0.6)'
          },
          ticks: {
            precision: 0,
            color: isDark ? '#94a3b8' : '#64748b',
            font: {
              family: 'Inter, sans-serif',
              size: 11
            }
          }
        }
      }
    }
  };
};

// Initialize Charts
const initCharts = () => {
  const ctxStatus = document.getElementById('taskStatusChart');
  const ctxRanges = document.getElementById('taskRangesChart');
  
  if (statusChartInstance) statusChartInstance.destroy();
  if (rangesChartInstance) rangesChartInstance.destroy();
  
  if (ctxStatus) {
    statusChartInstance = new Chart(ctxStatus, getStatusChartConfig());
  }
  if (ctxRanges) {
    rangesChartInstance = new Chart(ctxRanges, getRangesChartConfig());
  }
};

// Load live data from FastAPI Backend
const fetchLiveSummary = async () => {
  loading.value = true;
  connectionError.value = false;
  try {
    const data = await getDashboardSummary(authStore.user.userId);
    const itemMissingData = await getItemMissingData(authStore.user.userId);
    itemMissingDataApi.value = itemMissingData;

    if (data && typeof data === 'object' && 'total_project' in data) {
      apiSummary.value = data;
    } else {
      throw new Error("Invalid response format");
    }
  } catch (error) {
    console.error("Dashboard Service Error:", error);
    connectionError.value = true;
    isDemoMode.value = true; // Rollback to demo dataset
  } finally {
    loading.value = false;
  }
};

// Toggle data mode
const setMode = async (demo) => {
  if (demo) {
    isDemoMode.value = true;
    connectionError.value = false;
  } else {
    isDemoMode.value = false;
    await fetchLiveSummary();
  }
};

// Watch layout mode or data mutations to rebuild charts
watch(currentSummary, () => {
  nextTick(() => {
    initCharts();
  });
}, { deep: true });

onMounted(async () => {
  await fetchLiveSummary();

  nextTick(() => {
    setTimeout(() => {
      initCharts();
    }, 150);
  });
});

onBeforeUnmount(() => {
  if (statusChartInstance) statusChartInstance.destroy();
  if (rangesChartInstance) rangesChartInstance.destroy();
});
</script>

<style scoped>
.animate-spin-slow {
  animation: spin 8s linear infinite;
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}
</style>
