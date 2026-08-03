<template>
  <Transition name="modal-fade">
    <div 
      v-if="isOpen" 
      class="fixed inset-0 z-50 flex items-center justify-center p-4 overflow-y-auto"
      @keydown.escape="closeModal"
    >
      <!-- Backdrop with blur -->
      <div 
        class="fixed inset-0 bg-slate-50/80 backdrop-blur-sm transition-opacity" 
        @click="closeModal"
      ></div>

      <!-- Modal Card -->
      <div 
        class="relative w-[98vw] max-w-[1800px] bg-white border border-slate-200 rounded-3xl overflow-hidden shadow-2xl transition-all duration-300 transform scale-100 flex flex-col max-h-[85vh]"
        role="dialog"
        aria-modal="true"
      >
        <!-- Header background decoration -->
        <div class="absolute inset-x-0 top-0 h-32 bg-gradient-to-r from-primary-500/10 to-indigo-500/10 pointer-events-none"></div>

        <!-- Close Button -->
        <button 
          @click="closeModal"
          class="absolute top-4 right-4 p-2 rounded-full bg-slate-100 hover:bg-slate-200 border border-slate-200 text-slate-600 hover:text-slate-900 transition-colors z-10"
          aria-label="Close modal"
        >
          <i class="pi pi-times text-sm"></i>
        </button>

        <!-- Scrollable Content container -->
        <div class="flex-1 overflow-y-auto p-6 md:p-8 space-y-6 pt-12">
          <!-- Member Profile Header -->
          <div class="flex flex-col sm:flex-row items-center justify-between gap-4 text-center sm:text-left relative border-b border-slate-100 pb-5">
            <div>
              <h2 class="text-2xl font-extrabold text-slate-900 flex items-center gap-2 justify-center sm:justify-start">
                {{ member.name }}
                <span class="w-2.5 h-2.5 bg-emerald-500 rounded-full border border-white" title="Active"></span>
              </h2>
              <p class="text-indigo-600 font-semibold text-sm mt-1">{{ member.title }} — {{ member.part }}</p>
            </div>
            
            <div class="flex items-center justify-center">
              <span class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-bold bg-emerald-50 text-emerald-700 border border-emerald-200">
                <span class="w-1.5 h-1.5 rounded-full bg-emerald-400"></span>
                On-Time Rate: {{ onTimePercentage }}%
              </span>
            </div>
          </div>

          <!-- Top Section (KPI Summary) -->
          <div class="grid grid-cols-2 sm:grid-cols-4 gap-4">
            <div class="bg-slate-50 border border-slate-200 rounded-xl p-3.5 text-center">
              <span class="block text-[10px] font-semibold text-slate-500 uppercase tracking-wider">Total Projects</span>
              <span class="text-lg font-extrabold text-slate-900 mt-1 block">{{ member.projectCount || 0 }}</span>
            </div>
            <div class="bg-slate-50 border border-slate-200 rounded-xl p-3.5 text-center">
              <span class="block text-[10px] font-semibold text-slate-500 uppercase tracking-wider">Main Tasks</span>
              <span class="text-lg font-extrabold text-slate-900 mt-1 block">{{ member.mainTasksCount || 0 }}</span>
            </div>
            <div class="bg-slate-50 border border-slate-200 rounded-xl p-3.5 text-center">
              <span class="block text-[10px] font-semibold text-slate-500 uppercase tracking-wider">Subtasks</span>
              <span class="text-lg font-extrabold text-slate-900 mt-1 block">{{ member.subTasksCount || 0 }}</span>
            </div>
            <div class="bg-emerald-50 border border-emerald-200 rounded-xl p-3.5 text-center">
              <span class="block text-[10px] font-semibold text-emerald-700 uppercase tracking-wider">On Time</span>
              <span class="text-lg font-extrabold text-emerald-800 mt-1 block">{{ (member.onTime || 0) + (member.ahead || 0) }}</span>
            </div>
            
            <div class="bg-blue-50 border border-blue-200 rounded-xl p-3.5 text-center">
              <span class="block text-[10px] font-semibold text-blue-700 uppercase tracking-wider">Doing</span>
              <span class="text-lg font-extrabold text-blue-800 mt-1 block">{{ member.doing || 0 }}</span>
            </div>
            <div class="bg-rose-50 border border-rose-200 rounded-xl p-3.5 text-center">
              <span class="block text-[10px] font-semibold text-rose-700 uppercase tracking-wider">Delayed</span>
              <span class="text-lg font-extrabold text-rose-800 mt-1 block">{{ member.delay || 0 }}</span>
            </div>
            <div class="bg-purple-50 border border-purple-200 rounded-xl p-3.5 text-center">
              <span class="block text-[10px] font-semibold text-purple-700 uppercase tracking-wider">No Plan</span>
              <span class="text-lg font-extrabold text-purple-800 mt-1 block">{{ member.noPlan || 0 }}</span>
            </div>
            <div class="bg-slate-100 border border-slate-200 rounded-xl p-3.5 text-center">
              <span class="block text-[10px] font-semibold text-slate-600 uppercase tracking-wider">Not Yet Started</span>
              <span class="text-lg font-extrabold text-slate-800 mt-1 block">{{ member.notYetStart || 0 }}</span>
            </div>
          </div>

          <!-- Bottom Section (KPI Detail Table) -->
          <div class="space-y-4">
            <div class="flex items-center justify-between">
              <h3 class="text-base font-bold text-slate-900">Task Performance Details</h3>
              <span class="text-xs text-slate-500 font-semibold">Total Items: {{ filteredDetails.length }}</span>
            </div>
            
            <div 
              v-if="filteredDetails.length > 0" 
              class="border border-slate-200 bg-white rounded-2xl overflow-hidden shadow-sm"
            >
              <div class="overflow-x-auto">
                <table class="min-w-max w-full table-auto border-collapse text-left">
                  <thead>
                    <tr class="border-b border-slate-200 bg-slate-50 text-[10px] font-bold text-slate-600 uppercase tracking-wider">
                      <th class="py-3 px-4">Project ID & Name</th>
                      <th class="py-3 px-4">Main Task</th>
                      <th class="py-3 px-4">Sub Task</th>
                      <th class="py-3 px-4 text-center">Progress</th>
                      <th class="py-3 px-4 text-center">Status</th>
                      <th class="py-3 px-4 text-right">Budget</th>
                      <th class="py-3 px-4 text-right">Actual Cost</th>
                    </tr>
                  </thead>
                  <tbody class="divide-y divide-slate-100 text-xs">
                    <tr 
                      v-for="detail in filteredDetails" 
                      :key="detail.id_item"
                      class="hover:bg-slate-50 transition-colors"
                    >
                      <!-- Project ID & Name -->
                      <td class="py-3 px-4">
                        <div class="font-bold text-slate-900">#{{ detail.project_id }}</div>
                        <div class="text-[10px] text-slate-500 truncate max-w-[200px]" :title="detail.project_name">
                          {{ detail.project_name }}
                        </div>
                      </td>
                      
                      <!-- Main Task -->
                      <td class="py-3 px-4 font-semibold text-slate-700">
                        {{ detail.main_task }}
                      </td>
                      
                      <!-- Sub Task -->
                      <td class="py-3 px-4 text-slate-600 font-medium">
                        {{ detail.sub_task }}
                      </td>
                      
                      <!-- Progress -->
                      <td class="py-3 px-4">
                        <div class="flex items-center gap-2 justify-center">
                          <div class="w-16 bg-slate-100 rounded-full h-1.5 border border-slate-200">
                            <div 
                              class="bg-indigo-600 h-1.5 rounded-full" 
                              :style="{ width: `${detail.progress}%` }"
                            ></div>
                          </div>
                          <span class="font-bold text-slate-700 text-[10px] w-8">{{ detail.progress }}%</span>
                        </div>
                      </td>
                      
                      <!-- Status -->
                      <td class="py-3 px-4 text-center">
                        <span 
                          class="px-2.5 py-0.5 rounded-full text-[10px] font-bold border"
                          :class="getProjectStatusStyles(detail.status)"
                        >
                          {{ detail.status }}
                        </span>
                      </td>
                      
                      <!-- Budget -->
                      <td class="py-3 px-4 text-right font-mono text-slate-700 font-medium">
                        {{ formatCurrency(detail.budget) }}
                      </td>
                      
                      <!-- Actual Cost -->
                      <td class="py-3 px-4 text-right font-mono text-slate-700 font-medium">
                        {{ formatCurrency(detail.actual_cost) }}
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
            
            <div 
              v-else 
              class="bg-slate-50 border border-slate-200 rounded-2xl p-8 text-center text-slate-500 text-sm"
            >
              <i class="pi pi-inbox text-3xl mb-2 block"></i>
              No detailed task information found for this employee.
            </div>
          </div>
        </div>

        <!-- Footer -->
        <div class="p-6 border-t border-slate-200 bg-slate-50 flex justify-end gap-3">
          <button 
            @click="closeModal" 
            class="px-5 py-2 text-sm font-semibold bg-slate-100 text-slate-900 hover:bg-slate-200 hover:text-slate-950 rounded-xl transition-all"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  </Transition>
</template>

<script setup>
import { computed, onMounted, onUnmounted } from 'vue';

const props = defineProps({
  isOpen: {
    type: Boolean,
    required: true,
  },
  member: {
    type: Object,
    required: true,
  },
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

const emit = defineEmits(['close']);

function closeModal() {
  emit('close');
}

// Esc key binding
const handleKeydown = (e) => {
  if (e.key === 'Escape') {
    closeModal();
  }
};

onMounted(() => {
  document.addEventListener('keydown', handleKeydown);
});

onUnmounted(() => {
  document.removeEventListener('keydown', handleKeydown);
});

// Calculate individual member's On-Time percentage (ahead combined into onTime)
const onTimePercentage = computed(() => {
  if (!props.member) return 0;
  const onTime = props.member.onTime || 0;
  const ahead = props.member.ahead || 0;
  const delay = props.member.delay || 0;
  const total = onTime + ahead + delay;
  if (total === 0) return 0;
  return Math.round(((onTime + ahead) / total) * 100);
});

// Filter details by assignee === userId or id
const filteredDetails = computed(() => {
  if (!props.member) return [];
  const userId = props.member.userId;
  const id = props.member.id;
  const list = props.dashboardSummary?.personalKpiDetail || [];
  return list.filter(detail => {
    return (userId && detail.assignee === userId) || (id && detail.assignee === id);
  });
});

// Format monetary values
function formatCurrency(val) {
  if (val === undefined || val === null) return '-';
  const num = parseFloat(val);
  if (isNaN(num)) return val;
  return new Intl.NumberFormat('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 }).format(num);
}

// Custom badges styling
function getProjectStatusStyles(status) {
  const s = (status || '').toLowerCase();
  if (s === 'on time' || s === 'ahead' || s === 'ahead of schedule') {
    return 'bg-emerald-50 text-emerald-700 border border-emerald-200 dark:bg-emerald-950/40 dark:text-emerald-400 dark:border-emerald-800/50';
  } else if (s === 'doing' || s === 'in progress') {
    return 'bg-amber-50 text-amber-700 border border-amber-200 dark:bg-amber-950/40 dark:text-amber-400 dark:border-amber-800/50';
  } else if (s === 'delay' || s === 'delayed') {
    return 'bg-rose-50 text-rose-700 border border-rose-200 dark:bg-rose-950/40 dark:text-rose-400 dark:border-rose-800/50';
  } else if (s === 'not yet start' || s === 'not started') {
    return 'bg-slate-50 text-slate-600 border border-slate-200 dark:bg-slate-900 dark:text-slate-400 dark:border-slate-800';
  } else if (s === 'no plan') {
    return 'bg-purple-50 text-purple-700 border border-purple-200 dark:bg-purple-950/40 dark:text-purple-400 dark:border-purple-800/50';
  } else {
    return 'bg-slate-50 text-slate-600 border border-slate-200 dark:bg-slate-900 dark:text-slate-400 dark:border-slate-800';
  }
}
</script>

<style scoped>
/* Modal transition animations */
.modal-fade-enter-active,
.modal-fade-leave-active {
  transition: opacity 0.25s ease;
}

.modal-fade-enter-from,
.modal-fade-leave-to {
  opacity: 0;
}

.modal-fade-enter-active .relative.w-full {
  transition: transform 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.modal-fade-leave-active .relative.w-full {
  transition: transform 0.2s ease-in;
}

.modal-fade-enter-from .relative.w-full,
.modal-fade-leave-to .relative.w-full {
  transform: scale(0.9) translateY(10px);
}
</style>
