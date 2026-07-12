<route>
{
  meta: {
    title: "KPI Cá Nhân",
    icon: "pi pi-user",
    permission: ["DS_PMS_PK"],
  }
}
</route>

<template>
  <div class="min-h-screen bg-slate-50 text-slate-900 p-4 md:p-8 space-y-8 rounded-3xl border border-slate-200 shadow-2xl overflow-hidden relative">
    <!-- Top Decorative Glow -->
    <div class="absolute top-0 left-1/4 w-96 h-96 bg-primary-500/10 rounded-full blur-3xl pointer-events-none"></div>
    <div class="absolute top-10 right-1/4 w-96 h-96 bg-indigo-500/10 rounded-full blur-3xl pointer-events-none"></div>

    <!-- Header Section -->
    <header class="relative flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-slate-200 pb-6">
      <div>
        <div class="flex items-center gap-2 text-indigo-600 font-semibold text-xs tracking-wider uppercase mb-1">
          <i class="pi pi-chart-bar"></i>
          Performance & Analytics
        </div>
        <h1 class="text-3xl font-extrabold tracking-tight bg-clip-text text-transparent bg-gradient-to-r from-indigo-900 via-purple-700 to-blue-400">
          Personal KPI & Project Tracking
        </h1>
        <p class="text-xs text-slate-600 mt-1">
          Real-time member status tracking, task metrics distribution, and portfolio management.
        </p>
      </div>

      <!-- Quick Action Summary Badges -->
      <div class="flex items-center gap-2 text-xs">
        <span class="px-3 py-1.5 rounded-lg bg-white border border-slate-200 text-slate-700 font-medium">
          Vue 3 Composition API
        </span>
        <span class="px-3 py-1.5 rounded-lg bg-indigo-950/40 border border-indigo-500/30 text-indigo-400 font-medium">
          Tailwind CSS Styled
        </span>
      </div>
    </header>

    <!-- KPI Summary Cards & Status Registry -->
    <section class="relative z-10">
      <DashboardOverview :members="members" />
    </section>

    <!-- Member Directory with Grid/Table Views -->
    <section class="space-y-4 relative z-10">
      <div>
        <h3 class="text-lg font-bold text-slate-900">Team Member Registry</h3>
        <p class="text-xs text-slate-600">Select any team member card or table row below to explore their active project portfolios.</p>
      </div>
      <MemberList 
        :members="members" 
        @select-member="openMemberModal" 
      />
    </section>

    <!-- Member Detail Modal -->
    <MemberDetailModal 
      :is-open="isModalOpen" 
      :member="selectedMember" 
      @close="closeMemberModal" 
    />
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { mockMembers } from '../../components/KPI_System/mockData.js';
import DashboardOverview from '../../components/KPI_System/DashboardOverview.vue';
import MemberList from '../../components/KPI_System/MemberList.vue';
import MemberDetailModal from '../../components/KPI_System/MemberDetailModal.vue';

// 1. Core State
const members = ref(mockMembers);
const isModalOpen = ref(false);
const selectedMember = ref(mockMembers[0] || {});

// 2. Modal Controller
function openMemberModal(member) {
  selectedMember.value = member;
  isModalOpen.value = true;
}

function closeMemberModal() {
  isModalOpen.value = false;
}
</script>

<style scoped>
/* Scoped overrides to enforce high visual contrast */
h1 {
  font-size: 1.875rem !important; /* Resets default layouts styles size */
  line-height: 2.25rem !important;
}
</style>
