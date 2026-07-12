<template>
  <!-- Sub-Navigation / Tab System -->
  <nav class="relative z-10 flex flex-wrap border-b border-slate-200 dark:border-slate-800 gap-1 p-1 bg-slate-100/60 dark:bg-slate-900/60 backdrop-blur-md rounded-xl max-w-2xl">
    <button 
      v-for="tab in tabs" 
      :key="tab.id"
      @click="$emit('tab-change', tab.id)"
      class="flex items-center gap-2 px-4 py-2 text-sm font-medium rounded-lg transition-all duration-300"
      :class="[
        activeTab === tab.id 
          ? 'bg-white dark:bg-slate-800 text-indigo-600 dark:text-indigo-400 shadow-sm border border-slate-200/50 dark:border-slate-700/50 scale-[1.02]' 
          : 'text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-200 hover:bg-slate-50 dark:hover:bg-slate-800/40'
      ]"
    >
      <i :class="tab.icon"></i>
      {{ tab.name }}
    </button>
  </nav>
</template>

<script setup>
defineProps({
  activeTab: {
    type: String,
    required: true
  }
});

defineEmits(['tab-change']);

const tabs = [
  { id: 'Global', name: 'Global Overview', icon: 'pi pi-globe' },
  { id: 'Electrical', name: 'Electrical', icon: 'pi pi-bolt' },
  { id: 'Mechanical', name: 'Mechanical', icon: 'pi pi-cog' },
  { id: 'Planning', name: 'Planning', icon: 'pi pi-calendar' }
];
</script>
