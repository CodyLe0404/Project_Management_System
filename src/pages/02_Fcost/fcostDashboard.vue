<route>
{
  meta: {
    title: "Dashboard",
    icon: "pi pi-chart-bar",
    permission: ["DS_PMS_DK", "admin"],
  }
}
</route>

<template>
  <div class="min-h-screen space-y-6 pb-12">
    <!-- Header Section -->
    <header class="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-slate-200 dark:border-slate-800 pb-4">
      <div>
        <h1 class="text-2xl lg:text-3xl font-extrabold tracking-tight bg-clip-text text-transparent bg-gradient-to-r from-slate-900 via-indigo-900 to-indigo-600 dark:from-white dark:via-indigo-400 dark:to-blue-400">
          Failure Cost Dashboard
        </h1>
        <p class="text-xs text-slate-500 dark:text-slate-400 mt-1 flex items-center gap-2">
          <span>Overview of design error losses, 4M root cause patterns, and departmental metrics</span>
        </p>
      </div>

      <!-- Header Action Buttons -->
      <div class="flex items-center gap-2 flex-wrap">
        <Button
          icon="pi pi-refresh"
          label="Reset Mock Data"
          severity="secondary"
          outlined
          size="small"
          title="Reset database to original 40 mock records"
          :loading="store.loading"
          @click="confirmResetMock"
        />
        <Button
          icon="pi pi-list"
          label="View All Records"
          severity="secondary"
          size="small"
          @click="router.push('/02_Fcost/fcostList')"
        />
        <Button
          icon="pi pi-plus"
          label="New Failure Cost"
          size="small"
          class="!bg-indigo-600 hover:!bg-indigo-700 !border-indigo-600"
          @click="router.push('/02_Fcost/fcostEntry')"
        />
      </div>
    </header>

    <!-- Filter Bar Component -->
    <FailureCostFilter
      title="Dashboard Filters"
      apply-label="Filter Analytics"
      :show-keyword="false"
      :show-checker="false"
      :master-data="store.masterData"
      :initial-filter="dashboardFilter"
      @apply="handleApplyFilter"
      @reset="handleResetFilter"
    />

    <!-- KPI Cards Section -->
    <FailureCostKpiCards :kpis="store.dashboardData.kpis" />

    <!-- Visualizations / Charts Section -->
    <FailureCostCharts :charts="store.dashboardData.charts" />

    <!-- Recent Records Section -->
    <div class="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl shadow-sm overflow-hidden flex flex-col">
      <div class="p-4 sm:p-5 border-b border-slate-200 dark:border-slate-800 flex items-center justify-between bg-slate-50/50 dark:bg-slate-900/50">
        <div>
          <h3 class="font-bold text-base text-slate-800 dark:text-slate-200 flex items-center gap-2">
            <i class="pi pi-clock text-indigo-500"></i> Recent Failure Cost Incidents
          </h3>
          <p class="text-xs text-slate-500 dark:text-slate-400 mt-0.5">
            Latest logged design error cases across all projects
          </p>
        </div>

        <Button
          icon="pi pi-arrow-right"
          icon-pos="right"
          label="View All"
          size="small"
          outlined
          severity="secondary"
          @click="router.push('/02_Fcost/fcostList')"
        />
      </div>

      <!-- Recent Records Table -->
      <div class="overflow-x-auto">
        <table class="w-full text-left border-collapse text-xs">
          <thead>
            <tr class="bg-slate-50 dark:bg-slate-900/80 text-slate-500 dark:text-slate-400 font-semibold border-b border-slate-200 dark:border-slate-800">
              <th class="px-4 py-3 whitespace-nowrap">Date</th>
              <th class="px-4 py-3 whitespace-nowrap">Project</th>
              <th class="px-4 py-3 whitespace-nowrap">Team</th>
              <th class="px-4 py-3 whitespace-nowrap">Error Catalog</th>
              <th class="px-4 py-3 text-center whitespace-nowrap">Quantity</th>
              <th class="px-4 py-3 text-right whitespace-nowrap">F-Cost (USD)</th>
              <th class="px-4 py-3 text-center whitespace-nowrap">Status</th>
              <th class="px-4 py-3 text-center w-20 whitespace-nowrap">Detail</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-slate-100 dark:divide-slate-800/80">
            <tr
              v-for="rec in store.dashboardData.recentRecords"
              :key="rec.id"
              class="hover:bg-indigo-50/30 dark:hover:bg-slate-800/50 cursor-pointer transition-colors"
              @click="openDetailDrawer(rec)"
            >
              <td class="px-4 py-3 whitespace-nowrap font-medium text-slate-700 dark:text-slate-300">
                {{ rec.errorDate }}
              </td>
              <td class="px-4 py-3 font-medium text-slate-800 dark:text-slate-200">
                <span class="font-bold text-indigo-600 dark:text-indigo-400">{{ rec.projectNo }}</span>
                <span class="text-slate-400 mx-1">-</span>
                <span class="text-slate-700 dark:text-slate-300">{{ rec.projectName }}</span>
              </td>
              <td class="px-4 py-3 whitespace-nowrap">
                <span
                  class="px-2 py-0.5 rounded-md text-[11px] font-semibold border"
                  :class="getDeptBadgeStyle(rec.departmentName)"
                >
                  {{ rec.departmentName }}
                </span>
              </td>
              <td class="px-4 py-3 whitespace-nowrap text-slate-700 dark:text-slate-300">
                {{ rec.errorCatalogName }}
              </td>
              <td class="px-4 py-3 text-center font-bold text-slate-800 dark:text-slate-200">
                {{ rec.quantity }}
              </td>
              <td class="px-4 py-3 text-right font-extrabold text-slate-900 dark:text-slate-100 tabular-nums">
                {{ formatCurrency(rec.failureCostUSD) }}
              </td>
              <td class="px-4 py-3 text-center whitespace-nowrap">
                <span
                  class="px-2.5 py-0.5 rounded-full text-[11px] font-semibold border flex items-center justify-center gap-1 w-fit mx-auto"
                  :class="getStatusBadgeStyle(rec.statusName)"
                >
                  <span class="w-1.5 h-1.5 rounded-full" :class="getStatusDotColor(rec.statusName)"></span>
                  {{ rec.statusName }}
                </span>
              </td>
              <td class="px-4 py-3 text-center" @click.stop>
                <Button
                  icon="pi pi-eye"
                  text
                  rounded
                  size="small"
                  title="View Detail Drawer"
                  class="!w-7 !h-7"
                  @click="openDetailDrawer(rec)"
                />
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Detail Drawer -->
    <FailureCostDetailDrawer
      v-model:visible="drawerVisible"
      :record="selectedRecord"
      @edit="navigateToEdit"
    />
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { Button } from 'primevue';
import { useToast } from 'primevue/usetoast';
import { useConfirm } from 'primevue/useconfirm';

import { useFailureCostStore } from '../../stores/failureCostStore.js';
import FailureCostKpiCards from '../../components/FailureCost/FailureCostKpiCards.vue';
import FailureCostCharts from '../../components/FailureCost/FailureCostCharts.vue';
import FailureCostFilter from '../../components/FailureCost/FailureCostFilter.vue';
import FailureCostDetailDrawer from '../../components/FailureCost/FailureCostDetailDrawer.vue';

const router = useRouter();
const store = useFailureCostStore();
const toast = useToast();
const confirm = useConfirm();

const drawerVisible = ref(false);
const selectedRecord = ref(null);

const dashboardFilter = reactive({
  fromDate: '',
  toDate: '',
  departmentId: null,
  projectId: null,
  picUserId: null,
  errorCatalogId: null,
  analysis4MId: null,
  statusId: null
});

onMounted(async () => {
  await store.fetchDashboard(dashboardFilter);
});

async function handleApplyFilter(newFilter) {
  Object.assign(dashboardFilter, newFilter);
  await store.fetchDashboard(dashboardFilter);
  toast.add({
    severity: 'info',
    summary: 'Dashboard Updated',
    detail: 'Analytics refreshed with selected filters',
    life: 2500
  });
}

async function handleResetFilter() {
  dashboardFilter.fromDate = '';
  dashboardFilter.toDate = '';
  dashboardFilter.departmentId = null;
  dashboardFilter.projectId = null;
  dashboardFilter.picUserId = null;
  dashboardFilter.errorCatalogId = null;
  dashboardFilter.analysis4MId = null;
  dashboardFilter.statusId = null;
  await store.fetchDashboard(dashboardFilter);
  toast.add({
    severity: 'secondary',
    summary: 'Filters Cleared',
    detail: 'Dashboard reset to default view',
    life: 2000
  });
}

function openDetailDrawer(record) {
  selectedRecord.value = record;
  drawerVisible.value = true;
}

function navigateToEdit(record) {
  drawerVisible.value = false;
  router.push({
    path: '/02_Fcost/fcostEntry',
    query: { id: record.id }
  });
}

function confirmResetMock() {
  confirm.require({
    message: 'Reset all Failure Cost records to default mock dataset? Any newly created or edited records will be restored.',
    header: 'Reset Mock Dataset',
    icon: 'pi pi-exclamation-triangle',
    rejectProps: {
      label: 'Cancel',
      severity: 'secondary',
      outlined: true
    },
    acceptProps: {
      label: 'Reset Data',
      severity: 'danger'
    },
    accept: async () => {
      await store.resetToInitialDataset();
      await store.fetchDashboard(dashboardFilter);
      toast.add({
        severity: 'success',
        summary: 'Mock Data Reset',
        detail: 'Database restored to initial 40 mock records',
        life: 3000
      });
    }
  });
}

function formatCurrency(val) {
  const num = Number(val) || 0;
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
    minimumFractionDigits: 2,
    maximumFractionDigits: 2
  }).format(num);
}

function getDeptBadgeStyle(dept) {
  switch (dept) {
    case 'Electrical Design':
      return 'bg-blue-50 text-blue-700 border-blue-200 dark:bg-blue-950/40 dark:text-blue-300 dark:border-blue-800/60';
    case 'Mechanical Design':
      return 'bg-amber-50 text-amber-700 border-amber-200 dark:bg-amber-950/40 dark:text-amber-300 dark:border-amber-800/60';
    case 'Design Planning':
      return 'bg-purple-50 text-purple-700 border-purple-200 dark:bg-purple-950/40 dark:text-purple-300 dark:border-purple-800/60';
    case 'Engineering':
      return 'bg-emerald-50 text-emerald-700 border-emerald-200 dark:bg-emerald-950/40 dark:text-emerald-300 dark:border-emerald-800/60';
    default:
      return 'bg-slate-50 text-slate-700 border-slate-200 dark:bg-slate-800 dark:text-slate-300 dark:border-slate-700';
  }
}

function getStatusBadgeStyle(st) {
  switch (st) {
    case 'Open':
      return 'bg-amber-50 text-amber-700 border-amber-200 dark:bg-amber-950/40 dark:text-amber-300 dark:border-amber-800/60';
    case 'Monitoring':
      return 'bg-blue-50 text-blue-700 border-blue-200 dark:bg-blue-950/40 dark:text-blue-300 dark:border-blue-800/60';
    case 'Closed':
      return 'bg-emerald-50 text-emerald-700 border-emerald-200 dark:bg-emerald-950/40 dark:text-emerald-300 dark:border-emerald-800/60';
    default:
      return 'bg-slate-100 text-slate-700 border-slate-200 dark:bg-slate-800 dark:text-slate-300 dark:border-slate-700';
  }
}

function getStatusDotColor(st) {
  switch (st) {
    case 'Open':
      return 'bg-amber-500 animate-pulse';
    case 'Monitoring':
      return 'bg-blue-500';
    case 'Closed':
      return 'bg-emerald-500';
    default:
      return 'bg-slate-400';
  }
}
</script>

<style scoped>
h1 {
  font-size: 1.875rem !important;
  line-height: 2.25rem !important;
}
</style>
