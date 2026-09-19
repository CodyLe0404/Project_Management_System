<template>
  <div class="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl p-5 shadow-sm space-y-4">
    <!-- Header & Toggle for Filters -->
    <div class="flex items-center justify-between">
      <div class="flex items-center gap-2">
        <i class="pi pi-filter text-indigo-600 dark:text-indigo-400"></i>
        <h3 class="font-bold text-sm text-slate-800 dark:text-slate-200">
          {{ title }}
        </h3>
        <span v-if="activeFilterCount > 0" class="px-2 py-0.5 rounded-full text-[11px] font-bold bg-indigo-100 text-indigo-700 dark:bg-indigo-950 dark:text-indigo-300">
          {{ activeFilterCount }} active
        </span>
      </div>
      <div class="flex items-center gap-2">
        <Button
          v-if="showCollapseToggle"
          :icon="isExpanded ? 'pi pi-chevron-up' : 'pi pi-chevron-down'"
          :label="isExpanded ? 'Less Filters' : 'More Filters'"
          text
          size="small"
          @click="isExpanded = !isExpanded"
        />
        <Button
          icon="pi pi-refresh"
          label="Reset"
          severity="secondary"
          text
          size="small"
          @click="handleReset"
        />
        <Button
          icon="pi pi-search"
          :label="applyLabel"
          size="small"
          @click="handleApply"
        />
      </div>
    </div>

    <!-- Main Filter Controls Grid -->
    <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-3">
      <!-- Keyword Search (if enabled) -->
      <div v-if="showKeyword" class="sm:col-span-2">
        <label class="block text-xs font-semibold text-slate-600 dark:text-slate-400 mb-1">
          Search Keyword
        </label>
        <div class="relative">
          <i class="pi pi-search absolute left-3 top-2.5 text-xs text-slate-400"></i>
          <input
            v-model="localFilter.keyword"
            type="text"
            placeholder="Search project, description, PIC, root cause..."
            class="w-full pl-8 pr-3 py-1.5 text-xs border border-slate-200 dark:border-slate-700 rounded-xl bg-slate-50 dark:bg-slate-800 text-slate-800 dark:text-slate-200 focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 focus:outline-none"
            @keyup.enter="handleApply"
          />
        </div>
      </div>

      <!-- Department / Team -->
      <div>
        <label class="block text-xs font-semibold text-slate-600 dark:text-slate-400 mb-1">
          Department / Team
        </label>
        <select
          v-model="localFilter.departmentId"
          class="w-full px-3 py-1.5 text-xs border border-slate-200 dark:border-slate-700 rounded-xl bg-slate-50 dark:bg-slate-800 text-slate-800 dark:text-slate-200 focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 focus:outline-none"
          @change="onDepartmentChange"
        >
          <option :value="null">All Departments</option>
          <option v-for="dept in departments" :key="dept.departmentId" :value="dept.departmentId">
            {{ dept.departmentName }}
          </option>
        </select>
      </div>

      <!-- Status -->
      <div>
        <label class="block text-xs font-semibold text-slate-600 dark:text-slate-400 mb-1">
          Status
        </label>
        <select
          v-model="localFilter.statusId"
          class="w-full px-3 py-1.5 text-xs border border-slate-200 dark:border-slate-700 rounded-xl bg-slate-50 dark:bg-slate-800 text-slate-800 dark:text-slate-200 focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 focus:outline-none"
        >
          <option :value="null">All Statuses</option>
          <option v-for="st in statuses" :key="st.id" :value="st.id">
            {{ st.name }}
          </option>
        </select>
      </div>

      <!-- From Date -->
      <div>
        <label class="block text-xs font-semibold text-slate-600 dark:text-slate-400 mb-1">
          From Date
        </label>
        <input
          v-model="localFilter.fromDate"
          type="date"
          class="w-full px-3 py-1.5 text-xs border border-slate-200 dark:border-slate-700 rounded-xl bg-slate-50 dark:bg-slate-800 text-slate-800 dark:text-slate-200 focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 focus:outline-none"
        />
      </div>

      <!-- To Date -->
      <div>
        <label class="block text-xs font-semibold text-slate-600 dark:text-slate-400 mb-1">
          To Date
        </label>
        <input
          v-model="localFilter.toDate"
          type="date"
          class="w-full px-3 py-1.5 text-xs border border-slate-200 dark:border-slate-700 rounded-xl bg-slate-50 dark:bg-slate-800 text-slate-800 dark:text-slate-200 focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 focus:outline-none"
        />
      </div>

      <!-- Project -->
      <div>
        <label class="block text-xs font-semibold text-slate-600 dark:text-slate-400 mb-1">
          Project
        </label>
        <select
          v-model="localFilter.projectId"
          class="w-full px-3 py-1.5 text-xs border border-slate-200 dark:border-slate-700 rounded-xl bg-slate-50 dark:bg-slate-800 text-slate-800 dark:text-slate-200 focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 focus:outline-none"
        >
          <option :value="null">All Projects</option>
          <option v-for="prj in projects" :key="prj.id" :value="prj.id">
            {{ prj.projectNo }} - {{ prj.projectName }}
          </option>
        </select>
      </div>

      <!-- Error Catalog (cascades based on Department) -->
      <div>
        <label class="block text-xs font-semibold text-slate-600 dark:text-slate-400 mb-1">
          Error Catalog
        </label>
        <select
          v-model="localFilter.errorCatalogId"
          class="w-full px-3 py-1.5 text-xs border border-slate-200 dark:border-slate-700 rounded-xl bg-slate-50 dark:bg-slate-800 text-slate-800 dark:text-slate-200 focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 focus:outline-none"
        >
          <option :value="null">All Catalogs</option>
          <option v-for="cat in availableCatalogs" :key="cat.errorCatalogId" :value="cat.errorCatalogId">
            {{ cat.errorName }}
          </option>
        </select>
      </div>
    </div>

    <!-- Secondary / Expanded Filters Row -->
    <div v-show="isExpanded || !showCollapseToggle" class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-3 pt-2 border-t border-slate-100 dark:border-slate-800">
      <!-- PIC -->
      <div>
        <label class="block text-xs font-semibold text-slate-600 dark:text-slate-400 mb-1">
          Person In Charge (PIC)
        </label>
        <select
          v-model="localFilter.picUserId"
          class="w-full px-3 py-1.5 text-xs border border-slate-200 dark:border-slate-700 rounded-xl bg-slate-50 dark:bg-slate-800 text-slate-800 dark:text-slate-200 focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 focus:outline-none"
        >
          <option :value="null">All PICs</option>
          <option v-for="u in users" :key="u.id" :value="u.id">
            {{ u.name }} - {{ u.fullname }}
          </option>
        </select>
      </div>

      <!-- Checker (if enabled) -->
      <!-- <div v-if="showChecker">
        <label class="block text-xs font-semibold text-slate-600 dark:text-slate-400 mb-1">
          Checker
        </label>
        <select
          v-model="localFilter.checkerUserId"
          class="w-full px-3 py-1.5 text-xs border border-slate-200 dark:border-slate-700 rounded-xl bg-slate-50 dark:bg-slate-800 text-slate-800 dark:text-slate-200 focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 focus:outline-none"
        >
          <option :value="null">All Checkers</option>
          <option v-for="u in users" :key="u.id" :value="u.id">
            {{ u.name }} ({{ u.departmentName }})
          </option>
        </select>
      </div> -->

      <!-- 4M Analysis -->
      <div>
        <label class="block text-xs font-semibold text-slate-600 dark:text-slate-400 mb-1">
          4M Analysis
        </label>
        <select
          v-model="localFilter.analysis4MId"
          class="w-full px-3 py-1.5 text-xs border border-slate-200 dark:border-slate-700 rounded-xl bg-slate-50 dark:bg-slate-800 text-slate-800 dark:text-slate-200 focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 focus:outline-none"
        >
          <option :value="null">All 4M Categories</option>
          <option v-for="m in analysis4MList" :key="m.analysis4MId" :value="m.analysis4MId">
            {{ m.name }}
          </option>
        </select>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, reactive, watch } from 'vue';
import { Button } from 'primevue';

const props = defineProps({
  title: {
    type: String,
    default: 'Filter Records'
  },
  applyLabel: {
    type: String,
    default: 'Apply Filter'
  },
  showKeyword: {
    type: Boolean,
    default: true
  },
  showChecker: {
    type: Boolean,
    default: true
  },
  showCollapseToggle: {
    type: Boolean,
    default: true
  },
  initialFilter: {
    type: Object,
    default: () => ({})
  },
  masterData: {
    type: Object,
    required: true,
    default: () => ({
      departments: [],
      errorCatalogsByDept: {},
      allErrorCatalogs: [],
      analysis4MList: [],
      statuses: [],
      projects: [],
      users: []
    })
  }
});

const emit = defineEmits(['apply', 'reset']);

const isExpanded = ref(false);

const localFilter = reactive({
  fromDate: props.initialFilter?.fromDate || '',
  toDate: props.initialFilter?.toDate || '',
  departmentId: props.initialFilter?.departmentId ?? null,
  projectId: props.initialFilter?.projectId ?? null,
  picUserId: props.initialFilter?.picUserId ?? null,
  checkerUserId: props.initialFilter?.checkerUserId ?? null,
  errorCatalogId: props.initialFilter?.errorCatalogId ?? null,
  analysis4MId: props.initialFilter?.analysis4MId ?? null,
  statusId: props.initialFilter?.statusId ?? null,
  keyword: props.initialFilter?.keyword || ''
});

// Shorthand computed props from masterData
const departments = computed(() => props.masterData?.departments || []);
const projects = computed(() => props.masterData?.projects || []);
const users = computed(() => props.masterData?.users || []);
const statuses = computed(() => props.masterData?.statuses || []);
const analysis4MList = computed(() => props.masterData?.analysis4MList || []);

// Cascading catalogs based on selected department
const availableCatalogs = computed(() => {
  if (localFilter.departmentId && props.masterData?.errorCatalogsByDept?.[localFilter.departmentId]) {
    return props.masterData.errorCatalogsByDept[localFilter.departmentId];
  }
  return props.masterData?.allErrorCatalogs || [];
});

function onDepartmentChange() {
  // If catalog belongs to a different department, reset it
  if (localFilter.errorCatalogId) {
    const valid = availableCatalogs.value.some(c => c.errorCatalogId === Number(localFilter.errorCatalogId));
    if (!valid) {
      localFilter.errorCatalogId = null;
    }
  }
}

const activeFilterCount = computed(() => {
  let count = 0;
  if (localFilter.fromDate) count++;
  if (localFilter.toDate) count++;
  if (localFilter.departmentId) count++;
  if (localFilter.projectId) count++;
  if (localFilter.picUserId) count++;
  if (localFilter.checkerUserId) count++;
  if (localFilter.errorCatalogId) count++;
  if (localFilter.analysis4MId) count++;
  if (localFilter.statusId) count++;
  if (localFilter.keyword && localFilter.keyword.trim()) count++;
  return count;
});

function handleApply() {
  emit('apply', { ...localFilter });
}

function handleReset() {
  localFilter.fromDate = '';
  localFilter.toDate = '';
  localFilter.departmentId = null;
  localFilter.projectId = null;
  localFilter.picUserId = null;
  localFilter.checkerUserId = null;
  localFilter.errorCatalogId = null;
  localFilter.analysis4MId = null;
  localFilter.statusId = null;
  localFilter.keyword = '';
  emit('reset');
}

// Watch initial filter changes (e.g. from store)
watch(
  () => props.initialFilter,
  (newVal) => {
    if (newVal) {
      Object.assign(localFilter, newVal);
    }
  },
  { deep: true }
);
</script>
