<route>
{
  meta: {
    title: "Entry",
    icon: "pi pi-pen-to-square",
    permission: ["DS_PMS_DK", "admin"],
  }
}
</route>

<template>
  <div class="min-h-screen space-y-6 pb-12 max-w-5xl mx-auto">
    <!-- Header Section -->
    <header class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-200 dark:border-slate-800 pb-4">
      <div>
        <div class="flex items-center gap-2 mb-1">
          <Button
            icon="pi pi-arrow-left"
            text
            rounded
            size="small"
            class="!w-8 !h-8 text-slate-500"
            @click="handleCancel"
          />
          <span class="text-xs font-semibold px-2.5 py-0.5 rounded-full" :class="isEditMode ? 'bg-amber-100 text-amber-800 dark:bg-amber-950 dark:text-amber-300' : 'bg-indigo-100 text-indigo-800 dark:bg-indigo-950 dark:text-indigo-300'">
            {{ isEditMode ? `Edit Mode #${recordId}` : 'Create Mode' }}
          </span>
        </div>
        <h1 class="text-2xl lg:text-3xl font-extrabold tracking-tight bg-clip-text text-transparent bg-gradient-to-r from-slate-900 via-indigo-900 to-indigo-600 dark:from-white dark:via-indigo-400 dark:to-blue-400">
          {{ isEditMode ? `Edit Failure Cost Record #${recordId}` : 'New Failure Cost Entry' }}
        </h1>
        <p class="text-xs text-slate-500 dark:text-slate-400 mt-1">
          {{ isEditMode ? 'Update defect details, financial loss calculation, and corrective actions' : 'Log a new design failure incident with 4M root cause analysis and cost impact' }}
        </p>
      </div>

      <!-- Quick Back to List -->
      <div class="flex items-center gap-2">
        <Button
          icon="pi pi-list"
          label="Back to List"
          severity="secondary"
          size="small"
          outlined
          @click="handleCancel"
        />
      </div>
    </header>

    <!-- Global Validation Alert -->
    <div
      v-if="validationErrors.length > 0"
      class="p-4 rounded-2xl bg-rose-50 dark:bg-rose-950/40 border border-rose-200 dark:border-rose-900/60 text-xs text-rose-700 dark:text-rose-300 flex items-start gap-3"
    >
      <i class="pi pi-exclamation-circle text-base text-rose-500 mt-0.5"></i>
      <div>
        <span class="font-bold block mb-1">Please correct the following before saving:</span>
        <ul class="list-disc list-inside space-y-0.5">
          <li v-for="(err, idx) in validationErrors" :key="idx">{{ err }}</li>
        </ul>
      </div>
    </div>

    <!-- Main Entry Form -->
    <form @submit.prevent="handleSubmit" class="space-y-6">
      <!-- ========================================== -->
      <!-- SECTION A: ERROR INFORMATION -->
      <!-- ========================================== -->
      <div class="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl p-6 shadow-sm space-y-4">
        <div class="flex items-center justify-between border-b border-slate-100 dark:border-slate-800 pb-3">
          <h2 class="text-sm font-bold text-slate-900 dark:text-white uppercase tracking-wider flex items-center gap-2">
            <span class="w-6 h-6 rounded-lg bg-indigo-50 dark:bg-indigo-950/60 text-indigo-600 dark:text-indigo-400 flex items-center justify-center text-xs">
              A
            </span>
            Error Information
          </h2>
          <span class="text-[11px] text-slate-400">* All fields required</span>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
          <!-- Date -->
          <div>
            <label class="block font-semibold text-slate-700 dark:text-slate-300 mb-1">
              Date <span class="text-rose-500">*</span>
            </label>
            <input
              v-model="form.errorDate"
              type="date"
              class="form-control"
              :class="hasError('errorDate') ? 'border-rose-400 ring-1 ring-rose-300' : 'border-slate-200 dark:border-slate-700'"
            />
          </div>

          <!-- Team / Department -->
          <div>
            <label class="block font-semibold text-slate-700 dark:text-slate-300 mb-1">
              Team / Department <span class="text-rose-500">*</span>
            </label>
            <select
              v-model="form.departmentId"
              class="form-control"
              :class="hasError('departmentId') ? 'border-rose-400 ring-1 ring-rose-300' : 'border-slate-200 dark:border-slate-700'"
              @change="onDepartmentChanged"
            >
              <option :value="null" disabled>-- Select Department --</option>
              <option v-for="dept in store.masterData.departments" :key="dept.departmentId" :value="dept.departmentId">
                {{ dept.departmentName }}
              </option>
            </select>
          </div>

          <!-- Project No. -->
          <div>
            <label class="block font-semibold text-slate-700 dark:text-slate-300 mb-1">
              Project No. <span class="text-rose-500">*</span>
            </label>
            <AutoComplete
              v-model="selectedProject"
              :suggestions="projectSuggestions"
              optionLabel="projectNo"
              placeholder="-- Search Project Number --"
              dropdown
              forceSelection
              class="form-control-autocomplete"
              :inputClass="getSelectionInputClass('projectId')"
              @complete="searchProjects"
              @item-select="onProjectChanged"
            >
              <template #option="slotProps">
                <div class="flex flex-col">
                  <span class="font-semibold">{{ slotProps.option.projectNo }}</span>
                  <span class="text-xs text-slate-500">{{ slotProps.option.projectName }}</span>
                </div>
              </template>
            </AutoComplete>
          </div>

          <!-- Project Name (Auto Populated) -->
          <div>
            <label class="block font-semibold text-slate-700 dark:text-slate-300 mb-1">
              Project Name <span class="text-slate-400 text-[10px]">(Auto-filled from Project No.)</span>
            </label>
            <input
              :value="selectedProjectName"
              type="text"
              readonly
              placeholder="Select Project No."
              class="form-control form-control-readonly"
            />
          </div>

          <!-- PIC Section -->
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <!-- Bên trái: PIC ID -->
            <div>
              <label class="block font-semibold text-slate-700 dark:text-slate-300 mb-1">
                Person In Charge (PIC) ID <span class="text-rose-500">*</span>
              </label>
              <AutoComplete
                v-model="selectedPic"
                :suggestions="picSuggestions"
                optionLabel="name"
                placeholder="-- Search PIC ID --"
                dropdown
                forceSelection
                class="form-control-autocomplete w-full"
                :inputClass="getSelectionInputClass('picUserId')"
                @complete="searchPicUsers"
              >
                <template #option="slotProps">
                  <div class="flex flex-col">
                    <span class="font-semibold">{{ slotProps.option.name }}</span>
                    <span class="text-xs text-slate-500">{{ slotProps.option.fullname }}</span>
                  </div>
                </template>
              </AutoComplete>
            </div>

            <!-- Bên phải: PIC Name -->
            <div>
              <label class="block font-semibold text-slate-700 dark:text-slate-300 mb-1">
                PIC Name <span class="text-slate-400 text-[10px]">(Auto-filled from PIC ID)></span>
              </label>
              <input
                :value="selectedPicFullname"
                type="text"
                readonly
                placeholder="Select PIC ID"
                class="form-control form-control-readonly"
              />
            </div>
          </div>

          <!-- Checker -->
          <div>
            <label class="block font-semibold text-slate-700 dark:text-slate-300 mb-1">
              Checker <span class="text-rose-500">*</span>
            </label>
            <input
              type="text"
              v-model="selectedChecker"
              placeholder="Enter Checker Name..."
              class="w-full form-control-autocomplete"
              :class="getSelectionInputClass('checkerUserId')"
            />
          </div>
        </div>
      </div>

      <!-- ========================================== -->
      <!-- SECTION B: FAILURE COST INFORMATION -->
      <!-- ========================================== -->
      <div class="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl p-6 shadow-sm space-y-4">
        <div class="flex items-center justify-between border-b border-slate-100 dark:border-slate-800 pb-3">
          <h2 class="text-sm font-bold text-slate-900 dark:text-white uppercase tracking-wider flex items-center gap-2">
            <span class="w-6 h-6 rounded-lg bg-rose-50 dark:bg-rose-950/60 text-rose-600 dark:text-rose-400 flex items-center justify-center text-xs">
              B
            </span>
            Failure Cost Information
          </h2>
          <span class="text-[11px] text-slate-400">Error category & cost loss</span>
        </div>

        <div class="space-y-4 text-xs">
          <!-- Error Catalog (Cascading) -->
          <div>
            <label class="block font-semibold text-slate-700 dark:text-slate-300 mb-1">
              Error Catalog <span class="text-rose-500">*</span>
              <span v-if="!form.departmentId" class="text-amber-500 font-normal ml-2">
                (Please select Team/Department first)
              </span>
            </label>
            <select
              v-model="form.errorCatalogId"
              class="w-full px-3 py-2 text-xs border rounded-xl bg-slate-50 dark:bg-slate-800 text-slate-900 dark:text-slate-100 focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 focus:outline-none transition-all"
              :class="hasError('errorCatalogId') ? 'border-rose-400 ring-1 ring-rose-300' : 'border-slate-200 dark:border-slate-700'"
              :disabled="!form.departmentId"
            >
              <option :value="null" disabled>
                {{ form.departmentId ? '-- Select Error Catalog --' : '-- Choose Department First --' }}
              </option>
              <option v-for="cat in availableCatalogs" :key="cat.errorCatalogId" :value="cat.errorCatalogId">
                {{ cat.errorName }}
              </option>
            </select>
          </div>

          <!-- Defect Description (Large Textarea) -->
          <div>
            <label class="block font-semibold text-slate-700 dark:text-slate-300 mb-1">
              Defect Description <span class="text-rose-500">*</span>
            </label>
            <textarea
              v-model="form.defectDescription"
              rows="4"
              placeholder="Describe the defect, discrepancy, or error symptom in detail..."
              class="w-full px-3 py-2 text-xs border rounded-xl bg-slate-50 dark:bg-slate-800 text-slate-900 dark:text-slate-100 focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 focus:outline-none transition-all leading-relaxed"
              :class="hasError('defectDescription') ? 'border-rose-400 ring-1 ring-rose-300' : 'border-slate-200 dark:border-slate-700'"
            ></textarea>
          </div>

          <!-- Quantity & F-Cost USD (Two Column) -->
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <!-- Quantity -->
            <div>
              <label class="block font-semibold text-slate-700 dark:text-slate-300 mb-1">
                Quantity (Q'ty) <span class="text-rose-500">*</span>
              </label>
              <input
                v-model.number="form.quantity"
                type="number"
                min="1"
                step="1"
                placeholder="1"
                class="w-full px-3 py-2 text-xs border rounded-xl bg-slate-50 dark:bg-slate-800 text-slate-900 dark:text-slate-100 focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 focus:outline-none transition-all font-bold"
                :class="hasError('quantity') ? 'border-rose-400 ring-1 ring-rose-300' : 'border-slate-200 dark:border-slate-700'"
              />
            </div>

            <!-- Failure Cost (USD) -->
            <div>
              <label class="block font-semibold text-slate-700 dark:text-slate-300 mb-1">
                Failure Cost (USD) <span class="text-rose-500">*</span>
              </label>
              <div class="relative">
                <span class="absolute left-3 top-2 font-bold text-slate-400 text-xs">$</span>
                <input
                  v-model.number="form.failureCostUSD"
                  type="number"
                  min="0"
                  step="0.01"
                  placeholder="0.00"
                  class="w-full pl-7 pr-3 py-2 text-xs border rounded-xl bg-slate-50 dark:bg-slate-800 text-slate-900 dark:text-slate-100 focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 focus:outline-none transition-all font-extrabold"
                  :class="hasError('failureCostUSD') ? 'border-rose-400 ring-1 ring-rose-300' : 'border-slate-200 dark:border-slate-700'"
                />
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- ========================================== -->
      <!-- SECTION C: ROOT CAUSE & CORRECTIVE ACTION -->
      <!-- ========================================== -->
      <div class="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl p-6 shadow-sm space-y-4">
        <div class="flex items-center justify-between border-b border-slate-100 dark:border-slate-800 pb-3">
          <h2 class="text-sm font-bold text-slate-900 dark:text-white uppercase tracking-wider flex items-center gap-2">
            <span class="w-6 h-6 rounded-lg bg-amber-50 dark:bg-amber-950/60 text-amber-600 dark:text-amber-400 flex items-center justify-center text-xs">
              C
            </span>
            Root Cause & Corrective Action
          </h2>
          <span class="text-[11px] text-slate-400">4M Analysis & Preventative Measures</span>
        </div>

        <div class="space-y-4 text-xs">
          <!-- 4M Analysis -->
          <div>
            <label class="block font-semibold text-slate-700 dark:text-slate-300 mb-1">
              4M Analysis <span class="text-rose-500">*</span>
            </label>
            <select
              v-model="form.analysis4MId"
              class="w-full px-3 py-2 text-xs border rounded-xl bg-slate-50 dark:bg-slate-800 text-slate-900 dark:text-slate-100 focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 focus:outline-none transition-all"
              :class="hasError('analysis4MId') ? 'border-rose-400 ring-1 ring-rose-300' : 'border-slate-200 dark:border-slate-700'"
            >
              <option :value="null" disabled>-- Select 4M Classification --</option>
              <option v-for="m in store.masterData.analysis4MList" :key="m.id" :value="m.id">
                {{ m.name }}
              </option>
            </select>
          </div>

          <!-- Root Cause -->
          <div>
            <label class="block font-semibold text-slate-700 dark:text-slate-300 mb-1">
              Root Cause <span class="text-rose-500">*</span>
            </label>
            <textarea
              v-model="form.rootCause"
              rows="3"
              placeholder="Why did this error occur? Fundamental breakdown analysis..."
              class="w-full px-3 py-2 text-xs border rounded-xl bg-slate-50 dark:bg-slate-800 text-slate-900 dark:text-slate-100 focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 focus:outline-none transition-all leading-relaxed"
              :class="hasError('rootCause') ? 'border-rose-400 ring-1 ring-rose-300' : 'border-slate-200 dark:border-slate-700'"
            ></textarea>
          </div>

          <!-- Correction -->
          <div>
            <label class="block font-semibold text-slate-700 dark:text-slate-300 mb-1">
              Correction (Immediate Fix) <span class="text-rose-500">*</span>
            </label>
            <textarea
              v-model="form.correction"
              rows="3"
              placeholder="What immediate actions were taken to fix the current defect?"
              class="w-full px-3 py-2 text-xs border rounded-xl bg-slate-50 dark:bg-slate-800 text-slate-900 dark:text-slate-100 focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 focus:outline-none transition-all leading-relaxed"
              :class="hasError('correction') ? 'border-rose-400 ring-1 ring-rose-300' : 'border-slate-200 dark:border-slate-700'"
            ></textarea>
          </div>

          <!-- Prevention -->
          <div>
            <label class="block font-semibold text-slate-700 dark:text-slate-300 mb-1">
              Prevention (Systemic Recurrence Prevention) <span class="text-rose-500">*</span>
            </label>
            <textarea
              v-model="form.prevention"
              rows="3"
              placeholder="What checklist, standard, template, or process change ensures this error will not happen again?"
              class="w-full px-3 py-2 text-xs border rounded-xl bg-slate-50 dark:bg-slate-800 text-slate-900 dark:text-slate-100 focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 focus:outline-none transition-all leading-relaxed"
              :class="hasError('prevention') ? 'border-rose-400 ring-1 ring-rose-300' : 'border-slate-200 dark:border-slate-700'"
            ></textarea>
          </div>

          <!-- Status & Remark (Two Column) -->
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <!-- Status -->
            <div>
              <label class="block font-semibold text-slate-700 dark:text-slate-300 mb-1">
                Status <span class="text-rose-500">*</span>
              </label>
              <select
                v-model="form.statusId"
                class="w-full px-3 py-2 text-xs border rounded-xl bg-slate-50 dark:bg-slate-800 text-slate-900 dark:text-slate-100 focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 focus:outline-none transition-all font-semibold"
                :class="hasError('statusId') ? 'border-rose-400 ring-1 ring-rose-300' : 'border-slate-200 dark:border-slate-700'"
              >
                <option v-for="st in store.masterData.statuses" :key="st.id" :value="st.id">
                  {{ st.name }}
                </option>
              </select>
            </div>

            <!-- Remark -->
            <div>
              <label class="block font-semibold text-slate-700 dark:text-slate-300 mb-1">
                Remark <span class="text-slate-400 text-[10px]">(Optional notes)</span>
              </label>
              <input
                v-model="form.remark"
                type="text"
                placeholder="Additional audit or delivery remarks..."
                class="w-full px-3 py-2 text-xs border border-slate-200 dark:border-slate-700 rounded-xl bg-slate-50 dark:bg-slate-800 text-slate-900 dark:text-slate-100 focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 focus:outline-none transition-all"
              />
            </div>
          </div>
        </div>
      </div>

      <!-- Form Bottom Actions -->
      <div class="flex items-center justify-end gap-3 pt-4 border-t border-slate-200 dark:border-slate-800">
        <Button
          type="button"
          label="Cancel"
          severity="secondary"
          outlined
          size="small"
          class="px-5"
          @click="handleCancel"
        />
        <Button
          type="submit"
          :icon="isEditMode ? 'pi pi-check' : 'pi pi-save'"
          :label="isEditMode ? 'Save Changes' : 'Save Record'"
          size="small"
          :loading="store.loading"
          class="px-6 !bg-indigo-600 hover:!bg-indigo-700 !border-indigo-600"
        />
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { AutoComplete, Button } from 'primevue';
import { useToast } from 'primevue/usetoast';

import { useFailureCostStore } from '../../stores/failureCostStore.js';

const route = useRoute();
const router = useRouter();
const store = useFailureCostStore();
console.log("Store:", store)
const toast = useToast();

const recordId = computed(() => {
  return route.query.id || route.params.id || null;
});

const isEditMode = computed(() => !!recordId.value);

// Form Reactive Model
const form = reactive({
  errorDate: new Date().toISOString().split('T')[0],
  departmentId: null,
  projectId: null,
  picUserId: null,
  checkerUserId: null,
  errorCatalogId: null,
  defectDescription: '',
  quantity: 1,
  failureCostUSD: 0,
  analysis4MId: 1, // Default 'Man'
  rootCause: '',
  correction: '',
  prevention: '',
  statusId: 1, // Default 'Open'
  remark: ''
});

const validationErrors = ref([]);
const projectSuggestions = ref([]);
const picSuggestions = ref([]);
const checkerSuggestions = ref([]);

const selectionInputBaseClass = 'form-control';

const selectedProject = computed({
  get() {
    return store.masterData.projects.find(project => project.id === Number(form.projectId)) || null;
  },
  set(project) {
    form.projectId = project?.id ?? null;
  }
});

const selectedPic = computed({
  get() {
    return store.masterData.users.find(user => user.id === Number(form.picUserId)) || null;
  },
  set(user) {
    form.picUserId = user?.id ?? null;
  }
});

const selectedChecker = computed({
  get() {
    return store.masterData.users.find(user => user.id === Number(form.checkerUserId)) || null;
  },
  set(user) {
    form.checkerUserId = user?.id ?? null;
  }
});

// Auto-fill project name when project is selected
const selectedProjectName = computed(() => {
  if (!form.projectId) return '';
  const prj = store.masterData.projects.find(p => p.id === Number(form.projectId));
  return prj ? prj.projectName : '';
});

const selectedPicFullname = computed(() => {
  if (!form.picUserId) return '';
  const user = store.masterData.users.find(u => u.id === Number(form.picUserId));
  return user ? user.fullname : '';
});

// Cascading catalogs for selected department
const availableCatalogs = computed(() => {
  if (!form.departmentId || !Array.isArray(store.masterData?.errorCatalogsByDept)) {
    return store.masterData?.allErrorCatalogs || [];
  }
  // Lọc ra các catalog thuộc departmentId đang chọn (ép về Number để so sánh an toàn)
  const filtered = store.masterData.errorCatalogsByDept.filter(
    cat => Number(cat.departmentId) === Number(form.departmentId)
  );
  return filtered.length > 0 ? filtered : [];
});

function onDepartmentChanged() {
  // If catalog is no longer valid for selected department, reset it
  if (form.errorCatalogId) {
    const valid = availableCatalogs.value.some(c => c.id === Number(form.errorCatalogId));
    if (!valid) {
      form.errorCatalogId = null;
    }
  }
}

function onProjectChanged() {
  // Project name automatically computed
}

function searchProjects(event) {
  const query = (event.query || '').trim().toLowerCase();
  projectSuggestions.value = store.masterData.projects.filter(project => {
    return !query
      || String(project.projectNo || '').toLowerCase().includes(query)
      || String(project.projectName || '').toLowerCase().includes(query);
  });
}

function searchUsers(event, suggestions) {
  const query = (event.query || '').trim().toLowerCase();
  suggestions.value = store.masterData.users.filter(user => {
    return !query
      || String(user.name || '').toLowerCase().includes(query)
      || String(user.fullname || '').toLowerCase().includes(query);
  });
}

function searchPicUsers(event) {
  searchUsers(event, picSuggestions);
}

function searchCheckerUsers(event) {
  searchUsers(event, checkerSuggestions);
}

function getSelectionInputClass(field) {
  const errorClass = hasError(field) ? 'border-rose-400 ring-1 ring-rose-300' : 'border-slate-200 dark:border-slate-700';
  return `${selectionInputBaseClass} ${errorClass}`;
}

function hasError(field) {
  return validationErrors.value.some(err => err.toLowerCase().includes(field.toLowerCase()));
}

async function loadExistingRecord() {
  if (isEditMode.value) {
    try {
      const rec = await store.fetchRecordById(recordId.value);
      if (rec) {
        form.errorDate = rec.errorDate;
        form.departmentId = rec.departmentId;
        form.projectId = rec.projectId;
        form.picUserId = rec.picUserId;
        form.checkerUserId = rec.checkerUserId;
        form.errorCatalogId = rec.errorCatalogId;
        form.defectDescription = rec.defectDescription;
        form.quantity = rec.quantity;
        form.failureCostUSD = rec.failureCostUSD;
        form.analysis4MId = rec.analysis4MId;
        form.rootCause = rec.rootCause;
        form.correction = rec.correction;
        form.prevention = rec.prevention;
        form.statusId = rec.statusId;
        form.remark = rec.remark || '';
      }
    } catch (err) {
      toast.add({
        severity: 'error',
        summary: 'Error Loading Record',
        detail: `Record #${recordId.value} could not be loaded: ${err.message}`,
        life: 4000
      });
      router.push('/02_Fcost/fcostList');
    }
  }
}

onMounted(async () => {
  await store.fetchMasterData();
  await loadExistingRecord();
});

watch(
  () => recordId.value,
  async () => {
    await loadExistingRecord();
  }
);

function validateForm() {
  const errors = [];

  if (!form.errorDate) errors.push('Date is required');
  if (!form.departmentId) errors.push('Team / Department is required');
  if (!form.projectId) errors.push('Project No. is required');
  if (!form.picUserId) errors.push('PIC is required');
  if (!form.checkerUserId) errors.push('Checker is required');
  if (!form.errorCatalogId) errors.push('Error Catalog is required');
  if (!form.defectDescription || !form.defectDescription.trim()) errors.push('Defect Description cannot be empty');
  if (!form.quantity || form.quantity <= 0) errors.push('Quantity must be greater than 0');
  if (form.failureCostUSD === null || form.failureCostUSD === undefined || form.failureCostUSD < 0) {
    errors.push('Failure Cost (USD) must be greater than or equal to 0');
  }
  if (!form.analysis4MId) errors.push('4M Analysis is required');
  if (!form.rootCause || !form.rootCause.trim()) errors.push('Root Cause cannot be empty');
  if (!form.correction || !form.correction.trim()) errors.push('Correction cannot be empty');
  if (!form.prevention || !form.prevention.trim()) errors.push('Prevention cannot be empty');
  if (!form.statusId) errors.push('Status is required');

  validationErrors.value = errors;
  return errors.length === 0;
}

async function handleSubmit() {
  if (!validateForm()) {
    toast.add({
      severity: 'warn',
      summary: 'Validation Warning',
      detail: 'Please check required fields marked above',
      life: 3500
    });
    return;
  }

  try {
    if (isEditMode.value) {
      await store.updateRecord(recordId.value, form);
      toast.add({
        severity: 'success',
        summary: 'Record Updated',
        detail: `Failure Cost #${recordId.value} updated successfully`,
        life: 3000
      });
    } else {
      const created = await store.createRecord(form);
      toast.add({
        severity: 'success',
        summary: 'Record Created',
        detail: `New Failure Cost #${created.id} saved successfully`,
        life: 3000
      });
    }

    // Return to list after successful save
    router.push('/02_Fcost/fcostList');
  } catch (err) {
    toast.add({
      severity: 'error',
      summary: 'Save Failed',
      detail: err.message || 'An error occurred while saving',
      life: 4000
    });
  }
}

function handleCancel() {
  router.push('/02_Fcost/fcostList');
}
</script>

<style scoped>
.form-control {
  width: 100%;
  height: 34px;
  padding: 8px 12px;
  border-width: 1px;
  border-style: solid;
  border-radius: 12px;
  background-color: rgb(248 250 252);
  color: rgb(15 23 42);
  font-family: inherit;
  font-size: 12px;
  font-weight: 400;
  line-height: 16px;
  outline: none;
  transition: all 150ms ease;
}

.form-control:focus {
  border-color: rgb(99 102 241);
  box-shadow: 0 0 0 2px rgb(99 102 241 / 0.2);
}

.form-control-readonly {
  background-color: rgb(241 245 249);
  color: rgb(71 85 105);
  cursor: not-allowed;
}

.form-control-autocomplete {
  display: flex;
  width: 100%;
  height: 34px;
}

:deep(.form-control-autocomplete .p-autocomplete-input) {
  min-width: 0;
  height: 34px;
  padding: 8px 12px;
  border-width: 1px;
  border-style: solid;
  border-radius: 12px 0 0 12px;
  background-color: rgb(248 250 252);
  color: rgb(15 23 42);
  font-family: inherit;
  font-size: 12px;
  font-weight: 400;
  line-height: 16px;
  outline: none;
  transition: all 150ms ease;
}

:deep(.form-control-autocomplete .p-autocomplete-input:focus) {
  border-color: rgb(99 102 241);
  box-shadow: 0 0 0 2px rgb(99 102 241 / 0.2);
}

:deep(.form-control-autocomplete .p-autocomplete-dropdown) {
  width: 34px;
  height: 34px;
  padding: 0;
  border-width: 1px;
  border-style: solid;
  border-left-width: 0;
  border-radius: 0 12px 12px 0;
  background-color: rgb(248 250 252);
  color: rgb(71 85 105);
}

.dark .form-control,
.dark :deep(.form-control-autocomplete .p-autocomplete-input),
.dark :deep(.form-control-autocomplete .p-autocomplete-dropdown) {
  background-color: rgb(30 41 59);
  color: rgb(248 250 252);
}

.dark .form-control-readonly {
  background-color: rgb(30 41 59 / 0.6);
  color: rgb(203 213 225);
}

h1 {
  font-size: 1.875rem !important;
  line-height: 2.25rem !important;
}
</style>
