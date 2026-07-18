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
        <span class="px-3 py-1.5 rounded-lg bg-indigo-50 dark:bg-indigo-950/40 border border-indigo-200 dark:border-indigo-800/50 text-indigo-600 dark:text-indigo-400 font-medium">
          {{ activeTab === 'Global' ? 'All Departments' : activeTab + ' Department' }}
        </span>
      </div>
    </header>

    <!-- Sub-Navigation Tab Switcher -->
    <DeptTabNavigation 
      :active-tab="activeTab" 
      @tab-change="onTabChange" 
    />

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
      :total-main-tasks="totalMainTasks"
      :total-sub-tasks="totalSubTasks"
      :on-time-percentage="onTimePercentage"
      :on-time-projects-count="onTimeProjectsCount"
      :total-projects-count="totalProjectsCount"
      :active-projects-count="activeProjectsCount"
      :delayed-projects-count="delayedProjectsCount"
    />

    <!-- Visualizations / Charts Section -->
    <DeptCharts 
      :filtered-tasks="filteredTasks"
      :filtered-projects="filteredProjects"
    />

    <!-- Project Data Portfolio Registry -->
    <DeptProjectTable 
      :filtered-projects="filteredProjects"
      :active-tab="activeTab"
    />
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useAuthStore } from '../../stores/auth';

// Split Child Components imports
import DeptTabNavigation from '../../components/KPI_System/DeptTabNavigation.vue';
import DeptKpiCards from '../../components/KPI_System/DeptKpiCards.vue';
import DeptCharts from '../../components/KPI_System/DeptCharts.vue';
import DeptProjectTable from '../../components/KPI_System/DeptProjectTable.vue';

// Authentication Store Injection
const authStore = useAuthStore();

// Tab Switcher State
const activeTab = ref('Global');

const onTabChange = (tabId) => {
  activeTab.value = tabId;
};

const getTabIcon = (tabId) => {
  const tabIcons = {
    Global: 'pi pi-globe',
    Electrical: 'pi pi-bolt',
    Mechanical: 'pi pi-cog',
    Planning: 'pi pi-calendar'
  };
  return tabIcons[tabId] || 'pi pi-circle';
};

// Generates exactly 5 Main Tasks, and exactly 8 Sub Tasks per Main Task
const generateMockTasks = (projectStatus) => {
  const mainTasks = [];
  const mainTaskNames = [
    "Requirements & System Design",
    "Procurement & Hardware Assembly",
    "Software Coding & Configuration",
    "Integration & Dry Run Testing",
    "Final Delivery & Commissioning"
  ];

  for (let i = 0; i < 5; i++) {
    const subTasks = [];
    for (let j = 1; j <= 8; j++) {
      let subStatus = "Not yet start";
      
      if (projectStatus === "On Time") {
        subStatus = (i * 8 + j) % 5 === 0 ? "Ahead of schedule" : "On Time";
      } else if (projectStatus === "Ahead of schedule") {
        subStatus = "Ahead of schedule";
      } else if (projectStatus === "Delay") {
        // "delay" means started and finished past overdue date (so 100% progress but status is delay)
        subStatus = (i * 8 + j) % 3 === 0 ? "Delay" : "On Time";
      } else if (projectStatus === "Doing") {
        // In-progress project
        if (i < 2) {
          subStatus = "On Time";
        } else if (i === 2) {
          subStatus = j <= 4 ? "Doing" : "Not yet start";
        } else {
          subStatus = "Not yet start";
        }
      } else if (projectStatus === "Not yet start" || projectStatus === "No plan") {
        subStatus = "Not yet start";
      }

      subTasks.push({
        name: `Sub Task ${i + 1}.${j} - Sub-step`,
        status: subStatus
      });
    }
    
    mainTasks.push({
      name: mainTaskNames[i],
      subTasks
    });
  }
  return mainTasks;
};

// Dynamic hierarchical data resolution (calculates progress and status down from subtasks)
const resolveMainTask = (mainTask) => {
  const subTasksResolved = mainTask.subTasks.map(st => {
    let progress = 0;
    if (st.status === 'On Time' || st.status === 'Ahead of schedule' || st.status === 'Delay') {
      progress = 100;
    } else if (st.status === 'Doing') {
      progress = 50;
    }
    return { name: st.name, status: st.status, progress };
  });

  const totalProgress = subTasksResolved.reduce((sum, st) => sum + st.progress, 0);
  const progress = Math.round(totalProgress / subTasksResolved.length);

  // Status Precedence Rules: Delay > Doing > Not yet start > Ahead of schedule > On Time
  let status = 'Not yet start';
  const hasDelay = subTasksResolved.some(st => st.status === 'Delay');
  const hasDoing = subTasksResolved.some(st => st.status === 'Doing');
  const allNotStart = subTasksResolved.every(st => st.status === 'Not yet start');
  const allAhead = subTasksResolved.every(st => st.status === 'Ahead of schedule');
  const allAheadOrOnTime = subTasksResolved.every(st => st.status === 'Ahead of schedule' || st.status === 'On Time');

  if (hasDelay) {
    status = 'Delay';
  } else if (hasDoing) {
    status = 'Doing';
  } else if (allNotStart) {
    status = 'Not yet start';
  } else if (allAhead) {
    status = 'Ahead of schedule';
  } else if (allAheadOrOnTime) {
    status = 'On Time';
  } else {
    status = progress > 0 && progress < 100 ? 'Doing' : 'On Time';
  }

  const counts = {
    total: subTasksResolved.length,
    onTime: subTasksResolved.filter(st => st.status === 'On Time').length,
    aheadOfSchedule: subTasksResolved.filter(st => st.status === 'Ahead of schedule').length,
    delayed: subTasksResolved.filter(st => st.status === 'Delay').length,
    doing: subTasksResolved.filter(st => st.status === 'Doing').length,
    notYetStart: subTasksResolved.filter(st => st.status === 'Not yet start').length
  };

  return {
    name: mainTask.name,
    progress,
    status,
    subTasks: subTasksResolved,
    counts
  };
};

const resolveProject = (project) => {
  const resolvedMainTasks = project.mainTasks.map(mt => resolveMainTask(mt));

  const totalProgress = resolvedMainTasks.reduce((sum, mt) => sum + mt.progress, 0);
  const progress = Math.round(totalProgress / resolvedMainTasks.length);

  // Status Precedence Rules: Delay > Doing > Not yet start > Ahead of schedule > On Time
  let status = 'Not yet start';
  const hasDelay = resolvedMainTasks.some(mt => mt.status === 'Delay');
  const hasDoing = resolvedMainTasks.some(mt => mt.status === 'Doing');
  const allNotStart = resolvedMainTasks.every(mt => mt.status === 'Not yet start');
  const allAhead = resolvedMainTasks.every(mt => mt.status === 'Ahead of schedule');
  const allAheadOrOnTime = resolvedMainTasks.every(mt => mt.status === 'Ahead of schedule' || mt.status === 'On Time');

  if (hasDelay) {
    status = 'Delay';
  } else if (hasDoing) {
    status = 'Doing';
  } else if (allNotStart) {
    status = 'Not yet start';
  } else if (allAhead) {
    status = 'Ahead of schedule';
  } else if (allAheadOrOnTime) {
    status = 'On Time';
  } else {
    status = progress > 0 && progress < 100 ? 'Doing' : 'On Time';
  }

  const mainCounts = {
    total: resolvedMainTasks.length,
    onTime: resolvedMainTasks.filter(mt => mt.status === 'On Time').length,
    aheadOfSchedule: resolvedMainTasks.filter(mt => mt.status === 'Ahead of schedule').length,
    delayed: resolvedMainTasks.filter(mt => mt.status === 'Delay').length,
    doing: resolvedMainTasks.filter(mt => mt.status === 'Doing').length,
    notYetStart: resolvedMainTasks.filter(mt => mt.status === 'Not yet start').length
  };

  const subCounts = {
    total: resolvedMainTasks.reduce((sum, mt) => sum + mt.counts.total, 0),
    onTime: resolvedMainTasks.reduce((sum, mt) => sum + mt.counts.onTime, 0),
    aheadOfSchedule: resolvedMainTasks.reduce((sum, mt) => sum + mt.counts.aheadOfSchedule, 0),
    delayed: resolvedMainTasks.reduce((sum, mt) => sum + mt.counts.delayed, 0),
    doing: resolvedMainTasks.reduce((sum, mt) => sum + mt.counts.doing, 0),
    notYetStart: resolvedMainTasks.reduce((sum, mt) => sum + mt.counts.notYetStart, 0)
  };

  return {
    name: project.name,
    deadline: project.deadline,
    progress,
    status,
    mainTasks: resolvedMainTasks,
    tasks: {
      main: mainCounts,
      sub: subCounts
    }
  };
};

// Base data list containing projects and their targets
const rawDepartmentsData = {
  Electrical: {
    name: 'Electrical',
    description: 'Electrical engineering, panel wiring, cabling, and automation PLC systems.',
    colorClass: 'from-blue-600 to-cyan-500',
    projects: [
      { name: "Substation Control Panel Install", targetStatus: "Delay", deadline: "2026-06-15" },
      { name: "Main Switchboard Cabling", targetStatus: "On Time", deadline: "2026-07-20" },
      { name: "PLC Programming & Commissioning", targetStatus: "Ahead of schedule", deadline: "2026-07-30" },
      { name: "Backup Generator Wiring", targetStatus: "Doing", deadline: "2026-08-30" },
      { name: "Lighting Layout System Setup", targetStatus: "Not yet start", deadline: "2026-09-01" },
      { name: "Cable Tray Routing Layout", targetStatus: "Ahead of schedule", deadline: "2026-07-05" },
      { name: "Grounding System Verification", targetStatus: "No plan", deadline: "2026-11-30" }
    ]
  },
  Mechanical: {
    name: 'Mechanical',
    description: 'HVAC installation, mechanical structural assembly, piping, and commissioning.',
    colorClass: 'from-amber-500 to-orange-600',
    projects: [
      { name: "HVAC Ductwork Installation", targetStatus: "On Time", deadline: "2026-07-25" },
      { name: "Chiller Plant Assembly", targetStatus: "Doing", deadline: "2026-08-10" },
      { name: "Pump Commissioning & Alignment", targetStatus: "Ahead of schedule", deadline: "2026-07-15" },
      { name: "Ventilation Fan Balancing", targetStatus: "No plan", deadline: "2026-10-15" },
      { name: "Steam Pipe Welding & NDT", targetStatus: "Delay", deadline: "2026-06-25" },
      { name: "Cooling Tower Rigging Plan", targetStatus: "Not yet start", deadline: "2026-09-10" }
    ]
  },
  Planning: {
    name: 'Planning',
    description: 'Scheduling, resource allocation, risk mitigation, and project auditing.',
    colorClass: 'from-purple-600 to-indigo-500',
    projects: [
      { name: "Resource Allocation Map Q3", targetStatus: "On Time", deadline: "2026-07-01" },
      { name: "Risk Assessment Report", targetStatus: "Doing", deadline: "2026-08-05" },
      { name: "Procurement Schedule Sync", targetStatus: "Not yet start", deadline: "2026-09-15" },
      { name: "Milestone Tracking Dashboard", targetStatus: "Ahead of schedule", deadline: "2026-07-28" },
      { name: "Vendor Contract Alignment", targetStatus: "Delay", deadline: "2026-06-20" }
    ]
  }
};

// Map raw data into the full dynamic hierarchical trees
const resolvedDepartmentsData = computed(() => {
  const data = {};
  Object.keys(rawDepartmentsData).forEach(deptKey => {
    const dept = rawDepartmentsData[deptKey];
    data[deptKey] = {
      ...dept,
      projects: dept.projects.map(p => {
        const generatedTasks = generateMockTasks(p.targetStatus);
        return resolveProject({
          name: p.name,
          deadline: p.deadline,
          mainTasks: generatedTasks
        });
      })
    };
  });
  return data;
});

const currentDepartment = computed(() => {
  if (activeTab.value === 'Global') return null;
  return resolvedDepartmentsData.value[activeTab.value] || null;
});

// Filtered Projects based on selection
const filteredProjects = computed(() => {
  const deptData = resolvedDepartmentsData.value;
  if (activeTab.value === 'Global') {
    return [
      ...deptData.Electrical.projects.map(p => ({ ...p, dept: 'Electrical' })),
      ...deptData.Mechanical.projects.map(p => ({ ...p, dept: 'Mechanical' })),
      ...deptData.Planning.projects.map(p => ({ ...p, dept: 'Planning' }))
    ];
  } else {
    return deptData[activeTab.value].projects.map(p => ({ ...p, dept: activeTab.value }));
  }
});

// Dynamically Aggregates Tasks based on filtered projects
const filteredTasks = computed(() => {
  const agg = {
    main: { onTime: 0, aheadOfSchedule: 0, delayed: 0 },
    sub: { onTime: 0, aheadOfSchedule: 0, delayed: 0 }
  };
  
  filteredProjects.value.forEach(project => {
    if (project.tasks) {
      agg.main.onTime += project.tasks.main.onTime;
      agg.main.aheadOfSchedule += project.tasks.main.aheadOfSchedule;
      agg.main.delayed += project.tasks.main.delayed;

      agg.sub.onTime += project.tasks.sub.onTime;
      agg.sub.aheadOfSchedule += project.tasks.sub.aheadOfSchedule;
      agg.sub.delayed += project.tasks.sub.delayed;
    }
  });
  
  return agg;
});

// Card Metric Calculations
const totalMainTasks = computed(() => {
  const t = filteredTasks.value;
  return t.main.onTime + t.main.aheadOfSchedule + t.main.delayed;
});

const totalSubTasks = computed(() => {
  const t = filteredTasks.value;
  return t.sub.onTime + t.sub.aheadOfSchedule + t.sub.delayed;
});

const onTimeProjectsCount = computed(() => {
  return filteredProjects.value.filter(p => p.status === 'On Time' || p.status === 'Ahead of schedule').length;
});

const totalProjectsCount = computed(() => {
  return filteredProjects.value.length;
});

const activeProjectsCount = computed(() => {
  return filteredProjects.value.filter(p => p.status === 'Doing').length;
});

const delayedProjectsCount = computed(() => {
  return filteredProjects.value.filter(p => p.status === 'Delay').length;
});

const onTimePercentage = computed(() => {
  if (totalProjectsCount.value === 0) return 0;
  return Math.round((onTimeProjectsCount.value / totalProjectsCount.value) * 100);
});
</script>

<style scoped>
h1 {
  font-size: 1.875rem !important;
  line-height: 2.25rem !important;
}
</style>
