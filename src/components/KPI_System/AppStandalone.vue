<template>
  <div class="min-h-screen bg-slate-50 text-slate-900 p-4 md:p-8">
    <div class="max-w-7xl mx-auto space-y-8 relative">
      <!-- Decorative background blur -->
      <div class="absolute top-0 left-1/4 w-96 h-96 bg-primary-500/10 rounded-full blur-3xl pointer-events-none"></div>
      <div class="absolute top-10 right-1/4 w-96 h-96 bg-indigo-500/10 rounded-full blur-3xl pointer-events-none"></div>

      <!-- Header Section -->
      <header class="relative flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-slate-200 pb-6">
        <div>
          <div class="flex items-center gap-2 text-indigo-600 font-semibold text-xs tracking-wider uppercase mb-1">
            <i class="pi pi-chart-bar"></i>
            Performance & Analytics Dashboard
          </div>
          <h1 class="text-3xl font-extrabold tracking-tight bg-clip-text text-transparent bg-gradient-to-r from-slate-50 via-indigo-100 to-indigo-400">
            Personal KPI & Project Tracking
          </h1>
          <p class="text-xs text-slate-600 mt-1">
            Real-time tracking of member KPI statuses, task distribution ratio, and project allocations.
          </p>
        </div>

        <div class="flex items-center gap-2 text-xs">
          <span class="px-3 py-1.5 rounded-lg bg-white border border-slate-200 text-slate-700 font-medium">
            Vue 3 Composition API
          </span>
          <span class="px-3 py-1.5 rounded-lg bg-indigo-100/40 border border-indigo-200 text-indigo-600 font-medium">
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
          <p class="text-xs text-slate-600">Select any member card below to explore their active project portfolios.</p>
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
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { mockMembers } from './mockData.js';
import DashboardOverview from './DashboardOverview.vue';
import MemberList from './MemberList.vue';
import MemberDetailModal from './MemberDetailModal.vue';

// Core State
const members = ref(mockMembers);
const isModalOpen = ref(false);
const selectedMember = ref(mockMembers[0] || {});

// Modal Controller
function openMemberModal(member) {
  selectedMember.value = member;
  isModalOpen.value = true;
}

function closeMemberModal() {
  isModalOpen.value = false;
}
</script>

<style>
/* Base stylesheet rules for standalone integration */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
@import url('https://cdn.jsdelivr.net/npm/primeicons@7.0.0/primeicons.css');

body {
  font-family: 'Inter', sans-serif;
  background-color: #f8fafc; /* bg-slate-50 */
}
</style>
