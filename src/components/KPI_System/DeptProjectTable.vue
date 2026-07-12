<template>
  <!-- Project Data Table Section -->
  <section class="relative z-10 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl shadow-sm overflow-hidden">
    <!-- Table Header & Controls -->
    <div class="p-6 border-b border-slate-200 dark:border-slate-800 flex flex-col md:flex-row md:items-center justify-between gap-4">
      <div>
        <h3 class="font-bold text-lg text-slate-800 dark:text-slate-200">Project Portfolio Registry</h3>
        <p class="text-xs text-slate-500 dark:text-slate-400">Detailed progress tracker, deadlines, and task breakdowns for the active department</p>
      </div>
      
      <!-- Table Search & Filters -->
      <div class="flex items-center gap-3">
        <div class="relative">
          <span class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-slate-400">
            <i class="pi pi-search text-xs"></i>
          </span>
          <input 
            v-model="searchQuery" 
            type="text" 
            placeholder="Search projects..." 
            class="pl-9 pr-4 py-2 border border-slate-200 dark:border-slate-700 rounded-xl bg-slate-50 dark:bg-slate-800 text-xs focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 focus:outline-none transition-all w-60 text-slate-700 dark:text-slate-350"
          />
        </div>
      </div>
    </div>

    <!-- Data Table -->
    <div class="overflow-x-auto">
      <table class="w-full text-left border-collapse">
        <thead>
          <tr class="bg-slate-50 dark:bg-slate-900/60 text-slate-500 dark:text-slate-400 font-semibold text-xs border-b border-slate-200 dark:border-slate-800">
            <th class="px-6 py-4">Project Name</th>
            <th v-if="activeTab === 'Global'" class="px-6 py-4">Department</th>
            <th class="px-6 py-4">Progress</th>
            <th class="px-6 py-4">Main Tasks Breakdown</th>
            <th class="px-6 py-4">Sub Tasks Breakdown</th>
            <th class="px-6 py-4">Status</th>
            <th class="px-6 py-4">Deadline</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-slate-100 dark:divide-slate-800/80 text-xs">
          <tr 
            v-for="project in paginatedProjects" 
            :key="project.name"
            class="hover:bg-slate-50/55 dark:hover:bg-slate-800/40 transition-colors duration-250"
          >
            <!-- Project Name -->
            <td class="px-6 py-4 font-semibold text-slate-900 dark:text-slate-100">
              {{ project.name }}
            </td>
            
            <!-- Department (Global View Only) -->
            <td v-if="activeTab === 'Global'" class="px-6 py-4">
              <span class="px-2 py-1 rounded text-[10px] font-medium" :class="getDepartmentBadgeStyle(project.dept)">
                {{ project.dept }}
              </span>
            </td>
            
            <!-- Progress Bar -->
            <td class="px-6 py-4 min-w-[140px]">
              <div class="flex items-center gap-3">
                <div class="w-full bg-slate-100 dark:bg-slate-800 rounded-full h-2">
                  <div 
                    class="h-2 rounded-full transition-all duration-500" 
                    :style="{ width: project.progress + '%' }"
                    :class="getProgressColorClass(project.progress, project.status)"
                  ></div>
                </div>
                <span class="font-bold text-slate-700 dark:text-slate-300">{{ project.progress }}%</span>
              </div>
            </td>

            <!-- Main Tasks Breakdown -->
            <td class="px-6 py-4">
              <div class="flex flex-col gap-1" v-if="project.tasks">
                <span class="font-bold text-slate-900 dark:text-slate-100 text-xs">
                  {{ project.tasks.main.total }} Tasks
                </span>
                <div class="flex items-center gap-1 text-[9px]">
                  <span title="Ahead of schedule" class="px-1.5 py-0.5 bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 rounded font-semibold">
                    ▲ {{ project.tasks.main.aheadOfSchedule }}
                  </span>
                  <span title="On Time" class="px-1.5 py-0.5 bg-blue-500/10 text-blue-600 dark:text-blue-400 rounded font-semibold">
                    ● {{ project.tasks.main.onTime }}
                  </span>
                  <span title="Delay" class="px-1.5 py-0.5 bg-rose-500/10 text-rose-600 dark:text-rose-400 rounded font-semibold">
                    ▼ {{ project.tasks.main.delayed }}
                  </span>
                </div>
              </div>
              <span v-else class="text-slate-400">N/A</span>
            </td>

            <!-- Sub Tasks Breakdown -->
            <td class="px-6 py-4">
              <div class="flex flex-col gap-1" v-if="project.tasks">
                <span class="font-bold text-slate-900 dark:text-slate-100 text-xs">
                  {{ project.tasks.sub.total }} Tasks
                </span>
                <div class="flex items-center gap-1 text-[9px]">
                  <span title="Ahead of schedule" class="px-1.5 py-0.5 bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 rounded font-semibold">
                    ▲ {{ project.tasks.sub.aheadOfSchedule }}
                  </span>
                  <span title="On Time" class="px-1.5 py-0.5 bg-blue-500/10 text-blue-600 dark:text-blue-400 rounded font-semibold">
                    ● {{ project.tasks.sub.onTime }}
                  </span>
                  <span title="Delay" class="px-1.5 py-0.5 bg-rose-500/10 text-rose-600 dark:text-rose-400 rounded font-semibold">
                    ▼ {{ project.tasks.sub.delayed }}
                  </span>
                </div>
              </div>
              <span v-else class="text-slate-400">N/A</span>
            </td>

            <!-- Project Status -->
            <td class="px-6 py-4">
              <div class="flex flex-wrap gap-1">
                <span 
                  v-for="badge in [project.status]" 
                  :key="badge"
                  class="px-2.5 py-1 text-[10px] font-bold rounded-full border shadow-sm"
                  :class="getStatusBadgeStyle(badge)"
                >
                  {{ badge }}
                </span>
              </div>
            </td>
            
            <!-- Deadline -->
            <td class="px-6 py-4 text-slate-600 dark:text-slate-400 font-medium">
              <div class="flex items-center gap-1.5">
                <i class="pi pi-calendar text-[10px]" :class="isOverdue(project.deadline, project.progress) ? 'text-rose-500' : 'text-slate-400'"></i>
                <span :class="{ 'text-rose-500 font-bold': isOverdue(project.deadline, project.progress) }">
                  {{ formatDate(project.deadline) }}
                </span>
                <span v-if="isOverdue(project.deadline, project.progress)" class="ml-1 text-[9px] font-extrabold text-rose-500 uppercase tracking-wider">
                  Overdue
                </span>
              </div>
            </td>
          </tr>
          <tr v-if="paginatedProjects.length === 0">
            <td :colspan="activeTab === 'Global' ? 7 : 6" class="px-6 py-12 text-center text-slate-400 dark:text-slate-500">
              <div class="flex flex-col items-center justify-center gap-2">
                <i class="pi pi-inbox text-3xl"></i>
                <span>No projects matched your search criteria.</span>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Pagination Footer -->
    <div v-if="filteredAndSearchedProjects.length > itemsPerPage" class="p-4 border-t border-slate-200 dark:border-slate-800 flex items-center justify-between text-xs bg-slate-50/50 dark:bg-slate-900/30">
      <span class="text-slate-500">
        Showing {{ startIdx + 1 }} to {{ Math.min(endIdx, filteredAndSearchedProjects.length) }} of {{ filteredAndSearchedProjects.length }} projects
      </span>
      <div class="flex items-center gap-1">
        <button 
          @click="currentPage = Math.max(1, currentPage - 1)" 
          :disabled="currentPage === 1"
          class="p-2 border border-slate-200 dark:border-slate-800 rounded-lg hover:bg-slate-100 dark:hover:bg-slate-800 disabled:opacity-50 disabled:hover:bg-transparent text-slate-600 dark:text-slate-400 transition-colors"
        >
          <i class="pi pi-angle-left"></i>
        </button>
        <span class="px-3 font-semibold text-slate-700 dark:text-slate-300">
          Page {{ currentPage }} of {{ totalPages }}
        </span>
        <button 
          @click="currentPage = Math.min(totalPages, currentPage + 1)" 
          :disabled="currentPage === totalPages"
          class="p-2 border border-slate-200 dark:border-slate-800 rounded-lg hover:bg-slate-100 dark:hover:bg-slate-800 disabled:opacity-50 disabled:hover:bg-transparent text-slate-600 dark:text-slate-400 transition-colors"
        >
          <i class="pi pi-angle-right"></i>
        </button>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, computed, watch } from 'vue';

const props = defineProps({
  filteredProjects: {
    type: Array,
    required: true
  },
  activeTab: {
    type: String,
    required: true
  }
});

const searchQuery = ref('');
const currentPage = ref(1);
const itemsPerPage = 6;

// Reset page upon tab toggles
watch(() => props.activeTab, () => {
  currentPage.value = 1;
});

// Search Filter
const filteredAndSearchedProjects = computed(() => {
  const query = searchQuery.value.toLowerCase().trim();
  if (!query) return props.filteredProjects;
  return props.filteredProjects.filter(p => 
    p.name.toLowerCase().includes(query) || 
    p.status.toLowerCase().includes(query) ||
    (p.dept && p.dept.toLowerCase().includes(query))
  );
});

// Pagination Calculations
const totalPages = computed(() => {
  return Math.ceil(filteredAndSearchedProjects.value.length / itemsPerPage) || 1;
});

const startIdx = computed(() => (currentPage.value - 1) * itemsPerPage);
const endIdx = computed(() => startIdx.value + itemsPerPage);

const paginatedProjects = computed(() => {
  return filteredAndSearchedProjects.value.slice(startIdx.value, endIdx.value);
});

// Styling Helpers
const getStatusBadgeStyle = (status) => {
  switch (status) {
    case 'Ahead of schedule':
      return 'bg-emerald-50 text-emerald-700 border border-emerald-200 dark:bg-emerald-950/40 dark:text-emerald-300 dark:border-emerald-800/60';
    case 'On Time':
      return 'bg-blue-50 text-blue-700 border border-blue-200 dark:bg-blue-950/40 dark:text-blue-300 dark:border-blue-800/60';
    case 'Doing':
      return 'bg-amber-50 text-amber-700 border border-amber-200 dark:bg-amber-950/40 dark:text-amber-300 dark:border-amber-800/60';
    case 'Not yet start':
      return 'bg-slate-100 text-slate-600 border border-slate-200 dark:bg-slate-800/60 dark:text-slate-400 dark:border-slate-700/60';
    case 'No plan':
      return 'bg-purple-50 text-purple-700 border border-purple-200 dark:bg-purple-950/40 dark:text-purple-300 dark:border-purple-800/60';
    case 'Delay':
      return 'bg-rose-50 text-rose-700 border border-rose-200 dark:bg-rose-950/40 dark:text-rose-300 dark:border-rose-800/60';
    default:
      return 'bg-slate-50 text-slate-700 border border-slate-200 dark:bg-slate-900 dark:text-slate-300 dark:border-slate-800';
  }
};

const getDepartmentBadgeStyle = (dept) => {
  switch (dept) {
    case 'Electrical':
      return 'bg-blue-50 text-blue-700 border border-blue-200/50 dark:bg-blue-950/30 dark:text-blue-300 dark:border-blue-800/40';
    case 'Mechanical':
      return 'bg-amber-50 text-amber-700 border border-amber-200/50 dark:bg-amber-950/30 dark:text-amber-300 dark:border-amber-800/40';
    case 'Planning':
      return 'bg-purple-50 text-purple-700 border border-purple-200/50 dark:bg-purple-950/30 dark:text-purple-300 dark:border-purple-800/40';
    default:
      return 'bg-slate-100 text-slate-600 dark:bg-slate-900 dark:text-slate-400';
  }
};

const getProgressColorClass = (progress, status) => {
  if (status === 'Delay') return 'bg-rose-500';
  if (progress === 100) return 'bg-emerald-500';
  return 'bg-indigo-600';
};

const formatDate = (dateStr) => {
  const options = { year: 'numeric', month: 'short', day: 'numeric' };
  return new Date(dateStr).toLocaleDateString('en-US', options);
};

const isOverdue = (deadlineStr, progress) => {
  if (progress === 100) return false;
  return new Date(deadlineStr) < new Date();
};
</script>
