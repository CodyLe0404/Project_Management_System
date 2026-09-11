<route>
{
  meta: {
    title: "List",
    icon: "pi pi-list",
    permission: ["DS_PMS_DK", "admin"],
  }
}
</route>

<template>
  <div class="min-h-screen space-y-6 pb-12">
    <!-- Header Section -->
    <header class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-200 dark:border-slate-800 pb-4">
      <div>
        <h1 class="text-2xl lg:text-3xl font-extrabold tracking-tight bg-clip-text text-transparent bg-gradient-to-r from-slate-900 via-indigo-900 to-indigo-600 dark:from-white dark:via-indigo-400 dark:to-blue-400">
          Failure Cost List
        </h1>
        <p class="text-xs text-slate-500 dark:text-slate-400 mt-1">
          Search, audit, and manage design error records and cost recovery workflows
        </p>
      </div>

      <!-- Action Buttons -->
      <div class="flex items-center gap-2 flex-wrap">
        <Button
          icon="pi pi-chart-bar"
          label="View Dashboard"
          severity="secondary"
          size="small"
          outlined
          @click="router.push('/02_Fcost/fcostDashboard')"
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

    <!-- Top Filter Area -->
    <FailureCostFilter
      title="Search & Filter Records"
      apply-label="Search Records"
      :show-keyword="true"
      :show-checker="true"
      :show-collapse-toggle="true"
      :master-data="store.masterData"
      :initial-filter="store.filter"
      @apply="handleApplyFilter"
      @reset="handleResetFilter"
    />

    <!-- Main Operational Data Table -->
    <FailureCostTable
      title="Failure Cost Registry"
      :records="store.records"
      :total-records="store.totalRecords"
      :current-page="store.pagination.page"
      :page-size="store.pagination.pageSize"
      :total-pages="store.pagination.totalPages"
      :loading="store.loading"
      @update:current-page="handlePageChange"
      @update:page-size="handlePageSizeChange"
      @row-click="handleRowClick"
      @view-detail="handleViewDetail"
      @edit-record="handleEditRecord"
    >
      <template #actions>
        <Button
          icon="pi pi-refresh"
          text
          rounded
          size="small"
          title="Refresh List"
          :loading="store.loading"
          class="!w-7 !h-7"
          @click="store.fetchRecords()"
        />
      </template>
    </FailureCostTable>

    <!-- Row Detail Drawer -->
    <FailureCostDetailDrawer
      v-model:visible="drawerVisible"
      :record="selectedRecord"
      @edit="handleEditFromDrawer"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { Button } from 'primevue';
import { useToast } from 'primevue/usetoast';

import { useFailureCostStore } from '../../stores/failureCostStore.js';
import FailureCostFilter from '../../components/FailureCost/FailureCostFilter.vue';
import FailureCostTable from '../../components/FailureCost/FailureCostTable.vue';
import FailureCostDetailDrawer from '../../components/FailureCost/FailureCostDetailDrawer.vue';

const router = useRouter();
const store = useFailureCostStore();
const toast = useToast();

const drawerVisible = ref(false);
const selectedRecord = ref(null);

onMounted(async () => {
  await store.fetchRecords();
});

async function handleApplyFilter(newFilter) {
  store.setFilter(newFilter);
  await store.fetchRecords();
  toast.add({
    severity: 'info',
    summary: 'Search Applied',
    detail: `Found ${store.totalRecords} matching records`,
    life: 2500
  });
}

async function handleResetFilter() {
  store.resetFilter();
  await store.fetchRecords();
  toast.add({
    severity: 'secondary',
    summary: 'Filters Cleared',
    detail: 'Displaying all records',
    life: 2000
  });
}

async function handlePageChange(page) {
  store.setPage(page);
  await store.fetchRecords();
}

async function handlePageSizeChange(size) {
  store.setPageSize(size);
  await store.fetchRecords();
}

function handleRowClick(record) {
  selectedRecord.value = record;
  drawerVisible.value = true;
}

function handleViewDetail(record) {
  selectedRecord.value = record;
  drawerVisible.value = true;
}

function handleEditRecord(record) {
  router.push({
    path: '/02_Fcost/fcostEntry',
    query: { id: record.id }
  });
}

function handleEditFromDrawer(record) {
  drawerVisible.value = false;
  router.push({
    path: '/02_Fcost/fcostEntry',
    query: { id: record.id }
  });
}
</script>

<style scoped>
h1 {
  font-size: 1.875rem !important;
  line-height: 2.25rem !important;
}
</style>
