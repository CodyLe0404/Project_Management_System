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
  filteredTasks: {
    type: Object,
    required: true
  },
  filteredProjects: {
    type: Array,
    required: true
  }
});

let taskChart = null;
let projectChart = null;

const getTaskChartData = () => {
  const t = props.filteredTasks;
  return {
    labels: ['On time', 'Ahead of schedule', 'Delay'],
    datasets: [
      {
        label: 'Main Tasks',
        data: [t.main.onTime, t.main.aheadOfSchedule, t.main.delayed],
        backgroundColor: '#4f46e5', // Indigo 600
        hoverBackgroundColor: '#4338ca',
        borderRadius: 6
      },
      {
        label: 'Sub Tasks',
        data: [t.sub.onTime, t.sub.aheadOfSchedule, t.sub.delayed],
        backgroundColor: '#818cf8', // Indigo 400
        hoverBackgroundColor: '#6366f1',
        borderRadius: 6
      }
    ]
  };
};

const getProjectChartData = () => {
  const projects = props.filteredProjects;
  const statuses = ["Ahead of schedule", "Not yet start", "On Time", "Doing", "No plan", "Delay"];
  const counts = statuses.map(status => projects.filter(p => p.status === status).length);
  
  return {
    labels: statuses,
    datasets: [{
      data: counts,
      backgroundColor: [
        '#10b981', // Ahead of schedule -> Emerald 500
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

watch(() => props.filteredTasks, () => {
  updateCharts();
}, { deep: true });

watch(() => props.filteredProjects, () => {
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
