<template>
  <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
    <!-- Chart 1: Failure Cost by Month -->
    <div class="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl p-6 shadow-sm flex flex-col justify-between">
      <div class="flex items-center justify-between mb-4">
        <div>
          <h3 class="font-bold text-base text-slate-800 dark:text-slate-200 flex items-center gap-2">
            <i class="pi pi-chart-line text-indigo-500"></i> Failure Cost by Month
          </h3>
          <p class="text-xs text-slate-500 dark:text-slate-400 mt-0.5">Monthly financial impact trend in USD</p>
        </div>
        <span class="text-xs font-semibold text-slate-500 dark:text-slate-400 px-2.5 py-1 rounded-md bg-slate-100 dark:bg-slate-800">
          Monthly Trend
        </span>
      </div>
      <div class="relative h-64 w-full">
        <canvas ref="monthChartCanvas"></canvas>
      </div>
    </div>

    <!-- Chart 2: Failure Cost by Department / Team -->
    <div class="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl p-6 shadow-sm flex flex-col justify-between">
      <div class="flex items-center justify-between mb-4">
        <div>
          <h3 class="font-bold text-base text-slate-800 dark:text-slate-200 flex items-center gap-2">
            <i class="pi pi-sitemap text-blue-500"></i> Failure Cost by Department
          </h3>
          <p class="text-xs text-slate-500 dark:text-slate-400 mt-0.5">Total cost comparison across teams</p>
        </div>
        <span class="text-xs font-semibold text-slate-500 dark:text-slate-400 px-2.5 py-1 rounded-md bg-slate-100 dark:bg-slate-800">
          Department Breakdown
        </span>
      </div>
      <div class="relative h-64 w-full">
        <canvas ref="deptChartCanvas"></canvas>
      </div>
    </div>

    <!-- Chart 3: Failure Cost by Error Catalog -->
    <div class="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl p-6 shadow-sm flex flex-col justify-between">
      <div class="flex items-center justify-between mb-4">
        <div>
          <h3 class="font-bold text-base text-slate-800 dark:text-slate-200 flex items-center gap-2">
            <i class="pi pi-list text-amber-500"></i> Failure Cost by Error Catalog
          </h3>
          <p class="text-xs text-slate-500 dark:text-slate-400 mt-0.5">Key error categories by cumulative cost (USD)</p>
        </div>
        <span class="text-xs font-semibold text-slate-500 dark:text-slate-400 px-2.5 py-1 rounded-md bg-slate-100 dark:bg-slate-800">
          Root Categories
        </span>
      </div>
      <div class="relative h-72 w-full">
        <canvas ref="catalogChartCanvas"></canvas>
      </div>
    </div>

    <!-- Chart 4: Errors by 4M Analysis -->
    <div class="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl p-6 shadow-sm flex flex-col justify-between">
      <div class="flex items-center justify-between mb-4">
        <div>
          <h3 class="font-bold text-base text-slate-800 dark:text-slate-200 flex items-center gap-2">
            <i class="pi pi-chart-pie text-emerald-500"></i> Errors by 4M Analysis
          </h3>
          <p class="text-xs text-slate-500 dark:text-slate-400 mt-0.5">Distribution across Man, Machine, Material, Method</p>
        </div>
        <span class="text-xs font-semibold text-slate-500 dark:text-slate-400 px-2.5 py-1 rounded-md bg-slate-100 dark:bg-slate-800">
          4M Donut
        </span>
      </div>
      <div class="relative h-72 w-full flex items-center justify-center">
        <canvas ref="m4ChartCanvas"></canvas>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, onBeforeUnmount, nextTick } from 'vue';
import { Chart, registerables } from 'chart.js';

Chart.register(...registerables);

const props = defineProps({
  charts: {
    type: Object,
    required: true,
    default: () => ({
      costByMonth: [],
      costByDepartment: [],
      costByErrorCatalog: [],
      errorsBy4M: { counts: {}, costs: {} }
    })
  }
});

const monthChartCanvas = ref(null);
const deptChartCanvas = ref(null);
const catalogChartCanvas = ref(null);
const m4ChartCanvas = ref(null);

let monthChartInstance = null;
let deptChartInstance = null;
let catalogChartInstance = null;
let m4ChartInstance = null;

function destroyCharts() {
  if (monthChartInstance) {
    monthChartInstance.destroy();
    monthChartInstance = null;
  }
  if (deptChartInstance) {
    deptChartInstance.destroy();
    deptChartInstance = null;
  }
  if (catalogChartInstance) {
    catalogChartInstance.destroy();
    catalogChartInstance = null;
  }
  if (m4ChartInstance) {
    m4ChartInstance.destroy();
    m4ChartInstance = null;
  }
}

function initCharts() {
  destroyCharts();

  // 1. Month Chart (Bar with subtle line overlay)
  if (monthChartCanvas.value && props.charts?.costByMonth?.length) {
    const labels = props.charts.costByMonth.map(item => item.month);
    const costs = props.charts.costByMonth.map(item => item.cost);

    monthChartInstance = new Chart(monthChartCanvas.value, {
      type: 'bar',
      data: {
        labels,
        datasets: [
          {
            type: 'bar',
            label: 'Cost (USD)',
            data: costs,
            backgroundColor: 'rgba(99, 102, 241, 0.75)', // Indigo
            hoverBackgroundColor: 'rgba(79, 70, 229, 0.95)',
            borderRadius: 6,
            borderSkipped: false,
            yAxisID: 'y'
          },
          {
            type: 'line',
            label: 'Trend',
            data: costs,
            borderColor: '#f59e0b', // Amber line
            borderWidth: 2,
            pointBackgroundColor: '#f59e0b',
            pointRadius: 3,
            pointHoverRadius: 5,
            fill: false,
            tension: 0.3,
            yAxisID: 'y'
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: 'top',
            align: 'end',
            labels: {
              boxWidth: 12,
              font: { size: 11, family: 'Inter, sans-serif' },
              color: '#64748b'
            }
          },
          tooltip: {
            callbacks: {
              label: function (context) {
                const label = context.dataset.label || '';
                const val = context.parsed.y || 0;
                return `${label}: $${val.toLocaleString()}`;
              }
            }
          }
        },
        scales: {
          x: {
            grid: { display: false },
            ticks: { font: { size: 11 }, color: '#94a3b8' }
          },
          y: {
            beginAtZero: true,
            grid: { color: 'rgba(226, 232, 240, 0.6)' },
            ticks: {
              font: { size: 11 },
              color: '#94a3b8',
              callback: val => `$${val >= 1000 ? (val / 1000) + 'k' : val}`
            }
          }
        }
      }
    });
  }

  // 2. Department Chart
  if (deptChartCanvas.value && props.charts?.costByDepartment?.length) {
    const deptColors = {
      Electrical: '#3b82f6', // Blue
      Mechanical: '#f59e0b', // Amber
      Design: '#8b5cf6',     // Purple
      Engineering: '#10b981' // Emerald
    };

    const labels = props.charts.costByDepartment.map(d => d.department);
    const costs = props.charts.costByDepartment.map(d => d.cost);
    const bgColors = labels.map(name => deptColors[name] || '#6366f1');

    deptChartInstance = new Chart(deptChartCanvas.value, {
      type: 'bar',
      data: {
        labels,
        datasets: [{
          label: 'Total Cost ($)',
          data: costs,
          backgroundColor: bgColors,
          borderRadius: 8,
          borderSkipped: false
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: false },
          tooltip: {
            callbacks: {
              label: context => `Failure Cost: $${(context.parsed.y || 0).toLocaleString()}`
            }
          }
        },
        scales: {
          x: {
            grid: { display: false },
            ticks: { font: { size: 11, weight: '500' }, color: '#64748b' }
          },
          y: {
            beginAtZero: true,
            grid: { color: 'rgba(226, 232, 240, 0.6)' },
            ticks: {
              font: { size: 11 },
              color: '#94a3b8',
              callback: val => `$${val >= 1000 ? (val / 1000) + 'k' : val}`
            }
          }
        }
      }
    });
  }

  // 3. Error Catalog Chart (Horizontal Bar Chart)
  if (catalogChartCanvas.value && props.charts?.costByErrorCatalog?.length) {
    // Show top 8 error catalogs
    const topCatalogs = props.charts.costByErrorCatalog.slice(0, 8);
    const labels = topCatalogs.map(c => c.catalog);
    const costs = topCatalogs.map(c => c.cost);

    catalogChartInstance = new Chart(catalogChartCanvas.value, {
      type: 'bar',
      data: {
        labels,
        datasets: [{
          axis: 'y',
          label: 'Cost (USD)',
          data: costs,
          backgroundColor: 'rgba(14, 165, 233, 0.8)', // Sky
          hoverBackgroundColor: '#0284c7',
          borderRadius: 6
        }]
      },
      options: {
        indexAxis: 'y',
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: false },
          tooltip: {
            callbacks: {
              label: context => `Cost: $${(context.parsed.x || 0).toLocaleString()}`
            }
          }
        },
        scales: {
          x: {
            beginAtZero: true,
            grid: { color: 'rgba(226, 232, 240, 0.6)' },
            ticks: {
              font: { size: 10 },
              color: '#94a3b8',
              callback: val => `$${val >= 1000 ? (val / 1000) + 'k' : val}`
            }
          },
          y: {
            grid: { display: false },
            ticks: { font: { size: 11 }, color: '#475569' }
          }
        }
      }
    });
  }

  // 4. Errors by 4M Analysis (Donut Chart)
  if (m4ChartCanvas.value && props.charts?.errorsBy4M?.counts) {
    const counts = props.charts.errorsBy4M.counts;
    const labels = ['Man', 'Machine', 'Material', 'Method'];
    const data = labels.map(l => counts[l] || 0);

    m4ChartInstance = new Chart(m4ChartCanvas.value, {
      type: 'doughnut',
      data: {
        labels,
        datasets: [{
          data,
          backgroundColor: [
            '#6366f1', // Man -> Indigo
            '#06b6d4', // Machine -> Cyan
            '#f59e0b', // Material -> Amber
            '#10b981'  // Method -> Emerald
          ],
          borderWidth: 2,
          borderColor: '#ffffff',
          hoverOffset: 8
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        cutout: '65%',
        plugins: {
          legend: {
            position: 'bottom',
            labels: {
              boxWidth: 12,
              padding: 16,
              font: { size: 11, family: 'Inter, sans-serif' },
              color: '#64748b'
            }
          },
          tooltip: {
            callbacks: {
              label: context => {
                const total = data.reduce((a, b) => a + b, 0);
                const val = context.raw || 0;
                const pct = total > 0 ? ((val / total) * 100).toFixed(1) : 0;
                return `${context.label}: ${val} errors (${pct}%)`;
              }
            }
          }
        }
      }
    });
  }
}

onMounted(async () => {
  await nextTick();
  initCharts();
});

watch(
  () => props.charts,
  async () => {
    await nextTick();
    initCharts();
  },
  { deep: true }
);

onBeforeUnmount(() => {
  destroyCharts();
});
</script>
