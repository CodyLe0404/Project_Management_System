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
        class="relative w-full max-w-2xl bg-white border border-slate-200 rounded-3xl overflow-hidden shadow-2xl transition-all duration-300 transform scale-100 flex flex-col max-h-[85vh]"
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
          <div class="flex flex-col sm:flex-row items-center gap-4 text-center sm:text-left relative">
            <div class="relative group">
              <!-- Avatar circle -->
              <img 
                v-if="member.avatar" 
                :src="member.avatar" 
                :alt="member.name"
                class="w-20 h-20 rounded-2xl object-cover border border-slate-700 shadow-md group-hover:scale-105 transition-transform duration-300"
              />
              <div 
                v-else 
                class="w-20 h-20 rounded-2xl bg-indigo-600 flex items-center justify-center text-white font-bold text-2xl shadow-md border border-slate-700"
              >
                {{ member.name.substring(0, 2).toUpperCase() }}
              </div>
              <span class="absolute -bottom-1 -right-1 w-4 h-4 bg-emerald-500 rounded-full border-2 border-slate-900" title="Active"></span>
            </div>

            <div>
              <h2 class="text-2xl font-bold text-slate-900">{{ member.name }}</h2>
              <p class="text-indigo-600 font-medium text-sm mt-0.5">{{ member.role }}</p>
              <div class="mt-2 flex flex-wrap gap-2 justify-center sm:justify-start">
                <span class="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-xs font-semibold bg-emerald-500/10 text-emerald-700 border border-emerald-500/20">
                  <span class="w-1.5 h-1.5 rounded-full bg-emerald-400"></span>
                  On-Time Rate: {{ onTimePercentage }}%
                </span>
              </div>
            </div>
          </div>

          <!-- Stats Segment -->
          <div class="grid grid-cols-2 sm:grid-cols-4 gap-4">
            <div class="bg-slate-50 border border-slate-200 rounded-xl p-3.5 text-center">
              <span class="block text-xs text-slate-600">Main Tasks</span>
              <span class="text-xl font-bold text-slate-900">{{ member.mainTasksCount || 0 }}</span>
            </div>
            <div class="bg-slate-50 border border-slate-200 rounded-xl p-3.5 text-center">
              <span class="block text-xs text-slate-600">Sub Tasks</span>
              <span class="text-xl font-bold text-slate-900">{{ member.subTasksCount || 0 }}</span>
            </div>
            <div class="bg-emerald-500/10 border border-emerald-500/20 rounded-xl p-3.5 text-center">
              <span class="block text-xs text-emerald-400">Ahead</span>
              <span class="text-xl font-bold text-emerald-300">{{ member.aheadOfSchedule || 0 }}</span>
            </div>
            <div class="bg-rose-500/10 border border-rose-500/20 rounded-xl p-3.5 text-center">
              <span class="block text-xs text-rose-400">Delayed</span>
              <span class="text-xl font-bold text-rose-300">{{ member.delayed || 0 }}</span>
            </div>
          </div>

          <!-- Project Registry List -->
          <div>
            <div class="flex items-center justify-between mb-4">
              <h3 class="text-base font-bold text-slate-200">Allocated Project Portfolios</h3>
              <span class="text-xs text-slate-400">Total Assigned: {{ member.projects?.length || 0 }}</span>
            </div>
            
            <div 
              v-if="member.projects && member.projects.length > 0" 
              class="divide-y divide-slate-200 bg-slate-50 border border-slate-200 rounded-2xl overflow-hidden"
            >
              <div 
                v-for="project in member.projects" 
                :key="project.projectName"
                class="flex items-center justify-between p-4 hover:bg-slate-800/20 transition-colors"
              >
                <div class="flex items-center gap-3">
                  <div class="p-2 rounded-lg bg-indigo-500/10 text-indigo-600">
                    <i class="pi pi-folder text-sm"></i>
                  </div>
                  <span class="text-sm font-medium text-slate-900">{{ project.projectName }}</span>
                </div>
                <!-- Status Badge with custom coloring matching requested specifications -->
                <span 
                  class="px-3 py-1 rounded-full text-xs font-semibold border"
                  :class="getProjectStatusStyles(project.projectStatus)"
                >
                  {{ project.projectStatus }}
                </span>
              </div>
            </div>
            
            <div 
              v-else 
              class="bg-slate-50 border border-slate-200 rounded-2xl p-8 text-center text-slate-600 text-sm"
            >
              <i class="pi pi-inbox text-3xl mb-2 block"></i>
              No active projects assigned to this member.
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
import { computed } from 'vue';

const props = defineProps({
  isOpen: {
    type: Boolean,
    required: true,
  },
  member: {
    type: Object,
    required: true,
  }
});

const emit = defineEmits(['close']);

function closeModal() {
  emit('close');
}

// Custom badges styling according to specs
// - 'Ahead of schedule': Dark Green
// - 'On Time': Blue
// - 'Doing': Yellow
// - 'Not yet start': Light Gray
// - 'No plan': Purple
// - 'Delay': Red
function getProjectStatusStyles(status) {
  switch (status) {
    case 'Ahead of schedule':
      return 'bg-emerald-100 text-emerald-700 border-emerald-300';
    case 'On Time':
      return 'bg-blue-100 text-blue-700 border-blue-300';
    case 'Doing':
      return 'bg-amber-100 text-amber-700 border-amber-300';
    case 'Not yet start':
      return 'bg-slate-100 text-slate-700 border-slate-200';
    case 'No plan':
      return 'bg-purple-100 text-purple-700 border-purple-300';
    case 'Delay':
      return 'bg-rose-100 text-rose-700 border-rose-300';
    default:
      return 'bg-slate-100 text-slate-700 border-slate-200';
  }
}

// Calculate individual member's On-Time percentage
const onTimePercentage = computed(() => {
  if (!props.member) return 0;
  const onTime = props.member.onTime || 0;
  const ahead = props.member.aheadOfSchedule || 0;
  const delayed = props.member.delayed || 0;
  const total = onTime + ahead + delayed;
  if (total === 0) return 0;
  return Math.round(((onTime + ahead) / total) * 100);
});
</script>

<script>
// Expose functions for esc key bind
export default {
  mounted() {
    document.addEventListener('keydown', this.handleKeydown);
  },
  unmounted() {
    document.removeEventListener('keydown', this.handleKeydown);
  },
  methods: {
    handleKeydown(e) {
      if (e.key === 'Escape') {
        this.$emit('close');
      }
    }
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
