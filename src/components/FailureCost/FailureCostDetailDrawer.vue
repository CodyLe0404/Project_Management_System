<template>
  <!-- Detail Drawer for Failure Cost Record -->
  <Drawer
    :visible="visible"
    position="right"
    class="!w-full sm:!w-[520px] lg:!w-[580px] p-0 shadow-2xl"
    @update:visible="$emit('update:visible', $event)"
  >
    <template #container="{ closeCallback }">
      <div v-if="record" class="h-full flex flex-col bg-white dark:bg-slate-900 text-slate-800 dark:text-slate-100">
        <!-- Drawer Header -->
        <div class="px-6 py-4 border-b border-slate-200 dark:border-slate-800 flex items-center justify-between bg-slate-50/70 dark:bg-slate-900/70">
          <div>
            <div class="flex items-center gap-2.5">
              <span class="text-xs font-mono font-bold text-indigo-600 dark:text-indigo-400 bg-indigo-50 dark:bg-indigo-950/60 px-2.5 py-1 rounded-md">
                #{{ record.id }}
              </span>
              <span
                class="px-2.5 py-0.5 rounded-full text-xs font-semibold border flex items-center gap-1.5"
                :class="getStatusBadgeStyle(record.statusName)"
              >
                <span class="w-1.5 h-1.5 rounded-full" :class="getStatusDotColor(record.statusName)"></span>
                {{ record.statusName }}
              </span>
            </div>
            <h2 class="text-lg font-bold text-slate-900 dark:text-white mt-1">
              Failure Cost Details
            </h2>
          </div>

          <Button
            icon="pi pi-times"
            text
            rounded
            severity="secondary"
            class="!w-8 !h-8"
            @click="closeCallback"
          />
        </div>

        <!-- Drawer Content Body (Scrollable) -->
        <div class="flex-1 overflow-y-auto p-6 space-y-6">
          <!-- Section 1: Error Information -->
          <div class="bg-slate-50/80 dark:bg-slate-800/40 rounded-2xl p-4 border border-slate-200/80 dark:border-slate-700/60 space-y-3">
            <h3 class="text-xs font-bold uppercase tracking-wider text-indigo-600 dark:text-indigo-400 flex items-center gap-2">
              <i class="pi pi-info-circle"></i> Error Information
            </h3>

            <div class="grid grid-cols-3 gap-3 text-xs">
              <div>
                <span class="text-slate-400 block mb-0.5">Error Date</span>
                <span class="font-bold text-slate-800 dark:text-slate-200">{{ record.errorDate }}</span>
              </div>

              <div>
                <span class="text-slate-400 block mb-0.5">Department / Team</span>
                <span
                  class="inline-block px-2 py-0.5 rounded text-[11px] font-semibold border"
                  :class="getDeptBadgeStyle(record.departmentName)"
                >
                  {{ record.departmentName }}
                </span>
              </div>

              <div>
                <span class="text-slate-400 block mb-0.5">Document No.</span>
                <span class="font-bold text-slate-800 dark:text-slate-200">{{ record.documentNo }}</span>
              </div>
            </div>
            <div class="grid grid-cols-2 gap-3 text-xs">
              <div class="col-span-2">
                <span class="text-slate-400 block mb-0.5">Project</span>
                <div class="font-semibold text-slate-900 dark:text-slate-100">
                  <span class="text-indigo-600 dark:text-indigo-400 font-bold font-mono">{{ record.projectNo }}</span>
                  <span class="text-slate-400 mx-1.5">-</span>
                  <span>{{ record.projectName }}</span>
                </div>
              </div>

              <div>
                <span class="text-slate-400 block mb-0.5">Person In Charge (PIC)</span>
                <div class="flex items-center gap-1.5 font-medium text-slate-800 dark:text-slate-200">
                  <div class="w-5 h-5 rounded-full bg-indigo-100 dark:bg-indigo-900 text-indigo-700 dark:text-indigo-300 font-bold text-[10px] flex items-center justify-center">
                    {{ record.picName?.charAt(0) || 'U' }}
                  </div>
                  <span>{{ record.picName }}</span>
                </div>
              </div>

              <div>
                <span class="text-slate-400 block mb-0.5">Checker</span>
                <div class="flex items-center gap-1.5 font-medium text-slate-800 dark:text-slate-200">
                  <div class="w-5 h-5 rounded-full bg-slate-200 dark:bg-slate-700 text-slate-700 dark:text-slate-300 font-bold text-[10px] flex items-center justify-center">
                    {{ record.checkerName?.charAt(0) || 'C' }}
                  </div>
                  <span>{{ record.checkerName }}</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Section 2: Failure Cost & Defect -->
          <div class="bg-slate-50/80 dark:bg-slate-800/40 rounded-2xl p-4 border border-slate-200/80 dark:border-slate-700/60 space-y-3">
            <h3 class="text-xs font-bold uppercase tracking-wider text-rose-600 dark:text-rose-400 flex items-center gap-2">
              <i class="pi pi-dollar"></i> Failure Cost Information
            </h3>

            <div class="grid grid-cols-2 gap-3 text-xs">
              <div>
                <span class="text-slate-400 block mb-0.5">Error Catalog</span>
                <span class="font-bold text-slate-900 dark:text-white">{{ record.errorCatalogName }}</span>
              </div>

              <div>
                <span class="text-slate-400 block mb-0.5">Quantity</span>
                <span class="font-bold text-slate-900 dark:text-white text-sm">{{ record.quantity }}</span>
              </div>

              <div class="col-span-2 bg-rose-50/50 dark:bg-rose-950/20 p-3 rounded-xl border border-rose-100 dark:border-rose-900/40 flex items-center justify-between">
                <span class="text-xs font-semibold text-rose-800 dark:text-rose-300">Failure Cost (USD)</span>
                <span class="text-xl font-extrabold text-rose-700 dark:text-rose-400 tabular-nums">
                  {{ formatCurrency(record.failureCostUSD) }}
                </span>
              </div>

              <div class="col-span-2">
                <span class="text-slate-400 block mb-1">Defect Description</span>
                <div class="p-3 bg-white dark:bg-slate-800 rounded-xl border border-slate-200 dark:border-slate-700 text-slate-800 dark:text-slate-200 leading-relaxed text-xs">
                  {{ record.defectDescription }}
                </div>
              </div>
            </div>
          </div>

          <!-- Section 3: Root Cause & Action -->
          <div class="bg-slate-50/80 dark:bg-slate-800/40 rounded-2xl p-4 border border-slate-200/80 dark:border-slate-700/60 space-y-3">
            <h3 class="text-xs font-bold uppercase tracking-wider text-amber-600 dark:text-amber-400 flex items-center gap-2">
              <i class="pi pi-cog"></i> Root Cause & Corrective Action
            </h3>

            <div class="space-y-3 text-xs">
              <div class="flex items-center justify-between">
                <span class="text-slate-400">4M Analysis</span>
                <span
                  class="px-2 py-0.5 rounded text-[11px] font-bold uppercase border"
                  :class="get4MBadgeStyle(record.analysis4MName)"
                >
                  {{ record.analysis4MName }}
                </span>
              </div>

              <div>
                <span class="text-slate-400 block mb-1 font-medium">Root Cause</span>
                <div class="p-3 bg-white dark:bg-slate-800 rounded-xl border border-slate-200 dark:border-slate-700 text-slate-800 dark:text-slate-200 text-xs">
                  {{ record.rootCause }}
                </div>
              </div>

              <div>
                <span class="text-slate-400 block mb-1 font-medium">Correction</span>
                <div class="p-3 bg-white dark:bg-slate-800 rounded-xl border border-slate-200 dark:border-slate-700 text-slate-800 dark:text-slate-200 text-xs">
                  {{ record.correction }}
                </div>
              </div>

              <div>
                <span class="text-slate-400 block mb-1 font-medium">Prevention</span>
                <div class="p-3 bg-white dark:bg-slate-800 rounded-xl border border-slate-200 dark:border-slate-700 text-slate-800 dark:text-slate-200 text-xs">
                  {{ record.prevention }}
                </div>
              </div>

              <div v-if="record.remark">
                <span class="text-slate-400 block mb-1 font-medium">Remark</span>
                <div class="p-2.5 bg-amber-50/40 dark:bg-amber-950/20 rounded-xl border border-amber-200/50 dark:border-amber-900/40 text-slate-700 dark:text-slate-300 text-xs italic">
                  {{ record.remark }}
                </div>
              </div>
            </div>
          </div>

          <!-- Timestamps -->
          <div class="text-[11px] text-slate-400 flex items-center justify-between px-1">
            <span>Created: {{ formatDate(record.createdAt) }}</span>
            <span>Updated: {{ formatDate(record.updatedAt) }}</span>
          </div>
        </div>

        <!-- Drawer Footer Actions -->
        <div class="px-6 py-4 border-t border-slate-200 dark:border-slate-800 bg-slate-50/70 dark:bg-slate-900/70 flex items-center justify-between gap-3">
          <Button
            label="Close"
            severity="secondary"
            outlined
            class="flex-1"
            @click="closeCallback"
          />
          <Button
            icon="pi pi-pen-to-square"
            label="Edit Record"
            class="flex-1 !bg-indigo-600 hover:!bg-indigo-700 !border-indigo-600"
            @click="$emit('edit', record)"
          />
        </div>
      </div>
    </template>
  </Drawer>
</template>

<script setup>
import { Drawer, Button } from 'primevue';

const props = defineProps({
  visible: {
    type: Boolean,
    default: false
  },
  record: {
    type: Object,
    default: null
  }
});

defineEmits(['update:visible', 'edit']);

function formatCurrency(val) {
  const num = Number(val) || 0;
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
    minimumFractionDigits: 2,
    maximumFractionDigits: 2
  }).format(num);
}

function formatDate(isoStr) {
  if (!isoStr) return 'N/A';
  try {
    const d = new Date(isoStr);
    return d.toLocaleString('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  } catch (e) {
    return isoStr;
  }
}

function getDeptBadgeStyle(dept) {
  switch (dept) {
    case 'Electrical Design':
      return 'bg-blue-50 text-blue-700 border-blue-200 dark:bg-blue-950/40 dark:text-blue-300 dark:border-blue-800/60';
    case 'Mechanical Design':
      return 'bg-amber-50 text-amber-700 border-amber-200 dark:bg-amber-950/40 dark:text-amber-300 dark:border-amber-800/60';
    case 'Design Planning':
      return 'bg-purple-50 text-purple-700 border-purple-200 dark:bg-purple-950/40 dark:text-purple-300 dark:border-purple-800/60';
    case 'Engineering':
      return 'bg-emerald-50 text-emerald-700 border-emerald-200 dark:bg-emerald-950/40 dark:text-emerald-300 dark:border-emerald-800/60';
    default:
      return 'bg-slate-50 text-slate-700 border-slate-200 dark:bg-slate-800 dark:text-slate-300 dark:border-slate-700';
  }
}

function get4MBadgeStyle(m) {
  switch (m) {
    case 'Man (Con người - Sai sót cá nhân, copy-paste thiếu rà soát)':
      return 'bg-indigo-50 text-indigo-700 border-indigo-200 dark:bg-indigo-950/40 dark:text-indigo-300 dark:border-indigo-800/60';
    case 'Machine (Công cụ - Lỗi do phần mềm 2D, CREO, hệ thống AI)':
      return 'bg-cyan-50 text-cyan-700 border-cyan-200 dark:bg-cyan-950/40 dark:text-cyan-300 dark:border-cyan-800/60';
    case 'Material (Vật tư - Sai spec từ khách hàng/vendor)':
      return 'bg-amber-50 text-amber-700 border-amber-200 dark:bg-amber-950/40 dark:text-amber-300 dark:border-amber-800/60';
    case 'Method (Quy trình - Thiếu cross-check, lỗi checklist FTR)':
      return 'bg-emerald-50 text-emerald-700 border-emerald-200 dark:bg-emerald-950/40 dark:text-emerald-300 dark:border-emerald-800/60';
    default:
      return 'bg-slate-50 text-slate-700 border-slate-200 dark:bg-slate-800 dark:text-slate-300 dark:border-slate-700';
  }
}

function getStatusBadgeStyle(st) {
  switch (st) {
    case 'Open':
      return 'bg-amber-50 text-amber-700 border-amber-200 dark:bg-amber-950/40 dark:text-amber-300 dark:border-amber-800/60';
    case 'Monitoring':
      return 'bg-blue-50 text-blue-700 border-blue-200 dark:bg-blue-950/40 dark:text-blue-300 dark:border-blue-800/60';
    case 'Closed':
      return 'bg-emerald-50 text-emerald-700 border-emerald-200 dark:bg-emerald-950/40 dark:text-emerald-300 dark:border-emerald-800/60';
    default:
      return 'bg-slate-100 text-slate-700 border-slate-200 dark:bg-slate-800 dark:text-slate-300 dark:border-slate-700';
  }
}

function getStatusDotColor(st) {
  switch (st) {
    case 'Open':
      return 'bg-amber-500 animate-pulse';
    case 'Monitoring':
      return 'bg-blue-500';
    case 'Closed':
      return 'bg-emerald-500';
    default:
      return 'bg-slate-400';
  }
}
</script>
