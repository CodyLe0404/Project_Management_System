<template>
  <div class="space-y-6">
    <!-- Controls Panel: Search, Role Filter, View Toggle -->
    <div class="bg-white/90 backdrop-blur-md border border-slate-200 rounded-2xl p-4 flex flex-col md:flex-row items-center justify-between gap-4">
      <!-- Search Input -->
      <div class="relative w-full md:max-w-xs">
        <i class="pi pi-search absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-500 text-sm"></i>
        <input 
          v-model="searchQuery" 
          type="text" 
          placeholder="Search member name or role..." 
          class="w-full bg-slate-50 border border-slate-200 rounded-xl py-2 pl-10 pr-4 text-slate-900 placeholder-slate-500 focus:outline-none focus:border-indigo-500/80 focus:ring-1 focus:ring-indigo-500/80 transition-all text-sm"
        />
      </div>

      <!-- Filters & Layout toggle -->
      <div class="flex flex-wrap items-center justify-end gap-3 w-full md:w-auto">
        <!-- Role Dropdown Filter -->
        <div class="relative w-full sm:w-auto min-w-[160px]">
          <select 
            v-model="selectedRole" 
            class="w-full bg-slate-50 border border-slate-200 rounded-xl py-2 px-3 text-slate-900 focus:outline-none focus:border-indigo-500/80 transition-all text-sm appearance-none cursor-pointer"
          >
            <option value="ALL">All Roles</option>
            <option v-for="role in uniqueRoles" :key="role" :value="role">{{ role }}</option>
          </select>
          <i class="pi pi-chevron-down absolute right-3 top-1/2 -translate-y-1/2 text-slate-500 pointer-events-none text-xs"></i>
        </div>

        <!-- Layout Mode Toggle Buttons -->
        <div class="flex bg-slate-50 p-1 rounded-xl border border-slate-200">
          <button 
            @click="layoutMode = 'grid'" 
            :class="layoutMode === 'grid' ? 'bg-indigo-600/20 border-indigo-500/30 text-indigo-600' : 'text-slate-500 hover:text-slate-700 border-transparent'"
            class="px-3 py-1.5 rounded-lg border text-xs font-semibold flex items-center gap-1.5 transition-all"
            title="Grid View"
          >
            <i class="pi pi-th-large text-xs"></i>
            Grid
          </button>
          <button 
            @click="layoutMode = 'table'" 
            :class="layoutMode === 'table' ? 'bg-indigo-600/20 border-indigo-500/30 text-indigo-600' : 'text-slate-500 hover:text-slate-700 border-transparent'"
            class="px-3 py-1.5 rounded-lg border text-xs font-semibold flex items-center gap-1.5 transition-all"
            title="List Table View"
          >
            <i class="pi pi-list text-xs"></i>
            Table
          </button>
        </div>
      </div>
    </div>

    <!-- Empty State -->
    <div 
      v-if="filteredMembers.length === 0" 
      class="bg-white/90 border border-slate-200 rounded-2xl p-12 text-center text-slate-700 max-w-lg mx-auto"
    >
      <i class="pi pi-users text-4xl mb-3 block text-slate-500"></i>
      <h4 class="text-slate-900 font-bold text-base">No Members Found</h4>
      <p class="text-xs mt-1 text-slate-600">Try adjusting your filters or search keywords to find other staff members.</p>
    </div>

    <!-- Responsive Grid Layout -->
    <div 
      v-else-if="layoutMode === 'grid'" 
      class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6"
    >
      <div 
        v-for="member in filteredMembers" 
        :key="member.id"
        class="bg-white/90 backdrop-blur-md border border-slate-200 hover:border-slate-300 rounded-2xl p-6 shadow-lg transition-all duration-300 hover:-translate-y-1 hover:shadow-xl flex flex-col justify-between cursor-pointer group"
        @click="emitSelect(member)"
      >
        <!-- Profile Header -->
        <div>
          <div class="flex items-start gap-4">
            <div class="flex-1 min-w-0">
              <h4 class="text-base font-bold text-slate-900 truncate group-hover:text-indigo-600 transition-colors">
                {{ member.name }}
              </h4>
              <p class="text-xs text-slate-600 truncate mt-0.5">{{ member.title }} - {{ member.part }}</p>
              
              <!-- Task breakdown badge -->
              <div class="mt-2.5">
                <span class="inline-flex items-center gap-1.5 px-2 py-0.5 rounded-lg bg-indigo-500/10 text-indigo-400 border border-indigo-500/20 text-[11px] font-semibold">
                  <i class="pi pi-list text-[10px]"></i>
                  {{ member.mainTasksCount }} Main / {{ member.subTasksCount }} Sub
                </span>
              </div>
            </div>
          </div>
        </div>

        <!-- Custom Stacked Progress Bar & KPI details -->
        <div class="mt-6 space-y-4">
          <!-- Multi-colored progress segment -->
          <div class="space-y-1">
            <div class="flex items-center justify-between text-xs font-semibold">
              <span class="text-slate-600">Task KPI Distribution</span>
              <span 
                class="px-2 py-0.5 rounded-md text-[10px]"
                :class="getOnTimeColorClass(getMemberOnTimeRate(member))"
              >
                On-time: {{ getMemberOnTimeRate(member) }}%
              </span>
            </div>
            
            <!-- Stacked bar -->
            <div class="h-3 w-full bg-slate-100 rounded-full overflow-hidden flex border border-slate-200">
              <div 
                v-if="(member.onTime || 0) + (member.ahead || 0) > 0"
                class="h-full bg-blue-500 transition-all"
                :style="{ width: `${getTaskPercentage(member, 'onTime')}%` }"
                title="On Time"
              ></div>
              <div 
                v-if="member.delay > 0"
                class="h-full bg-rose-500 transition-all"
                :style="{ width: `${getTaskPercentage(member, 'delay')}%` }"
                title="Delayed"
              ></div>
            </div>
            
            <!-- Legend indicators -->
            <div class="flex justify-between items-center text-[10px] text-slate-500 pt-1">
              <span class="flex items-center gap-1"><span class="w-1.5 h-1.5 rounded-full bg-blue-500"></span>On-Time ({{ (member.onTime || 0) + (member.ahead || 0) }})</span>
              <span class="flex items-center gap-1"><span class="w-1.5 h-1.5 rounded-full bg-rose-500"></span>Delayed ({{ member.delay || 0 }})</span>
            </div>
          </div>
          
          <!-- Bottom actions -->
          <div class="pt-3 border-t border-slate-200 flex items-center justify-between text-xs text-slate-600">
            <span class="text-[11px] font-medium flex items-center gap-1">
              <i class="pi pi-folder text-slate-500"></i>
              Projects: {{ member.projectCount || 0 }}
            </span>
            <span class="text-indigo-400 group-hover:translate-x-1 transition-transform flex items-center gap-1 font-semibold text-[11px]">
              Details
              <i class="pi pi-arrow-right text-[10px]"></i>
            </span>
          </div>
        </div>
      </div>
    </div>

    <!-- Elegant Table Layout -->
    <div 
      v-else 
      class="bg-white/90 border border-slate-200 rounded-2xl overflow-hidden shadow-lg"
    >
      <div class="overflow-x-auto">
        <table class="w-full text-left border-collapse">
          <thead>
            <tr class="border-b border-slate-200 bg-slate-50 text-xs font-semibold text-slate-600 tracking-wider">
              <th class="py-4 px-6">Member Profile</th>
              <th class="py-4 px-6">Task Breakdown</th>
              <th class="py-4 px-6 max-w-xs">Task Performance Ratio</th>
              <th class="py-4 px-6 text-center">On-Time %</th>
              <th class="py-4 px-6 text-center">Projects</th>
              <th class="py-4 px-6 text-center">Action</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-slate-200 text-sm">
            <tr 
              v-for="member in filteredMembers" 
              :key="member.id"
              class="hover:bg-slate-100 cursor-pointer transition-colors"
              @click="emitSelect(member)"
            >
              <!-- Profile cell -->
              <td class="py-4 px-6">
                <div class="flex items-center gap-3">
                  <div>
                    <h5 class="font-bold text-slate-900">{{ member.name }}</h5>
                    <p class="text-xs text-slate-600">{{ member.title }} - {{ member.part }}</p>
                  </div>
                </div>
              </td>
              
              <!-- Task breakdown -->
              <td class="py-4 px-6 whitespace-nowrap">
                <div class="flex flex-col gap-1">
                  <span class="text-xs font-semibold text-slate-700">
                    {{ member.mainTasksCount }} Main Tasks
                  </span>
                  <span class="text-[11px] text-slate-600">
                    {{ member.subTasksCount }} Sub Tasks
                  </span>
                </div>
              </td>
 
              <!-- Custom Stacked Progress Bar Column -->
              <td class="py-4 px-6 min-w-[200px]">
                <div class="space-y-1">
                  <div class="h-2 w-full bg-slate-100 rounded-full overflow-hidden flex border border-slate-200">
                    <div 
                      v-if="(member.onTime || 0) + (member.ahead || 0) > 0"
                      class="h-full bg-blue-500"
                      :style="{ width: `${getTaskPercentage(member, 'onTime')}%` }"
                    ></div>
                    <div 
                      v-if="member.delay > 0"
                      class="h-full bg-rose-500"
                      :style="{ width: `${getTaskPercentage(member, 'delay')}%` }"
                    ></div>
                  </div>
                  <div class="flex justify-between items-center text-[10px] text-slate-500 font-medium">
                    <span class="text-blue-500 font-bold">{{ (member.onTime || 0) + (member.ahead || 0) }} On-Time</span>
                    <span class="text-rose-500 font-bold">{{ member.delay || 0 }} Delayed</span>
                  </div>
                </div>
              </td>
 
              <!-- On-time % -->
              <td class="py-4 px-6 text-center font-bold">
                <span 
                  class="px-2.5 py-1 rounded-lg text-xs font-bold"
                  :class="getOnTimeColorClass(getMemberOnTimeRate(member))"
                >
                  {{ getMemberOnTimeRate(member) }}%
                </span>
              </td>
 
              <!-- Projects Count -->
              <td class="py-4 px-6 text-center text-slate-700 font-semibold">
                {{ member.projectCount || 0 }}
              </td>

              <!-- Actions -->
              <td class="py-4 px-6 text-center">
                <button 
                  class="p-1.5 rounded-lg bg-slate-100 text-indigo-600 border border-slate-200 hover:bg-slate-200 transition-all"
                  aria-label="View portfolio details"
                >
                  <i class="pi pi-arrow-right text-xs"></i>
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';

const props = defineProps({
  dashboardSummary: {
    type: Object,
    required: true,
    default: () => ({
      totalSummary: {},
      personalKpiSummary: [],
      personalKpiDetail: []
    })
  }
});

const emit = defineEmits(['select-member']);

const searchQuery = ref('');
const selectedRole = ref('ALL');
const layoutMode = ref('grid');

// List of all unique roles in the dataset
const uniqueRoles = computed(() => {
  const roles = new Set();
  const list = props.dashboardSummary?.personalKpiSummary || [];
  list.forEach(m => {
    if (m.title) roles.add(m.title);
  });
  return Array.from(roles).sort();
});

// Search & Role filters
const filteredMembers = computed(() => {
  const list = props.dashboardSummary?.personalKpiSummary || [];
  const filtered = list.filter(member => {
    const matchesSearch = (member.name || '').toLowerCase().includes(searchQuery.value.toLowerCase()) ||
                          (member.title || '').toLowerCase().includes(searchQuery.value.toLowerCase()) ||
                          (member.part || '').toLowerCase().includes(searchQuery.value.toLowerCase());
    
    const matchesRole = selectedRole.value === 'ALL' || member.title === selectedRole.value;
    
    return matchesSearch && matchesRole;
  });
  
  // Sort alphabetically A-Z by employee's name
  return filtered.sort((a, b) => {
    const nameA = (a.name || '').toLowerCase();
    const nameB = (b.name || '').toLowerCase();
    return nameA.localeCompare(nameB);
  });
});

function emitSelect(member) {
  emit('select-member', member);
}

// Calculate individual member's On-Time percentage
function getMemberOnTimeRate(member) {
  const onTimeCombined = (member.onTime || 0) + (member.ahead || 0);
  const delay = member.delay || 0;
  const total = onTimeCombined + delay;
  if (total === 0) return 0;
  return Math.round((onTimeCombined / total) * 100);
}

// Calculate individual segments in stacked bar
function getTaskPercentage(member, type) {
  const onTimeCombined = (member.onTime || 0) + (member.ahead || 0);
  const delay = member.delay || 0;
  const total = onTimeCombined + delay;
  if (total === 0) return 0;
  
  if (type === 'onTime') {
    return Math.round((onTimeCombined / total) * 100);
  } else if (type === 'delay') {
    return Math.round((delay / total) * 100);
  }
  return 0;
}

// Colored indicator badge for different on-time threshold rates
function getOnTimeColorClass(rate) {
  if (rate >= 90) {
    return 'bg-emerald-950/0 text-emerald-500 border border-emerald-500/20';
  } else if (rate >= 75) {
    return 'bg-blue-950/0 text-blue-500 border border-blue-500/20';
  } else {
    return 'bg-rose-950/0 text-rose-500 border border-rose-500/20';
  }
}
</script>

<style scoped>
/* Styling focus ring styles, custom selects and animations */
select {
  background-image: none; /* Reset standard styles */
}
</style>
