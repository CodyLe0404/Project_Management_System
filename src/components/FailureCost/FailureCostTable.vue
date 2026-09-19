<template>
  <div class="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl shadow-sm overflow-hidden flex flex-col">
    <!-- Table Header Toolbar -->
    <div class="p-4 sm:p-5 border-b border-slate-200 dark:border-slate-800 flex flex-col sm:flex-row sm:items-center justify-between gap-3 bg-slate-50/50 dark:bg-slate-900/50">
      <div class="flex items-center gap-3">
        <h3 class="font-bold text-base text-slate-800 dark:text-slate-200">
          {{ title }}
        </h3>
        <span class="px-2.5 py-0.5 rounded-full text-xs font-semibold bg-slate-200/80 dark:bg-slate-800 text-slate-700 dark:text-slate-300">
          {{ totalRecords }} records
        </span>
      </div>

      <div class="flex items-center gap-3">
        <!-- Page size selector -->
        <div class="flex items-center gap-2 text-xs text-slate-500">
          <span>Show</span>
          <select
            :value="pageSize"
            class="px-2 py-1 border border-slate-200 dark:border-slate-700 rounded-lg bg-white dark:bg-slate-800 text-xs text-slate-700 dark:text-slate-300 focus:outline-none focus:ring-1 focus:ring-indigo-500"
            @change="$emit('update:pageSize', Number($event.target.value))"
          >
            <option :value="5">5</option>
            <option :value="10">10</option>
            <option :value="20">20</option>
            <option :value="50">50</option>
          </select>
          <span>per page</span>
        </div>

        <slot name="actions" />
      </div>
    </div>

    <!-- Table Body -->
    <div class="overflow-x-auto relative">
      <!-- Loading Overlay -->
      <div
        v-if="loading"
        class="absolute inset-0 bg-white/70 dark:bg-slate-900/70 backdrop-blur-[1px] flex items-center justify-center z-20"
      >
        <div class="flex items-center gap-2 text-indigo-600 dark:text-indigo-400 font-semibold text-xs">
          <i class="pi pi-spin pi-spinner text-base"></i>
          Loading failure costs...
        </div>
      </div>

      <table class="w-full text-left border-collapse">
        <thead>
          <tr class="bg-slate-50 dark:bg-slate-900/80 text-slate-500 dark:text-slate-400 font-semibold text-xs border-b border-slate-200 dark:border-slate-800">
            <th class="px-4 py-3.5 w-12 text-center">No.</th>
            <th class="px-4 py-3.5 whitespace-nowrap">Date</th>
            <th class="px-4 py-3.5 whitespace-nowrap">Team</th>
            <th class="px-4 py-3.5 min-w-[200px]">Project</th>
            <th class="px-4 py-3.5 whitespace-nowrap">PIC</th>
            <th class="px-4 py-3.5 whitespace-nowrap">Error Catalog</th>
            <th class="px-4 py-3.5 text-center whitespace-nowrap">Qty</th>
            <th class="px-4 py-3.5 text-right whitespace-nowrap">F-Cost (USD)</th>
            <th class="px-4 py-3.5 text-center whitespace-nowrap">4M</th>
            <th class="px-4 py-3.5 text-center whitespace-nowrap">Status</th>
            <th class="px-4 py-3.5 text-center w-28 whitespace-nowrap">Action</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-slate-100 dark:divide-slate-800/80 text-xs">
          <!-- Empty State -->
          <tr v-if="!loading && records.length === 0">
            <td colspan="11" class="px-6 py-12 text-center text-slate-500 dark:text-slate-400">
              <div class="flex flex-col items-center justify-center gap-2">
                <div class="w-12 h-12 rounded-full bg-slate-100 dark:bg-slate-800 flex items-center justify-center text-slate-400">
                  <i class="pi pi-inbox text-xl"></i>
                </div>
                <span class="font-semibold text-sm text-slate-700 dark:text-slate-300">No failure cost records found.</span>
                <span class="text-xs text-slate-400">Try adjusting your search criteria or add a new record.</span>
              </div>
            </td>
          </tr>

          <!-- Data Rows -->
          <tr
            v-for="(record, index) in records"
            :key="record.id"
            class="hover:bg-indigo-50/30 dark:hover:bg-slate-800/50 cursor-pointer transition-colors"
            @click="$emit('row-click', record)"
          >
            <!-- Sequential No -->
            <td class="px-4 py-3 text-center text-slate-400 font-mono">
              {{ (currentPage - 1) * pageSize + index + 1 }}
            </td>

            <!-- Date -->
            <td class="px-4 py-3 whitespace-nowrap font-medium text-slate-700 dark:text-slate-300">
              {{ record.errorDate }}
            </td>

            <!-- Team / Department -->
            <td class="px-4 py-3 whitespace-nowrap">
              <span
                class="px-2 py-0.5 rounded-md text-[11px] font-semibold border"
                :class="getDeptBadgeStyle(record.departmentName)"
              >
                {{ record.departmentName }}
              </span>
            </td>

            <!-- Project -->
            <td class="px-4 py-3 font-medium text-slate-800 dark:text-slate-200">
              <div class="truncate max-w-xs" :title="`${record.projectNo} - ${record.projectName}`">
                <span class="font-bold text-indigo-600 dark:text-indigo-400">{{ record.projectNo }}</span>
                <span class="text-slate-400 mx-1">-</span>
                <span class="text-slate-700 dark:text-slate-300">{{ record.projectName }}</span>
              </div>
            </td>

            <!-- PIC -->
            <td class="px-4 py-3 whitespace-nowrap text-slate-600 dark:text-slate-400">
              <div class="flex items-center gap-1.5">
                <div class="w-5 h-5 rounded-full bg-slate-200 dark:bg-slate-700 text-[10px] font-bold flex items-center justify-center text-slate-600 dark:text-slate-300">
                  {{ record.picName?.charAt(0) || 'U' }}
                </div>
                <span>{{ record.picName }}</span>
              </div>
            </td>

            <!-- Error Catalog -->
            <td class="px-4 py-3 whitespace-nowrap text-slate-700 dark:text-slate-300 font-medium">
              {{ record.errorCatalogName }}
            </td>

            <!-- Qty -->
            <td class="px-4 py-3 text-center font-bold text-slate-800 dark:text-slate-200">
              {{ record.quantity }}
            </td>

            <!-- F-Cost (USD) -->
            <td class="px-4 py-3 text-right font-extrabold text-slate-900 dark:text-slate-100 tabular-nums">
              {{ formatCurrency(record.failureCostUSD) }}
            </td>

            <!-- 4M Analysis -->
            <td class="px-4 py-3 text-center whitespace-nowrap">
              <span
                class="px-2 py-0.5 rounded text-[10px] font-bold tracking-wide uppercase border"
                :class="get4MBadgeStyle(record.analysis4MName)"
              >
                {{ record.analysis4MName }}
              </span>
            </td>

            <!-- Status -->
            <td class="px-4 py-3 text-center whitespace-nowrap">
              <span
                class="px-2.5 py-0.5 rounded-full text-[11px] font-semibold border flex items-center justify-center gap-1 w-fit mx-auto"
                :class="getStatusBadgeStyle(record.statusName)"
              >
                <span class="w-1.5 h-1.5 rounded-full" :class="getStatusDotColor(record.statusName)"></span>
                {{ record.statusName }}
              </span>
            </td>

            <!-- Actions -->
            <td class="px-4 py-3 text-center whitespace-nowrap" @click.stop>
              <div class="flex items-center justify-center gap-1">
                <Button
                  icon="pi pi-eye"
                  text
                  rounded
                  size="small"
                  title="View Details"
                  severity="secondary"
                  class="!w-7 !h-7"
                  @click="$emit('view-detail', record)"
                />
                <Button
                  icon="pi pi-pencil"
                  text
                  rounded
                  size="small"
                  title="Edit Record"
                  severity="info"
                  class="!w-7 !h-7"
                  @click="$emit('edit-record', record)"
                />
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Table Footer / Pagination -->
    <div
      v-if="totalRecords > 0"
      class="p-4 border-t border-slate-200 dark:border-slate-800 flex flex-col sm:flex-row sm:items-center justify-between gap-3 bg-slate-50/50 dark:bg-slate-900/50 text-xs text-slate-500"
    >
      <div>
        Showing
        <span class="font-bold text-slate-700 dark:text-slate-300">{{ (currentPage - 1) * pageSize + 1 }}</span>
        to
        <span class="font-bold text-slate-700 dark:text-slate-300">{{ Math.min(currentPage * pageSize, totalRecords) }}</span>
        of
        <span class="font-bold text-slate-700 dark:text-slate-300">{{ totalRecords }}</span>
        entries
      </div>

      <div class="flex items-center gap-1">
        <Button
          icon="pi pi-angle-double-left"
          text
          size="small"
          :disabled="currentPage <= 1"
          @click="$emit('update:currentPage', 1)"
        />
        <Button
          icon="pi pi-angle-left"
          text
          size="small"
          :disabled="currentPage <= 1"
          @click="$emit('update:currentPage', currentPage - 1)"
        />

        <span class="px-3 py-1 font-semibold text-slate-700 dark:text-slate-300">
          Page {{ currentPage }} of {{ totalPages }}
        </span>

        <Button
          icon="pi pi-angle-right"
          text
          size="small"
          :disabled="currentPage >= totalPages"
          @click="$emit('update:currentPage', currentPage + 1)"
        />
        <Button
          icon="pi pi-angle-double-right"
          text
          size="small"
          :disabled="currentPage >= totalPages"
          @click="$emit('update:currentPage', totalPages)"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';
import { Button } from 'primevue';

const props = defineProps({
  title: {
    type: String,
    default: 'Failure Cost Records'
  },
  records: {
    type: Array,
    default: () => []
  },
  totalRecords: {
    type: Number,
    default: 0
  },
  currentPage: {
    type: Number,
    default: 1
  },
  pageSize: {
    type: Number,
    default: 10
  },
  totalPages: {
    type: Number,
    default: 1
  },
  loading: {
    type: Boolean,
    default: false
  }
});

defineEmits([
  'update:currentPage',
  'update:pageSize',
  'row-click',
  'view-detail',
  'edit-record'
]);

function formatCurrency(val) {
  const num = Number(val) || 0;
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
    minimumFractionDigits: 2,
    maximumFractionDigits: 2
  }).format(num);
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
    case 'Man':
      return 'bg-indigo-50 text-indigo-700 border-indigo-200 dark:bg-indigo-950/40 dark:text-indigo-300 dark:border-indigo-800/60';
    case 'Machine':
      return 'bg-cyan-50 text-cyan-700 border-cyan-200 dark:bg-cyan-950/40 dark:text-cyan-300 dark:border-cyan-800/60';
    case 'Material':
      return 'bg-amber-50 text-amber-700 border-amber-200 dark:bg-amber-950/40 dark:text-amber-300 dark:border-amber-800/60';
    case 'Method':
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
