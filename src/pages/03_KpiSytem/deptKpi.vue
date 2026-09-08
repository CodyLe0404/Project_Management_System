<route>
{
  meta: {
    title: "KPI Phòng Ban",
    icon: "pi pi-users",
    permission: ["DS_PMS_DK"],
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
          <i class="pi pi-chart-bar"></i>
          Departmental Analytics
        </div>
        <h1 class="text-3xl font-extrabold tracking-tight bg-clip-text text-transparent bg-gradient-to-r from-slate-900 via-indigo-900 to-indigo-600 dark:from-white dark:via-indigo-400 dark:to-blue-400">
          Department KPI Dashboard
        </h1>
        <p class="text-xs text-slate-600 dark:text-slate-400 mt-1">
          Real-time task distribution, project execution percentages, and milestone analytics for department teams.
        </p>
      </div>

      <!-- Quick Summary Status -->
      <div class="flex flex-wrap items-center gap-2 text-xs">
        <span class="px-3 py-1.5 rounded-lg bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 text-slate-700 dark:text-slate-300 font-medium shadow-sm">
          Active User: {{ authStore.user?.displayName || 'Guest User' }}
        </span>
      </div>
    </header>

    <!-- Active Department Description Details (Hidden for Global Overview) -->
    <div v-if="currentDepartment" class="relative z-10 bg-white/50 dark:bg-slate-900/30 backdrop-blur-md border border-slate-200/50 dark:border-slate-800/50 rounded-2xl p-4 flex items-start gap-3 transition-all duration-300">
      <div class="p-3 rounded-xl bg-gradient-to-br text-white shadow-md shadow-indigo-500/10" :class="currentDepartment.colorClass">
        <i :class="getTabIcon(activeTab)" class="text-xl"></i>
      </div>
      <div>
        <h2 class="text-lg font-bold text-slate-800 dark:text-slate-200">{{ activeTab }} Department Overview</h2>
        <p class="text-xs text-slate-600 dark:text-slate-400 mt-0.5">{{ currentDepartment.description }}</p>
      </div>
    </div>

    <!-- KPI Summary Metrics Cards -->
    <DeptKpiCards 
      v-if="isLoaded" 
      :dept-kpi-summary-data="deptKpiSummaryData"
    />

    <!-- Visualizations / Charts Section -->
    <DeptCharts 
      v-if="isLoaded" 
      :dept-kpi-summary-data="deptKpiSummaryData"
    />

    <!-- Project Data Portfolio Registry -->
    <DeptProjectTable 
      v-if="isLoaded" 
      :dept-kpi-detail-data="deptKpiDetailData"
    />
  </div>
</template>

<script setup>
import { ref, onMounted, computed, watch } from 'vue'
import { useAuthStore } from '../../stores/auth';

import { getDeptKpiSummary } from '../../services/projectService'
// import { deptKpiData  } from '../../components/KPI_System/mockData.js';
import DeptTabNavigation from '../../components/KPI_System/DeptTabNavigation.vue';
import DeptKpiCards from '../../components/KPI_System/DeptKpiCards.vue';
import DeptCharts from '../../components/KPI_System/DeptCharts.vue';
import DeptProjectTable from '../../components/KPI_System/DeptProjectTable.vue';

// Authentication Store Injection
const authStore = useAuthStore();

const deptKpiSummaryData = ref({}); 
const deptKpiDetailData = ref({}); 
const isLoaded = ref(false) 

onMounted(async () => {
  try {
    const res = await getDeptKpiSummary(authStore.user.userId);
    // const res = await deptKpiData
    deptKpiSummaryData.value = res.deptKpiSummary
    deptKpiDetailData.value = res.deptKpiDetail
    // console.log("deptKpiSummaryData", deptKpiSummaryData)
    isLoaded.value = true 
  } catch (error) {
    console.error("Lỗi fetch data:", error)
  }
})

</script>

<style scoped>
h1 {
  font-size: 1.875rem !important;
  line-height: 2.25rem !important;
}
</style>
