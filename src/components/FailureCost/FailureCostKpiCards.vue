<template>
  <!-- KPI Cards Grid -->
  <section class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-4">
    <!-- Card 1: Total Failure Cost -->
    <div class="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl p-5 shadow-sm hover:shadow-md transition-all duration-200 flex flex-col justify-between group">
      <div class="flex items-center justify-between">
        <span class="text-xs font-bold uppercase tracking-wider text-slate-500 dark:text-slate-400">Total Failure Cost</span>
        <div class="w-9 h-9 rounded-xl bg-rose-50 dark:bg-rose-950/50 text-rose-600 dark:text-rose-400 flex items-center justify-center group-hover:scale-110 transition-transform">
          <i class="pi pi-dollar text-sm"></i>
        </div>
      </div>
      <div class="mt-4">
        <div class="text-2xl lg:text-3xl font-extrabold text-slate-900 dark:text-white tracking-tight">
          {{ formatCurrency(kpis.totalFailureCost) }}
        </div>
        <p class="text-xs text-slate-500 dark:text-slate-400 mt-2 flex items-center gap-1 font-medium">
          <i class="pi pi-shield text-slate-400 text-[10px]"></i> Total financial impact
        </p>
      </div>
    </div>

    <!-- Card 2: Total Errors -->
    <div class="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl p-5 shadow-sm hover:shadow-md transition-all duration-200 flex flex-col justify-between group">
      <div class="flex items-center justify-between">
        <span class="text-xs font-bold uppercase tracking-wider text-slate-500 dark:text-slate-400">Total Errors</span>
        <div class="w-9 h-9 rounded-xl bg-indigo-50 dark:bg-indigo-950/50 text-indigo-600 dark:text-indigo-400 flex items-center justify-center group-hover:scale-110 transition-transform">
          <i class="pi pi-exclamation-triangle text-sm"></i>
        </div>
      </div>
      <div class="mt-4">
        <div class="text-2xl lg:text-3xl font-extrabold text-slate-900 dark:text-white tracking-tight">
          {{ kpis.totalErrors }}
        </div>
        <p class="text-xs text-slate-500 dark:text-slate-400 mt-2 flex items-center gap-1 font-medium">
          <span class="w-2 h-2 rounded-full bg-indigo-500"></span> Recorded defect incidents
        </p>
      </div>
    </div>

    <!-- Card 3: Total Error Quantity -->
    <div class="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl p-5 shadow-sm hover:shadow-md transition-all duration-200 flex flex-col justify-between group">
      <div class="flex items-center justify-between">
        <span class="text-xs font-bold uppercase tracking-wider text-slate-500 dark:text-slate-400">Total Error Quantity</span>
        <div class="w-9 h-9 rounded-xl bg-amber-50 dark:bg-amber-950/50 text-amber-600 dark:text-amber-400 flex items-center justify-center group-hover:scale-110 transition-transform">
          <i class="pi pi-box text-sm"></i>
        </div>
      </div>
      <div class="mt-4">
        <div class="text-2xl lg:text-3xl font-extrabold text-slate-900 dark:text-white tracking-tight">
          {{ kpis.totalQuantity }}
        </div>
        <p class="text-xs text-slate-500 dark:text-slate-400 mt-2 flex items-center gap-1 font-medium">
          <span class="w-2 h-2 rounded-full bg-amber-500"></span> Cumulative units affected
        </p>
      </div>
    </div>

    <!-- Card 4: Open Errors -->
    <div class="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl p-5 shadow-sm hover:shadow-md transition-all duration-200 flex flex-col justify-between group">
      <div class="flex items-center justify-between">
        <span class="text-xs font-bold uppercase tracking-wider text-slate-500 dark:text-slate-400">Open Errors</span>
        <div class="w-9 h-9 rounded-xl bg-orange-50 dark:bg-orange-950/50 text-orange-600 dark:text-orange-400 flex items-center justify-center group-hover:scale-110 transition-transform">
          <i class="pi pi-clock text-sm"></i>
        </div>
      </div>
      <div class="mt-4">
        <div class="text-2xl lg:text-3xl font-extrabold text-orange-600 dark:text-orange-400 tracking-tight flex items-baseline gap-2">
          {{ kpis.openErrors }}
          <span v-if="kpis.monitoringErrors" class="text-xs font-medium text-slate-400">
            (+{{ kpis.monitoringErrors }} monitoring)
          </span>
        </div>
        <p class="text-xs text-slate-500 dark:text-slate-400 mt-2 flex items-center gap-1 font-medium">
          <span class="w-2 h-2 rounded-full bg-orange-500 animate-pulse"></span> Requires active resolution
        </p>
      </div>
    </div>

    <!-- Card 5: Average Cost / Error -->
    <div class="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl p-5 shadow-sm hover:shadow-md transition-all duration-200 flex flex-col justify-between group">
      <div class="flex items-center justify-between">
        <span class="text-xs font-bold uppercase tracking-wider text-slate-500 dark:text-slate-400">Avg Cost / Error</span>
        <div class="w-9 h-9 rounded-xl bg-sky-50 dark:bg-sky-950/50 text-sky-600 dark:text-sky-400 flex items-center justify-center group-hover:scale-110 transition-transform">
          <i class="pi pi-chart-line text-sm"></i>
        </div>
      </div>
      <div class="mt-4">
        <div class="text-2xl lg:text-3xl font-extrabold text-slate-900 dark:text-white tracking-tight">
          {{ formatCurrency(kpis.averageCostPerError) }}
        </div>
        <p class="text-xs text-slate-500 dark:text-slate-400 mt-2 flex items-center gap-1 font-medium">
          <i class="pi pi-calculator text-slate-400 text-[10px]"></i> Average financial loss per incident
        </p>
      </div>
    </div>
  </section>
</template>

<script setup>
defineProps({
  kpis: {
    type: Object,
    required: true,
    default: () => ({
      totalFailureCost: 0,
      totalErrors: 0,
      totalQuantity: 0,
      openErrors: 0,
      monitoringErrors: 0,
      closedErrors: 0,
      averageCostPerError: 0
    })
  }
});

function formatCurrency(val) {
  const num = Number(val) || 0;
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
    minimumFractionDigits: 2,
    maximumFractionDigits: 2
  }).format(num);
}
</script>
