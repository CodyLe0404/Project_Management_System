<template>
  <div class="relative z-10 space-y-8">
    <!-- Missing Data Table -->
    <section class="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl shadow-sm overflow-hidden">
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
              <td :colspan="missingDataColumns.length" class="px-6 py-10 text-center text-sm text-slate-500 dark:text-slate-400">No matching items found.</td>
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

    <!-- Project Common Data Table -->
    <section class="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl shadow-sm overflow-hidden">
      <div class="p-6 border-b border-slate-100 dark:border-slate-800">
        <div class="flex flex-col lg:flex-row lg:items-center justify-between gap-4">
          <div>
            <h2 class="font-bold text-slate-800 dark:text-slate-200">All Over Due Date Data </h2>
            <p class="text-xs text-slate-500 dark:text-slate-400 mt-1">Project task schedule, ownership, progress, and cost details.</p>
          </div>
          <label class="relative block w-full lg:w-80">
            <span class="sr-only">Search project common data</span>
            <i class="pi pi-search absolute left-3 top-1/2 -translate-y-1/2 text-slate-400"></i>
            <input
              v-model="projectCommonSearch"
              type="search"
              placeholder="Search projects or tasks..."
              class="w-full rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-950 py-2.5 pl-9 pr-3 text-sm outline-none transition focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/20"
            />
          </label>
        </div>
      </div>

      <div class="overflow-x-auto">
        <table class="w-full min-w-[1900px] text-left text-sm">
          <thead class="bg-slate-50 dark:bg-slate-950/70 text-xs uppercase tracking-wider text-slate-500 dark:text-slate-400">
            <tr>
              <th v-for="column in projectCommonColumns" :key="column.key" scope="col" class="px-6 py-4 font-semibold whitespace-nowrap">
                <button class="inline-flex items-center gap-2 hover:text-indigo-600 dark:hover:text-indigo-400" @click="sortProjectCommonData(column.key)">
                  {{ column.label }}
                  <i :class="projectCommonSortKey === column.key ? (projectCommonSortDirection === 'asc' ? 'pi pi-sort-amount-up-alt' : 'pi pi-sort-amount-down') : 'pi pi-sort-alt'" aria-hidden="true"></i>
                </button>
              </th>
            </tr>
          </thead>
          <tbody class="divide-y divide-slate-100 dark:divide-slate-800">
            <tr v-for="(item, index) in paginatedProjectCommonData" :key="`${item.project_id}-${item.task_no}-${index}`" class="transition-colors odd:bg-white even:bg-slate-50/70 hover:bg-indigo-50/70 dark:odd:bg-slate-900 dark:even:bg-slate-800/40 dark:hover:bg-indigo-950/40">
              <td v-for="column in projectCommonColumns" :key="column.key" class="px-6 py-4 text-slate-600 dark:text-slate-300 whitespace-nowrap" :class="column.key === 'budget' || column.key === 'actual_cost' ? 'text-right tabular-nums' : ''">
                <span v-if="column.key === 'project_name' || column.key === 'sub_task'" class="block max-w-xs truncate" :title="displayProjectCommonValue(item, column)">
                  {{ displayProjectCommonValue(item, column) }}
                </span>
                <span v-else-if="column.key === 'status'" class="inline-flex rounded-full border border-slate-200 dark:border-slate-700 px-2.5 py-0.5 text-[11px] font-semibold">
                  {{ displayProjectCommonValue(item, column) }}
                </span>
                <span v-else>{{ displayProjectCommonValue(item, column) }}</span>
              </td>
            </tr>
            <tr v-if="!paginatedProjectCommonData.length">
              <td :colspan="projectCommonColumns.length" class="px-6 py-10 text-center text-sm text-slate-500 dark:text-slate-400">No matching project data found.</td>
            </tr>
          </tbody>
        </table>
      </div>

      <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-t border-slate-100 dark:border-slate-800 px-6 py-4 text-xs text-slate-500 dark:text-slate-400">
        <span>Showing {{ projectCommonRangeStart }}-{{ projectCommonRangeEnd }} of {{ filteredProjectCommonData.length }}</span>
        <div class="flex items-center gap-2">
          <button class="inline-flex items-center gap-2 rounded-lg border border-slate-200 dark:border-slate-700 px-3 py-2 font-semibold transition hover:border-indigo-400 hover:text-indigo-600 disabled:cursor-not-allowed disabled:opacity-40" :disabled="projectCommonPage === 1" @click="projectCommonPage--">
            <i class="pi pi-angle-left"></i> Previous
          </button>
          <span class="min-w-20 text-center font-semibold">Page {{ projectCommonPage }} of {{ projectCommonPageCount }}</span>
          <button class="inline-flex items-center gap-2 rounded-lg border border-slate-200 dark:border-slate-700 px-3 py-2 font-semibold transition hover:border-indigo-400 hover:text-indigo-600 disabled:cursor-not-allowed disabled:opacity-40" :disabled="projectCommonPage === projectCommonPageCount" @click="projectCommonPage++">
            Next <i class="pi pi-angle-right"></i>
          </button>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { computed, ref, watch } from 'vue';

const props = defineProps({
  itemMissingData: {
    type: [Array, Object],
    default: null
  },
  projectCommonData: {
    type: [Array, Object],
    default: null
  }
});

const demoMissingData = Array.from({ length: 14 }, () => ({
  project_id: '1001',
  project_number: 'L252A335',
  project_name: 'HYD_TR 6&7 Station',
  task_no: 101,
  main_task: 'LV'
}));
const missingDataColumns = [
  { key: 'project_number', label: 'Project Number' },
  { key: 'project_name', label: 'Project Name' },
  { key: 'task_no', label: 'Task No' },
  { key: 'main_task', label: 'Main Task' },
  { key: 'sub_task', label: 'Sub Task' },
  { key: 'progress', label: 'Progress' },
  { key: 'status', label: 'Status' },
  { key: 'assignee', label: 'Assignee' }
];
const projectCommonColumns = [
  { key: 'project_id', label: 'Project ID', type: 'text' },
  { key: 'project_number', label: 'Project Number', type: 'text' },
  { key: 'project_name', label: 'Project Name', type: 'text' },
  { key: 'task_no', label: 'Task No', type: 'number' },
  { key: 'main_task', label: 'Main Task', type: 'text' },
  { key: 'sub_task', label: 'Sub Task', type: 'text' },
  { key: 'qty', label: 'Qty', type: 'number' },
  { key: 'assignee', label: 'Assignee', type: 'text' },
  { key: 'progress', label: 'Progress', type: 'progress' },
  { key: 'status', label: 'Status', type: 'text' },
  { key: 'plan_start', label: 'Plan Start', type: 'date' },
  { key: 'plan_end', label: 'Plan End', type: 'date' },
  { key: 'actual_start', label: 'Actual Start', type: 'date' },
  { key: 'actual_end', label: 'Actual End', type: 'date' },
  { key: 'budget', label: 'Budget', type: 'money' },
  { key: 'actual_cost', label: 'Actual Cost', type: 'money' },
  { key: 'remark', label: 'Remark', type: 'text' }
];
const missingDataSearch = ref('');
const missingDataPage = ref(1);
const missingDataPageSize = 10;
const missingDataSortKey = ref('project_id');
const missingDataSortDirection = ref('asc');
const projectCommonSearch = ref('');
const projectCommonPage = ref(1);
const projectCommonPageSize = 10;
const projectCommonSortKey = ref('project_number');
const projectCommonSortDirection = ref('asc');

const missingDataRows = computed(() => {
  const response = props.itemMissingData;
  if (Array.isArray(response)) return response;
  if (Array.isArray(response?.data)) return response.data;
  return demoMissingData;
});

const projectCommonRows = computed(() => {
  const response = props.projectCommonData;
  if (Array.isArray(response)) return response;
  if (Array.isArray(response?.data)) return response.data;
  return [];
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

const filteredProjectCommonData = computed(() => {
  const query = projectCommonSearch.value.trim().toLowerCase();
  const rows = query
    ? projectCommonRows.value.filter((item) => projectCommonColumns.some(({ key }) => String(item[key] ?? '').toLowerCase().includes(query)))
    : [...projectCommonRows.value];
  const sortColumn = projectCommonColumns.find(({ key }) => key === projectCommonSortKey.value);

  return rows.sort((left, right) => {
    const leftValue = left[projectCommonSortKey.value] ?? '';
    const rightValue = right[projectCommonSortKey.value] ?? '';
    const comparison = ['number', 'money', 'progress'].includes(sortColumn?.type)
      ? (Number(leftValue) || 0) - (Number(rightValue) || 0)
      : String(leftValue).localeCompare(String(rightValue), undefined, { numeric: true, sensitivity: 'base' });
    return projectCommonSortDirection.value === 'asc' ? comparison : -comparison;
  });
});

const missingDataPageCount = computed(() => Math.max(1, Math.ceil(filteredMissingData.value.length / missingDataPageSize)));
const paginatedMissingData = computed(() => {
  const start = (missingDataPage.value - 1) * missingDataPageSize;
  return filteredMissingData.value.slice(start, start + missingDataPageSize);
});
const missingDataRangeStart = computed(() => filteredMissingData.value.length ? (missingDataPage.value - 1) * missingDataPageSize + 1 : 0);
const missingDataRangeEnd = computed(() => Math.min(missingDataPage.value * missingDataPageSize, filteredMissingData.value.length));
const projectCommonPageCount = computed(() => Math.max(1, Math.ceil(filteredProjectCommonData.value.length / projectCommonPageSize)));
const paginatedProjectCommonData = computed(() => {
  const start = (projectCommonPage.value - 1) * projectCommonPageSize;
  return filteredProjectCommonData.value.slice(start, start + projectCommonPageSize);
});
const projectCommonRangeStart = computed(() => filteredProjectCommonData.value.length ? (projectCommonPage.value - 1) * projectCommonPageSize + 1 : 0);
const projectCommonRangeEnd = computed(() => Math.min(projectCommonPage.value * projectCommonPageSize, filteredProjectCommonData.value.length));

const sortMissingData = (key) => {
  if (missingDataSortKey.value === key) {
    missingDataSortDirection.value = missingDataSortDirection.value === 'asc' ? 'desc' : 'asc';
  } else {
    missingDataSortKey.value = key;
    missingDataSortDirection.value = 'asc';
  }
};

const sortProjectCommonData = (key) => {
  if (projectCommonSortKey.value === key) {
    projectCommonSortDirection.value = projectCommonSortDirection.value === 'asc' ? 'desc' : 'asc';
  } else {
    projectCommonSortKey.value = key;
    projectCommonSortDirection.value = 'asc';
  }
};

function displayProjectCommonValue(item, column) {
  const value = item[column.key];
  if (value === null || value === undefined || value === '') return '-';
  if (column.type === 'money') {
    const amount = Number(value);
    return Number.isFinite(amount)
      ? new Intl.NumberFormat('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 }).format(amount)
      : value;
  }
  if (column.type === 'number') {
    const number = Number(value);
    return Number.isFinite(number) ? new Intl.NumberFormat('en-US').format(number) : value;
  }
  if (column.type === 'progress') {
    const progress = Number(value);
    return Number.isFinite(progress) ? `${progress}%` : value;
  }
  return value;
}

watch([missingDataSearch, filteredMissingData], () => {
  if (missingDataPage.value > missingDataPageCount.value) missingDataPage.value = missingDataPageCount.value;
  if (missingDataSearch.value) missingDataPage.value = 1;
});

watch([projectCommonSearch, filteredProjectCommonData], () => {
  if (projectCommonPage.value > projectCommonPageCount.value) projectCommonPage.value = projectCommonPageCount.value;
  if (projectCommonSearch.value) projectCommonPage.value = 1;
});
</script>
