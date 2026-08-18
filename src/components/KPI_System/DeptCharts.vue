<template>
  <!-- Visualizations / Charts Section -->
  <section class="relative z-10 grid grid-cols-1 lg:grid-cols-5 gap-6">
    <!-- Task Status Stacked Bar Chart -->
    <div class="lg:col-span-3 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl p-6 shadow-sm">
      <div class="flex items-center justify-between mb-4">
        <div>
          <h3 class="font-bold text-slate-800 dark:text-slate-200">Task Status Distribution</h3>
          <p class="text-xs text-slate-500 dark:text-slate-400">Comparing Main vs Sub task volume per status</p>
        </div>
        <span class="text-xs font-semibold text-slate-400 px-2 py-1 rounded bg-slate-50 dark:bg-slate-850 border border-slate-200/50 dark:border-slate-800">
          Stacked Bar Chart
        </span>
      </div>
      <div class="relative h-64 w-full">
        <canvas id="taskChartSub"></canvas>
      </div>
    </div>

    <!-- Project Status Donut Chart -->
    <div class="lg:col-span-2 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl p-6 shadow-sm">
      <div class="flex items-center justify-between mb-4">
        <div>
          <h3 class="font-bold text-slate-800 dark:text-slate-200">Project Status Allocation</h3>
          <p class="text-xs text-slate-500 dark:text-slate-400">Overview of project pipeline health</p>
        </div>
        <span class="text-xs font-semibold text-slate-400 px-2 py-1 rounded bg-slate-50 dark:bg-slate-850 border border-slate-200/50 dark:border-slate-800">
          Donut Chart
        </span>
      </div>
      <div class="relative h-64 w-full">
        <canvas id="projectChartSub"></canvas>
      </div>
    </div>
  </section>
</template>

<script setup>
import { onMounted, watch, onBeforeUnmount, nextTick } from 'vue';
import { Chart, registerables } from 'chart.js';

Chart.register(...registerables);

const props = defineProps({
  deptKpiSummaryData: {
    type: Object,
    required: true
  }
});

let taskChart = null;
let projectChart = null;
const getTaskChartData = () => {
  const design_data = props.deptKpiSummaryData;
  const design_m = design_data.subTask["Design (M)"]
  const design_e = design_data.subTask["Design (E)"]

  return {
    labels: ['On time', 'Delay', 'Doing', 'Not Yet Start', 'No Plan'],
    datasets: [
      {
        label: 'Electrical',
        data: [design_e.onTime, design_e.delayed, design_e.doing, design_e.notYetStart, design_e.noPlan],
        backgroundColor: '#4f46e5', // Indigo 600
        hoverBackgroundColor: '#4338ca',
        borderRadius: 6
      },
      {
        label: 'Mechanical',
        data: [design_m.onTime, design_m.delayed, design_m.doing, design_m.notYetStart, design_m.noPlan],
        backgroundColor: '#818cf8', // Indigo 400
        hoverBackgroundColor: '#6366f1',
        borderRadius: 6
      }
    ]
  };
};

const getProjectChartData = () => {
  const main_task = props.deptKpiSummaryData.mainTask;
  const statuses = ["Not Yet Start", "On Time", "Doing", "No Plan", "Delay"];
  
  return {
    labels: statuses,
    datasets: [{
      data: [main_task.notYetStart, main_task.onTime, main_task.doing, main_task.noPlan, main_task.delayed],
      backgroundColor: [
        '#94a3b8', // Not yet start -> Slate 400
        '#3b82f6', // On Time -> Blue 500
        '#f59e0b', // Doing -> Amber 500
        '#a78bfa', // No plan -> Violet 400
        '#ef4444'  // Delay -> Red 500
      ],
      borderWidth: 0,
      hoverOffset: 6
    }]
  };
};

const initCharts = () => {
  const ctxTask = document.getElementById('taskChartSub');
  const ctxProject = document.getElementById('projectChartSub');
  
  if (ctxTask && ctxProject) {
    // Task stacked bar chart initialization
    taskChart = new Chart(ctxTask, {
      type: 'bar',
      data: getTaskChartData(),
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: 'bottom',
            labels: {
              boxWidth: 10,
              padding: 20,
              font: { size: 11, family: 'Inter, sans-serif' },
              color: '#64748b'
            }
          },
          tooltip: {
            backgroundColor: '#0f172a',
            padding: 10,
            titleFont: { size: 12, weight: 'bold' },
            bodyFont: { size: 12 },
            cornerRadius: 8
          }
        },
        scales: {
          x: {
            stacked: true,
            grid: { display: false },
            ticks: { font: { size: 10 }, color: '#64748b' }
          },
          y: {
            stacked: true,
            beginAtZero: true,
            ticks: { font: { size: 10 }, precision: 0, color: '#64748b' },
            grid: { color: 'rgba(226, 232, 240, 0.5)' }
          }
        }
      }
    });

    // Project distribution donut chart initialization
    projectChart = new Chart(ctxProject, {
      type: 'doughnut',
      data: getProjectChartData(),
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: 'bottom',
            labels: {
              boxWidth: 10,
              padding: 12,
              font: { size: 10, family: 'Inter, sans-serif' },
              color: '#64748b'
            }
          },
          tooltip: {
            backgroundColor: '#0f172a',
            padding: 10,
            cornerRadius: 8
          }
        },
        cutout: '70%',
        radius: '90%'
      }
    });
  }
};

const updateCharts = () => {
  if (taskChart) {
    taskChart.data = getTaskChartData();
    taskChart.update();
  }
  if (projectChart) {
    projectChart.data = getProjectChartData();
    projectChart.update();
  }
};

watch(() => props.deptKpiSummaryData, () => {
  updateCharts();
}, { deep: true });

watch(() => props.deptKpiSummaryData, () => {
  updateCharts();
}, { deep: true });

onMounted(() => {
  nextTick(() => {
    // Small timeout to guarantee DOM layouts are computed
    setTimeout(() => {
      initCharts();
    }, 100);
  });
});

onBeforeUnmount(() => {
  if (taskChart) taskChart.destroy();
  if (projectChart) projectChart.destroy();
});
</script>

<style scoped>
canvas {
  width: 100% !important;
  height: 100% !important;
}
</style>
