<route>
{
  meta: {
    title: "Kế Hoạch Theo Ngày",
    icon: "pi pi-calendar-clock",
    permission: ["DS_PMS_PI"],
  }
}
</route>

<template>
  <div class="project-page">
    <section class="table-card">
      <!-- Top Sticky Toolbar -->
      <div class="toolbar">
        <!-- Date Picker Filter Control -->
        <div class="date-filter-box">
          <div class="date-filter-title">
            <i class="pi pi-calendar-clock text-blue-600"></i>
            <span class="font-semibold text-sm text-gray-700">Plan End Date:</span>
          </div>

          <div class="date-controls">
            <button
              type="button"
              class="date-step-btn"
              title="Previous Day"
              @click="goToPrevDay"
            >
              <i class="pi pi-chevron-left"></i>
            </button>

            <DatePicker
              v-model="selectedDate"
              dateFormat="yy-mm-dd"
              showIcon
              iconDisplay="input"
              placeholder="YYYY-MM-DD"
              class="date-input-field"
              showButtonBar
            />

            <button
              type="button"
              class="date-step-btn"
              title="Next Day"
              @click="goToNextDay"
            >
              <i class="pi pi-chevron-right"></i>
            </button>

            <button
              type="button"
              class="quick-pill-btn"
              :class="{ active: isToday }"
              @click="goToToday"
            >
              <i class="pi pi-clock text-xs"></i>
              Today
            </button>

            <button
              type="button"
              class="quick-pill-btn"
              :class="{ active: !selectedDate }"
              @click="clearDateFilter"
            >
              All Dates
            </button>
          </div>
        </div>

        <!-- Search Inputs Group -->
        <div class="toolbar-search-group">
          <div class="toolbar-search-wrap">
            <input
              ref="searchInput"
              v-model="searchQuery"
              type="text"
              placeholder="Search Project..."
              class="search-input"
            />
          </div>

          <div class="toolbar-search-wrap">
            <input
              ref="taskInput"
              v-model="taskQuery"
              type="text"
              placeholder="Search Task / Task No..."
              class="search-input"
            />
          </div>

          <div class="toolbar-search-wrap">
            <input
              ref="assigneeInput"
              v-model="assigneeQuery"
              type="text"
              placeholder="Search Assignee..."
              class="search-input"
            />
          </div>
        </div>

        <!-- Action Buttons -->
        <div class="toolbar-action-group">
          <button
            type="button"
            class="refresh-btn"
            :disabled="isLoading"
            title="Reload project data from server"
            @click="reloadProjectData"
          >
            <i class="pi pi-refresh" :class="{ 'pi-spin': isLoading }"></i>
            <span>{{ isLoading ? 'LOADING...' : 'REFRESH' }}</span>
          </button>

          <button
            type="button"
            @click="calculateAndSave"
            class="save-btn"
            :disabled="isSaving"
          >
            <i class="pi pi-save"></i>
            <span>{{ isSaving ? 'SAVING...' : 'CALCULATE & SAVE' }}</span>
          </button>
        </div>
      </div>

      <!-- KPI Summary Ribbon & Header -->
      <div class="card-header header-with-toggle">
        <div class="header-left">
          <div class="title-row">
            <h2>📅 Kế Hoạch Theo Ngày</h2>
            <span class="active-date-badge">
              <i class="pi pi-filter"></i>
              {{ activeDateLabel }}
            </span>
          </div>
          <p class="subtitle">
            Hiển thị các dự án và hạng mục công việc có ngày kết thúc theo kế hoạch (Plan End) khớp với ngày được chọn.
          </p>

          <!-- KPI Metrics Chips -->
          <div class="kpi-ribbon">
            <div class="kpi-chip chip-total">
              <span class="kpi-label">Projects:</span>
              <span class="kpi-num">{{ dateStats.totalProjects }}</span>
            </div>
            <div class="kpi-chip chip-tasks">
              <span class="kpi-label">Tasks Due:</span>
              <span class="kpi-num">{{ dateStats.totalTasks }}</span>
            </div>
            <div class="kpi-chip chip-completed">
              <span class="kpi-label">Done:</span>
              <span class="kpi-num">{{ dateStats.completed }}</span>
            </div>
            <div class="kpi-chip chip-doing">
              <span class="kpi-label">Doing:</span>
              <span class="kpi-num">{{ dateStats.inProgress }}</span>
            </div>
            <div class="kpi-chip chip-delay" :class="{ 'has-delay': dateStats.delay > 0 }">
              <span class="kpi-label">Delay:</span>
              <span class="kpi-num">{{ dateStats.delay }}</span>
            </div>
          </div>
        </div>

        <!-- View Switcher (Project Summary / Task Summary / Full Detail) -->
        <div class="view-switcher-wrapper">
          <div class="view-switcher">
            <button
              type="button"
              :class="{ active: viewMode === VIEW_MODES.PROJECT }"
              @click="setViewMode(VIEW_MODES.PROJECT)"
            >
              Project Summary
            </button>
            <button
              type="button"
              :class="{ active: viewMode === VIEW_MODES.TASK }"
              @click="setViewMode(VIEW_MODES.TASK)"
            >
              Task Summary
            </button>
            <button
              type="button"
              :class="{ active: viewMode === VIEW_MODES.FULL }"
              @click="setViewMode(VIEW_MODES.FULL)"
            >
              Full Detail
            </button>
          </div>
        </div>
      </div>

      <!-- Empty state notification when no tasks match current date filter -->
      <div v-if="dateStats.totalTasks === 0 && !isLoading" class="empty-date-banner">
        <div class="empty-content">
          <i class="pi pi-info-circle empty-icon"></i>
          <div>
            <div class="empty-title">Không tìm thấy công việc nào có Plan End vào ngày {{ activeDateLabel }}</div>
            <div class="empty-desc">Bạn có thể chọn một ngày khác từ Date Picker trên thanh công cụ hoặc bấm xem tất cả các ngày.</div>
          </div>
        </div>
        <button type="button" class="empty-reset-btn" @click="clearDateFilter">
          <i class="pi pi-calendar-plus"></i>
          Xem tất cả công việc (All Dates)
        </button>
      </div>

      <!-- Handsontable Container -->
      <div
        ref="hotContainer"
        class="hot-wrapper ht-theme-main"
      />
    </section>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount, toRaw, watch } from 'vue'

import Handsontable from 'handsontable'
import { useToast } from 'primevue/usetoast'
import DatePicker from 'primevue/datepicker'

import 'handsontable/styles/handsontable.css'
import 'handsontable/styles/ht-theme-main.css'

import { registerAllModules } from 'handsontable/registry'

import {
  getProjectsDetails,
  saveProjectItems,
  saveHeaderItems,
  deleteProjectRowData,
  insertProjectRowData
} from '../../services/projectService'

import { useAuthStore } from '../../stores/auth'

registerAllModules()

const authStore = useAuthStore()
const toast = useToast()

// DOM & Handsontable references
const hotContainer = ref(null)
let hot = null

// Data State
const tableData = ref([])
const rawRows = ref([])
const isSaving = ref(false)
const isLoading = ref(false)

// Search filters
const searchInput = ref(null)
const taskInput = ref(null)
const assigneeInput = ref(null)
const searchQuery = ref('')
const taskQuery = ref('')
const assigneeQuery = ref('')

// View Modes
const VIEW_MODES = {
  PROJECT: 'project-summary',
  TASK: 'task-summary',
  FULL: 'full-detail'
}
const viewMode = ref(VIEW_MODES.FULL)
const setViewMode = (mode) => {
  viewMode.value = mode
}

// ==========================================
// Date Filter Helpers & State Management
// ==========================================

function getTodayDate() {
  const now = new Date()
  now.setHours(0, 0, 0, 0)
  return now
}

function toDateString(val) {
  if (!val) return ''
  if (val instanceof Date) {
    if (isNaN(val.getTime())) return ''
    const year = val.getFullYear()
    const month = String(val.getMonth() + 1).padStart(2, '0')
    const day = String(val.getDate()).padStart(2, '0')
    return `${year}-${month}-${day}`
  }
  const str = String(val).trim()
  const match = str.match(/^(\d{4})-(\d{2})-(\d{2})/)
  if (match) {
    return `${match[1]}-${match[2]}-${match[3]}`
  }
  const d = new Date(str)
  if (!isNaN(d.getTime())) {
    const year = d.getFullYear()
    const month = String(d.getMonth() + 1).padStart(2, '0')
    const day = String(d.getDate()).padStart(2, '0')
    return `${year}-${month}-${day}`
  }
  return ''
}

// Selected date starts at today's current date (Requirements 2 & 3)
const selectedDate = ref(getTodayDate())

const selectedDateString = computed(() => {
  return selectedDate.value ? toDateString(selectedDate.value) : ''
})

const isToday = computed(() => {
  return selectedDateString.value === toDateString(getTodayDate())
})

const activeDateLabel = computed(() => {
  if (!selectedDateString.value) return 'Tất cả các ngày'
  if (isToday.value) {
    return `${selectedDateString.value} (Hôm nay)`
  }
  return selectedDateString.value
})

const confirmDiscardChanges = () => {
  if (changedRows.size > 0 || insertedRowsToSave.length > 0 || deletedItemIds.length > 0) {
    return window.confirm('Bạn có thay đổi chưa lưu. Bạn có muốn chuyển ngày và hủy các thay đổi này?')
  }
  return true
}

const goToToday = () => {
  if (!confirmDiscardChanges()) return
  selectedDate.value = getTodayDate()
}

const goToPrevDay = () => {
  if (!confirmDiscardChanges()) return
  const current = selectedDate.value ? new Date(selectedDate.value) : getTodayDate()
  current.setDate(current.getDate() - 1)
  current.setHours(0, 0, 0, 0)
  selectedDate.value = current
}

const goToNextDay = () => {
  if (!confirmDiscardChanges()) return
  const current = selectedDate.value ? new Date(selectedDate.value) : getTodayDate()
  current.setDate(current.getDate() + 1)
  current.setHours(0, 0, 0, 0)
  selectedDate.value = current
}

const clearDateFilter = () => {
  if (!confirmDiscardChanges()) return
  selectedDate.value = null
}

// KPI Statistics for the selected date
const dateStats = computed(() => {
  const targetDate = selectedDateString.value
  const rows = targetDate
    ? rawRows.value.filter(r => r.id_item && toDateString(r.plan_end) === targetDate)
    : rawRows.value.filter(r => r.id_item)

  const projectIds = new Set(rows.map(r => r.project_id).filter(Boolean))
  const totalTasks = rows.length

  let completed = 0
  let delay = 0
  let inProgress = 0
  let notStarted = 0

  rows.forEach(r => {
    const status = getTaskStatus(r)
    if (status === 'On Time') {
      completed++
    } else if (status === 'Delay') {
      delay++
    } else if (status === 'Doing') {
      inProgress++
    } else {
      notStarted++
    }
  })

  return {
    totalProjects: projectIds.size,
    totalTasks,
    completed,
    inProgress,
    delay,
    notStarted
  }
})

// ==========================================
// Tracking & Modification Sets
// ==========================================
const changedRows = new Set()
const modifiedHeaderRows = new Set()
let deletedItemIds = []
let insertedRowsToSave = []
const insertedRowMap = new Map()

const getDeleteCount = () => new Set(deletedItemIds).size
const hasDeletePermission = () => authStore.hasPermission('DS_PMS_PI_M')

const showDeletePermissionWarning = () => {
  toast.add({
    severity: 'warn',
    summary: 'Permission denied',
    detail: 'You do not have permission to delete this project row.',
    life: 4000
  })
}

const confirmDeleteRows = (count) => {
  const message = count > 1
    ? `Bạn đang thực hiện xóa ${count} rows. Continue?`
    : 'Bạn đang thực hiện xóa 1 row. Continue?'

  return window.confirm(message)
}

const buildUpdatedPayload = () => {
  const source = tableData.value.filter(
    row => !row.is_header && row.id_item && changedRows.has(row.id_item)
  )

  return source.map(row => ({
    item_id: row.id_item,
    main_task: row.main_task || '',
    sub_task: row.sub_task || '',
    qty: row.qty || 0,
    user_id: authStore.user?.userId,
    assignee: row.assignee || null,
    process: getRowProcess(row) || 0,
    status: getTaskStatus(row) || '',
    plan_start: row.plan_start || null,
    plan_end: row.plan_end || null,
    actual_start: row.actual_start || null,
    actual_end: row.actual_end || null,
    actual_cost: row.actual_cost === '' ? null : Number(row.actual_cost),
    remark: row.remark || ''
  }))
}

const buildHeaderUpdate = () => {
  const payload = []

  for (const headerRow of modifiedHeaderRows) {
    payload.push({
      project_id: headerRow.project_id || '',
      task_no: headerRow.task_no || '',
      main_task: headerRow.main_task || '',
      qty: headerRow.qty || 0,
      budget: headerRow.budget || 0,
      actual_cost: headerRow.actual_cost === '' ? null : Number(headerRow.actual_cost),
      user_id: authStore.user?.userId
    })
  }

  return payload
}

// ==========================================
// Save & Load Functions
// ==========================================

const calculateAndSave = async () => {
  if (isSaving.value || !hot) return

  const hasDeletes = deletedItemIds.length > 0
  const hasInserts = insertedRowsToSave.length > 0
  const hasUpdates = changedRows.size > 0
  const headerHasChanges = Array.from(modifiedHeaderRows).length > 0

  if (hasDeletes && !hasDeletePermission()) {
    showDeletePermissionWarning()
    return
  }

  if (!hasDeletes && !hasInserts && !hasUpdates && !headerHasChanges) {
    alert('Saved successfully (No changes detected)')
    return
  }

  try {
    isSaving.value = true

    if (hasDeletes) {
      const deleteCount = getDeleteCount()
      const confirmed = confirmDeleteRows(deleteCount)
      if (!confirmed) {
        return
      }

      const removeRows = deletedItemIds.join(',')
      if (deletedItemIds.length >= 500) {
        alert('⚠️ Quá nhiều dữ liệu được xóa cùng lúc. Vui lòng xóa dữ liệu theo từng nhóm nhỏ hơn 500 rows!')
        return
      } else {
        await deleteProjectRowData(removeRows, authStore.user?.userId)
      }
    }

    if (hasInserts) {
      await insertProjectRowData(insertedRowsToSave)
    }

    if (hasUpdates) {
      const payload = buildUpdatedPayload()
      if (payload.length) {
        await saveProjectItems(payload)
      }
    }

    if (headerHasChanges) {
      const payload = buildHeaderUpdate()
      const resultUpdateHeader = await saveHeaderItems(payload)
      if (!resultUpdateHeader.success) {
        alert(resultUpdateHeader.message || 'Cập nhật thất bại!')
        return
      }
    }

    alert('Saved successfully')
    changedRows.clear()
    modifiedHeaderRows.clear()
    deletedItemIds = []
    insertedRowsToSave = []
    insertedRowMap.clear()

    await fetchProjectData()
  } catch (error) {
    console.error(error)
    alert('Save failed: ' + (error.message || 'Unknown error'))
  } finally {
    isSaving.value = false
  }
}

const fetchProjectData = async () => {
  await loadData()
}

const reloadProjectData = async () => {
  if (!confirmDiscardChanges()) return
  await loadData()
}

// Rebuild hierarchy and table data based on selected date
const rebuildTableData = () => {
  const targetDate = selectedDateString.value

  // Filter raw rows by Plan End date if a date is selected
  const filteredRaw = targetDate
    ? rawRows.value.filter(row => toDateString(row.plan_end) === targetDate)
    : rawRows.value

  tableData.value = buildProjectHierarchy(filteredRaw)

  changedRows.clear()
  modifiedHeaderRows.clear()
  deletedItemIds = []
  insertedRowsToSave = []
  insertedRowMap.clear()

  if (hot) {
    hot.loadData(toRaw(getDisplayedRows()))
  }
}

const loadData = async () => {
  try {
    isLoading.value = true
    const rawData = await getProjectsDetails(authStore.user?.userId)

    if (rawData) {
      rawData.forEach(row => {
        if (row.id_item) {
          row._original_plan_start = row.plan_start
          row._original_plan_end = row.plan_end
        }
      })
    }

    rawRows.value = rawData || []
    rebuildTableData()

    initOrUpdateHandsontable()
  } catch (error) {
    console.error('Failed to load project details:', error)
  } finally {
    isLoading.value = false
  }
}

function initOrUpdateHandsontable() {
  if (!hotContainer.value) return

  const projectNameWidth = getAutoFitColumnWidth(rawRows.value, 'project_name')
  const mainTaskWidth = getAutoFitColumnWidth(rawRows.value, 'main_task')
  const subtaskWidth = getAutoFitColumnWidth(rawRows.value, 'sub_task')
  const asssigneeWidth = getAutoFitColumnWidth(rawRows.value, 'assignee')
  const planStartWidth = getAutoFitColumnWidth(rawRows.value, 'plan_start')
  const planEndWidth = getAutoFitColumnWidth(rawRows.value, 'plan_end')
  const actualStartWidth = getAutoFitColumnWidth(rawRows.value, 'actual_start')
  const actualEndWidth = getAutoFitColumnWidth(rawRows.value, 'actual_end')

  if (hot) {
    hot.destroy()
    hot = null
  }

  hot = new Handsontable(
    hotContainer.value,
    {
      data: toRaw(getDisplayedRows()),

      width: '100%',
      height: 750,

      stretchH: 'all',

      autoWrapRow: true,
      autoWrapCol: true,

      autoColumnSize: true,
      autoRowSize: true,

      manualColumnResize: true,
      manualRowResize: true,

      hiddenColumns: {
        columns: getHiddenColumns(),
        indicators: true
      },

      rowHeaders: true,
      colHeaders: [
        'No',
        'Project Number',
        'Project Name',
        'Task No',
        'Main Task',
        'Sub Task',
        'Qty',
        'Assignee',
        'Process %',
        'Status',
        'Plan Start',
        'Plan End',
        'Plan Day',
        'Actual Start',
        'Actual End',
        'Actual Day',
        'Budget',
        'Actual Cost',
        'Budget Variance',
        'Remark'
      ],

      fixedColumnsStart: 0,

      columnSorting: true,
      filters: false,
      dropdownMenu: false,
      contextMenu: true,

      currentRowClassName: 'current-row',
      currentColClassName: 'current-col',

      outsideClickDeselects: false,
      viewportRowRenderingOffset: 120,

      columns: [
        {
          data: 'project_id',
          readOnly: true
        },
        {
          data: 'project_number',
          readOnly: true,
          renderer: hideRepeatedRenderer
        },
        {
          data: 'project_name',
          readOnly: true,
          renderer: hideRepeatedRenderer,
          width: projectNameWidth
        },
        {
          data: 'task_no',
          readOnly: true,
          renderer: hideRepeatedRenderer
        },
        {
          data: 'main_task',
          readOnly: true,
          renderer: hideRepeatedRenderer,
          width: mainTaskWidth
        },
        {
          data: 'sub_task',
          width: subtaskWidth
        },
        {
          data: 'qty',
          readOnly: true,
          renderer: hideRepeatedRenderer
        },
        {
          data: 'assignee',
          width: asssigneeWidth
        },
        {
          data: 'percent',
          type: 'numeric',
          readOnly: true
        },
        {
          data: 'status',
          readOnly: true,
          width: getStatusColumnWidth(tableData.value)
        },
        {
          data: 'plan_start',
          type: 'date',
          dateFormat: 'YYYY-MM-DD',
          correctFormat: true,
          width: planStartWidth
        },
        {
          data: 'plan_end',
          type: 'date',
          dateFormat: 'YYYY-MM-DD',
          correctFormat: true,
          width: planEndWidth
        },
        {
          data: 'plan_day',
          type: 'numeric',
          readOnly: true
        },
        {
          data: 'actual_start',
          type: 'date',
          dateFormat: 'YYYY-MM-DD',
          correctFormat: true,
          width: actualStartWidth
        },
        {
          data: 'actual_end',
          type: 'date',
          dateFormat: 'YYYY-MM-DD',
          correctFormat: true,
          width: actualEndWidth
        },
        {
          data: 'actual_day',
          type: 'numeric',
          readOnly: true
        },
        {
          data: 'budget',
          type: 'numeric',
          renderer: hideRepeatedRenderer
        },
        {
          data: 'actual_cost',
          type: 'numeric',
          renderer: hideRepeatedRenderer
        },
        {
          data: 'budget_variance',
          type: 'numeric',
          readOnly: true,
          renderer: hideRepeatedRenderer
        },
        {
          data: 'remark'
        }
      ],
      cells(row, col) {
        const cellProperties = {}
        const rowData = this.instance.getSourceDataAtRow(row)
        const prop = this.instance.colToProp(col)

        const hasModifyPermission = authStore.user?.userConfig?.includes('DS_PMS_PI_M') || false

        if ((prop === 'plan_start' || prop === 'plan_end') && !hasModifyPermission) {
          const isExistingRowWithOriginalData = rowData?.id_item && rowData?.[`_original_${prop}`]
          if (isExistingRowWithOriginalData) {
            cellProperties.readOnly = true
          }
        }

        if (rowData?.is_header) {
          const headerTypeClass = rowData.rowType === 'project'
            ? 'project-summary-row'
            : rowData.rowType === 'task'
              ? 'task-summary-row'
              : 'project-header-row'

          cellProperties.className = headerTypeClass

          const editableColumns = ['main_task', 'budget', 'actual_cost', 'qty']
          cellProperties.readOnly = !editableColumns.includes(prop)
        }

        return cellProperties
      },
      beforeBeginEditing(row, col) {
        const prop = this.colToProp(col)
        const rowData = this.getSourceDataAtRow(row)
        const hasModifyPermission = authStore.user?.userConfig?.includes('DS_PMS_PI_M') || false

        if ((prop === 'plan_start' || prop === 'plan_end') && !hasModifyPermission) {
          if (rowData?.id_item && rowData?.[`_original_${prop}`]) {
            return false
          }
        }
        return true
      },
      beforeRemoveRow(index, amount) {
        if (!hasDeletePermission()) {
          showDeletePermissionWarning()
          return false
        }

        const removedIds = []
        for (let i = 0; i < amount; i++) {
          const rowIndex = index + i
          const rowData = this.getSourceDataAtRow(rowIndex)

          if (rowData?.id_item) {
            removedIds.push(rowData.id_item)
          }
        }

        if (removedIds.length) {
          deletedItemIds.push(...removedIds)
        }

        return true
      },
      afterCreateRow(index, amount) {
        const prevRowData = this.getSourceDataAtRow(index - 1)
        const baseOrderNo = prevRowData && prevRowData.order_no ? Number(prevRowData.order_no) + 1 : 1

        for (let i = 0; i < amount; i++) {
          const currentGridIndex = index + i
          const newRow = this.getSourceDataAtRow(currentGridIndex) || {}
          const calculatedOrderNo = baseOrderNo + i

          this.setDataAtRowProp(currentGridIndex, 'order_no', calculatedOrderNo)

          if (prevRowData) {
            const columnsToCopy = ['project_id', 'project_number', 'project_name', 'task_no', 'main_task']
            columnsToCopy.forEach(col => {
              if (prevRowData[col] !== undefined) {
                this.setDataAtRowProp(currentGridIndex, col, prevRowData[col])
                newRow[col] = prevRowData[col]
              }
            })
          }

          // Default plan_end to currently selected date filter if active
          const defaultPlanDate = selectedDateString.value || null
          if (defaultPlanDate) {
            this.setDataAtRowProp(currentGridIndex, 'plan_end', defaultPlanDate)
            newRow.plan_end = defaultPlanDate
          }

          const payloadRow = {
            rowType: 'detail',
            is_header: false,
            project_id: newRow.project_id || '',
            project_number: newRow.project_number || '',
            project_name: newRow.project_name || '',
            task_no: newRow.task_no || '',
            main_task: newRow.main_task || '',
            sub_task: newRow.sub_task || '',
            assignee: newRow.assignee || '',
            percent: getRowProcess(newRow) || 0,
            status: getTaskStatus(newRow) || '',
            qty: newRow.qty || 0,
            budget: newRow.budget || 0,
            actual_cost: newRow.actual_cost || 0,
            user_id: authStore.user?.userId,
            plan_start: newRow.plan_start || null,
            plan_end: newRow.plan_end || defaultPlanDate,
            actual_start: newRow.actual_start || null,
            actual_end: newRow.actual_end || null,
            order_no: calculatedOrderNo,
            remark: newRow.remark || ''
          }

          insertedRowsToSave.push(payloadRow)
          insertedRowMap.set(currentGridIndex, payloadRow)
        }
      },
      beforeChange(changes, source) {
        if (!changes || source === 'loadData') return

        const hasModifyPermission = authStore.user?.userConfig?.includes('DS_PMS_PI_M') || false

        for (const [row, prop] of changes) {
          const rowData = this.getSourceDataAtRow(row)
          if (!rowData) continue

          if (!rowData.id_item) {
            continue
          }

          if (rowData.is_header) {
            const allowedHeaderProps = ['main_task', 'budget', 'actual_cost', 'qty']
            if (!allowedHeaderProps.includes(prop)) {
              return false
            }
            continue
          }

          const protectedReadOnlyProps = new Set([
            'project_id',
            'project_number',
            'project_name',
            'task_no',
            'main_task',
            'qty',
            'percent',
            'status',
            'plan_day',
            'actual_day',
            'budget_variance'
          ])

          if (protectedReadOnlyProps.has(prop)) {
            return false
          }

          if ((prop === 'plan_start' || prop === 'plan_end') && !hasModifyPermission) {
            if (rowData?.[`_original_${prop}`]) {
              return false
            }
          }
        }
      },
      afterChange(changes, source) {
        if (!changes || source === 'loadData') return

        changes.forEach(change => {
          const [row, prop, oldValue, newValue] = change
          const rowData = this.getSourceDataAtRow(row)

          if (!rowData) return

          if (rowData.is_header) {
            if (oldValue !== newValue) {
              modifiedHeaderRows.add(rowData)
            }

            if (prop === 'main_task' && oldValue !== newValue) {
              let nextRow = row + 1
              while (true) {
                const nextRowData = this.getSourceDataAtRow(nextRow)
                if (!nextRowData || nextRowData.is_header) break

                this.setDataAtRowProp(nextRow, 'main_task', newValue)
                if (nextRowData.id_item) {
                  changedRows.add(nextRowData.id_item)
                }
                nextRow++
              }
            }

            if (prop === 'qty' && oldValue !== newValue) {
              let nextRow = row + 1
              while (true) {
                const nextRowData = this.getSourceDataAtRow(nextRow)
                if (!nextRowData || nextRowData.is_header) break

                this.setDataAtRowProp(nextRow, 'qty', newValue)
                if (nextRowData.id_item) {
                  changedRows.add(nextRowData.id_item)
                }
                nextRow++
              }
            }

            if (prop === 'actual_cost' && oldValue !== newValue) {
              const affectedIds = syncSummaryActualCost(rowData, newValue)
              affectedIds.forEach(idItem => {
                if (idItem) {
                  changedRows.add(idItem)
                }
              })
            }
            return
          }

          const rowKey = row
          const insertedRow = insertedRowMap.get(rowKey)

          if (insertedRow) {
            insertedRow[prop] = newValue
            insertedRow.user_id = authStore.user?.userId

            if (['plan_start', 'plan_end', 'actual_start', 'actual_end'].includes(prop)) {
              insertedRow.percent = getRowProcess(insertedRow)
              insertedRow.status = getTaskStatus(insertedRow)
              this.setDataAtRowProp(row, 'percent', insertedRow.percent)
              this.setDataAtRowProp(row, 'status', insertedRow.status)
            }
            return
          }

          if (rowData.id_item && oldValue !== newValue) {
            if (['plan_start', 'plan_end', 'actual_start', 'actual_end'].includes(prop)) {
              const percent = getRowProcess(rowData)
              const status = getTaskStatus(rowData)
              this.setDataAtRowProp(row, 'percent', percent)
              this.setDataAtRowProp(row, 'status', status)
            }
            changedRows.add(rowData.id_item)
          }
        })
      },
      licenseKey: 'non-commercial-and-evaluation'
    }
  )
}

// ==========================================
// Filtering & Hierarchy Logic
// ==========================================

function getDisplayedRows() {
  const projectQuery = String(searchQuery.value || '').trim().toLowerCase()
  const taskQueryValue = String(taskQuery.value || '').trim().toLowerCase()
  const assigneeQueryValue = String(assigneeQuery.value || '').trim().toLowerCase()

  // 1. Identify projects matching project query
  const matchingProjectIds = new Set()
  for (const row of tableData.value) {
    const projectId = String(row.project_id ?? '')
    const projectNumber = String(row.project_number || '').toLowerCase()
    const projectName = String(row.project_name || '').toLowerCase()

    const projectMatches = !projectQuery || projectNumber.includes(projectQuery) || projectName.includes(projectQuery)
    if (projectMatches) {
      matchingProjectIds.add(projectId)
    }
  }

  // 2. Identify Tasks matching task query within valid projects
  const matchingTaskKeys = new Set()
  for (const row of tableData.value) {
    const projectId = String(row.project_id ?? '')
    if (!matchingProjectIds.has(projectId)) continue

    const mainTask = String(row.main_task || '').toLowerCase()
    const subTask = String(row.sub_task || '').toLowerCase()
    const taskNo = String(row.task_no || '').toLowerCase()

    const taskMatches = !taskQueryValue || taskNo.includes(taskQueryValue) || mainTask.includes(taskQueryValue) || subTask.includes(taskQueryValue)
    if (taskMatches) {
      matchingTaskKeys.add(`${projectId}__${row.main_task}`)
    }
  }

  // 3. Identify directly matching rows (project + task + assignee)
  const directlyMatchingRowIds = new Set()
  for (const row of tableData.value) {
    const projectId = String(row.project_id ?? '')
    const taskKey = `${projectId}__${row.main_task}`
    const assignee = String(row.assignee || '').toLowerCase()

    const projectMatches = matchingProjectIds.has(projectId)
    const taskMatches = matchingTaskKeys.has(taskKey)
    const assigneeMatches = !assigneeQueryValue || assignee.includes(assigneeQueryValue)

    if (projectMatches && taskMatches && assigneeMatches) {
      const rowId = row.id_item || `${projectId}__${row.main_task}`
      directlyMatchingRowIds.add(rowId)
    }
  }

  // 4. Build hierarchy visibility
  const visibleProjectIds = new Set()
  const visibleTaskKeys = new Set()
  for (const row of tableData.value) {
    const rowId = row.id_item || `${String(row.project_id ?? '')}__${row.main_task}`
    if (!directlyMatchingRowIds.has(rowId)) continue

    const projectId = String(row.project_id ?? '')
    const taskKey = `${projectId}__${row.main_task}`
    visibleProjectIds.add(projectId)
    visibleTaskKeys.add(taskKey)
  }

  // 5. Build final result based on View Mode
  const showProjectSummaries = viewMode.value === VIEW_MODES.PROJECT
  const showTaskSummaries = viewMode.value === VIEW_MODES.TASK
  const showFullDetail = viewMode.value === VIEW_MODES.FULL

  const result = []
  for (const row of tableData.value) {
    const projectId = String(row.project_id ?? '')
    const taskKey = `${projectId}__${row.main_task}`
    const visibleProject = visibleProjectIds.has(projectId)
    const visibleTask = visibleTaskKeys.has(taskKey)

    if (showProjectSummaries) {
      if (row.rowType !== 'project' || !visibleProject) continue
      result.push(row)
      continue
    }

    if (showTaskSummaries) {
      if (row.rowType === 'detail' || !visibleProject || !visibleTask) continue
      result.push(row)
      continue
    }

    if (showFullDetail) {
      if (!visibleProject || !visibleTask) continue
      result.push(row)
    }
  }

  return result
}

function getHiddenColumns() {
  if (viewMode.value === VIEW_MODES.PROJECT) {
    return [3, 7]
  }
  return []
}

function getAutoFitColumnWidth(rows, field, minWidth = 180, maxWidth = 420) {
  const canvas = document.createElement('canvas')
  const context = canvas.getContext('2d')
  context.font = '14px Inter, sans-serif'

  const headerLabel = field === 'project_name' ? 'Project Name' : 'Main Task'
  const values = rows
    .map(row => String(row?.[field] ?? ''))
    .concat(headerLabel)

  const maxTextWidth = values.reduce((max, value) => {
    const width = context.measureText(value).width
    return width > max ? width : max
  }, 0)

  const calculatedWidth = Math.ceil(maxTextWidth + 32)
  return Math.min(Math.max(calculatedWidth, minWidth), maxWidth)
}

function getStatusColumnWidth(rows) {
  const canvas = document.createElement('canvas')
  const context = canvas.getContext('2d')
  context.font = '14px Inter, sans-serif'

  const values = rows.map(row => row.status || '').concat('Status')

  const maxWidth = values.reduce((max, value) => {
    const width = context.measureText(value).width
    return width > max ? width : max
  }, 0)

  return Math.ceil(maxWidth + 50)
}

// Watchers
let searchTimer = null

watch(selectedDateString, () => {
  rebuildTableData()
})

watch(viewMode, () => {
  if (!hot) return
  hot.updateSettings({ hiddenColumns: { columns: getHiddenColumns(), indicators: true } })
  hot.render()
})

watch([viewMode, searchQuery, taskQuery, assigneeQuery], () => {
  if (!hot) return

  const activeElement = document.activeElement
  const isActiveSearchInput = activeElement === searchInput.value ||
                              activeElement === taskInput.value ||
                              activeElement === assigneeInput.value
  const selectionStart = isActiveSearchInput ? activeElement.selectionStart : null
  const selectionEnd = isActiveSearchInput ? activeElement.selectionEnd : null

  clearTimeout(searchTimer)
  searchTimer = setTimeout(() => {
    hot.loadData(toRaw(getDisplayedRows()))

    if (isActiveSearchInput && activeElement) {
      activeElement.focus()
      if (selectionStart !== null && selectionEnd !== null) {
        activeElement.setSelectionRange(selectionStart, selectionEnd)
      }
    }
  }, 180)
})

onBeforeUnmount(() => {
  clearTimeout(searchTimer)
  if (hot) {
    hot.destroy()
    hot = null
  }
})

// ==========================================
// Hierarchy & Calculation Utilities
// ==========================================

function getRowProcess(row) {
  const hasPlanStart = Boolean(row.plan_start)
  const hasPlanEnd = Boolean(row.plan_end)
  const hasActualStart = Boolean(row.actual_start)
  const hasActualEnd = Boolean(row.actual_end)

  return hasPlanStart && hasPlanEnd && hasActualStart && hasActualEnd ? 100 : 0
}

function averagePercent(rows) {
  const total = rows.reduce((sum, row) => sum + Number(row.percent || 0), 0)
  return rows.length ? Math.round(total / rows.length) : 0
}

function buildRowSummary(sourceRows, rowType) {
  const sample = sourceRows[0] || {}
  const planStart = getMinDate(sourceRows, 'plan_start')
  const planEnd = getMaxDate(sourceRows, 'plan_end')
  const actualStart = getMinDate(sourceRows, 'actual_start')
  const actualEnd = getMaxDate(sourceRows, 'actual_end')

  const totalSubTasks = sourceRows.reduce((count, row) => count + (row.sub_task ? 1 : 0), 0)
  const uniqueMainTaskCount = new Set(sourceRows.map(row => row.main_task).filter(Boolean)).size
  const totalHeaderQty = Array.from(
    sourceRows.reduce((map, row) => {
      if (row.main_task && !map.has(row.main_task)) {
        map.set(row.main_task, Number(row.qty || 0))
      }
      return map
    }, new Map()).values()
  ).reduce((sum, value) => sum + value, 0)

  const budget = Number(sample.budget || 0)
  const actualCost = Number(sample.actual_cost ?? sample.actualCost ?? 0)

  const result = {
    rowType,
    is_header: true,
    project_id: sample.project_id,
    project_number: sample.project_number,
    project_name: sample.project_name,
    task_no: rowType === 'task' ? sample.task_no : '',
    main_task: rowType === 'task' ? sample.main_task : '',
    sub_task: rowType === 'task' ? `${totalSubTasks} subtask` : '',
    qty: rowType === 'task' ? sample.qty || 0 : totalHeaderQty,
    assignee: rowType === 'task' ? sourceRows[0]?.assignee || '' : '',
    percent: averagePercent(sourceRows),
    status: getHeaderStatus(planStart, planEnd, actualStart, actualEnd),
    plan_start: planStart,
    plan_end: planEnd,
    plan_day: calculateUniqueActiveDays(sourceRows, 'plan_start', 'plan_end'),
    actual_start: actualStart,
    actual_end: actualEnd,
    actual_day: calculateUniqueActiveDays(sourceRows, 'actual_start', 'actual_end'),
    budget: budget,
    actual_cost: actualCost,
    budget_variance: budget - actualCost,
    remark: ''
  }

  if (rowType === 'project') {
    result.main_task = `${uniqueMainTaskCount} main task`
    result.sub_task = `Total ${totalSubTasks} subtask`
  }

  return result
}

function buildProjectHierarchy(rows) {
  const projectMap = new Map()

  rows.forEach(row => {
    const projectKey = row.project_id
    const taskKey = `${row.project_id}__${row.main_task}`

    if (!projectMap.has(projectKey)) {
      projectMap.set(projectKey, {
        project_id: row.project_id,
        project_number: row.project_number,
        project_name: row.project_name,
        tasks: new Map(),
        details: []
      })
    }

    const project = projectMap.get(projectKey)
    project.details.push(row)

    if (!project.tasks.has(taskKey)) {
      project.tasks.set(taskKey, {
        taskKey,
        main_task: row.main_task,
        task_no: row.task_no,
        assignee: row.assignee,
        sub_task: row.sub_task,
        details: []
      })
    }

    project.tasks.get(taskKey).details.push(row)
  })

  const flattened = []

  for (const project of projectMap.values()) {
    const projectSummary = buildRowSummary(project.details, 'project')
    projectSummary.project_id = project.project_id
    projectSummary.project_number = project.project_number
    projectSummary.project_name = project.project_name
    flattened.push(projectSummary)

    for (const task of project.tasks.values()) {
      const taskSummary = buildRowSummary(task.details, 'task')
      taskSummary.project_id = project.project_id
      taskSummary.project_number = project.project_number
      taskSummary.project_name = project.project_name
      taskSummary.task_no = task.task_no
      taskSummary.main_task = task.main_task
      taskSummary.assignee = task.assignee || ''
      flattened.push(taskSummary)

      task.details.forEach(detail => {
        flattened.push({
          ...detail,
          rowType: 'detail',
          is_header: false,
          plan_day: calculateDays(detail.plan_start, detail.plan_end),
          actual_day: calculateDays(detail.actual_start, detail.actual_end),
          status: detail.status || getTaskStatus(detail),
          percent: detail.percent === undefined ? getRowProcess(detail) : detail.percent,
          budget_variance: Number(detail.budget || 0) - Number(detail.actual_cost || 0)
        })
      })
    }
  }

  return flattened
}

function getMinDate(rows, field) {
  const dates = rows
    .map(r => r[field])
    .filter(Boolean)
    .map(d => new Date(d))

  if (!dates.length) return null

  return new Date(Math.min(...dates))
    .toISOString()
    .split('T')[0]
}

function getMaxDate(rows, field) {
  const dates = rows
    .map(r => r[field])
    .filter(Boolean)
    .map(d => new Date(d))

  if (!dates.length) return null

  return new Date(Math.max(...dates))
    .toISOString()
    .split('T')[0]
}

function getTaskStatus(row) {
  const planStart = row.plan_start ? new Date(row.plan_start) : null
  const planEnd = row.plan_end ? new Date(row.plan_end) : null
  const actualStart = row.actual_start ? new Date(row.actual_start) : null
  const actualEnd = row.actual_end ? new Date(row.actual_end) : null

  if (!planStart && !planEnd) return 'No plan'
  if (!actualStart && !actualEnd) return 'Not yet start'
  if (actualStart && !actualEnd) return 'Doing'
  if (actualEnd) {
    if (planEnd && actualEnd > planEnd) return 'Delay'
    return 'On Time'
  }
  return 'Not yet start'
}

function getHeaderStatus(planStart, planEnd, actualStart, actualEnd) {
  if (!planStart && !planEnd) return 'No plan'
  if (!actualStart && !actualEnd) return 'Not yet start'
  if (actualStart && !actualEnd) return 'Doing'
  if (actualEnd) {
    if (planEnd && actualEnd > planEnd) return 'Delay'
    return 'On Time'
  }
  return 'Not yet start'
}

function normalizeDateValue(value) {
  if (!value) return null
  const parsedDate = new Date(value)
  if (Number.isNaN(parsedDate.getTime())) return null
  parsedDate.setHours(0, 0, 0, 0)
  return parsedDate
}

function formatDateKey(date) {
  const year = date.getFullYear()
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const day = String(date.getDate()).padStart(2, '0')
  return `${year}-${month}-${day}`
}

function calculateDays(startDate, endDate) {
  const start = normalizeDateValue(startDate)
  const end = normalizeDateValue(endDate)

  if (!start || !end || end < start) return 0

  let count = 0
  const current = new Date(start)

  while (current <= end) {
    const dayOfWeek = current.getDay()
    if (dayOfWeek !== 0 && dayOfWeek !== 6) {
      count++
    }
    current.setDate(current.getDate() + 1)
  }

  return count
}

function calculateUniqueActiveDays(rows, startField, endField) {
  if (!Array.isArray(rows) || !rows.length) return 0

  const activeDates = new Set()

  rows.forEach(row => {
    const start = normalizeDateValue(row[startField])
    const end = normalizeDateValue(row[endField])

    if (!start || !end || end < start) return

    const current = new Date(start)

    while (current <= end) {
      const dayOfWeek = current.getDay()
      if (dayOfWeek !== 0 && dayOfWeek !== 6) {
        activeDates.add(formatDateKey(current))
      }
      current.setDate(current.getDate() + 1)
    }
  })

  return activeDates.size
}

function syncSummaryActualCost(headerRow, value) {
  if (!headerRow || !headerRow.is_header) return []

  const affectedIds = []

  tableData.value.forEach(row => {
    if (
      !row.is_header &&
      row.project_id === headerRow.project_id &&
      row.main_task === headerRow.main_task
    ) {
      row.actual_cost = value
      if (row.id_item) {
        affectedIds.push(row.id_item)
      }
    }
  })

  headerRow.actual_cost = value
  return affectedIds
}

const hideRepeatedColumns = [
  'project_number',
  'project_name',
  'task_no',
  'main_task',
  'qty',
  'budget',
  'actual_cost',
  'budget_variance'
]

function hideRepeatedRenderer(
  instance,
  td,
  row,
  col,
  prop,
  value,
  cellProperties
) {
  const rowData = instance.getSourceDataAtRow(row)
  const isDetailRow = rowData && !rowData.is_header && rowData.rowType !== 'project' && rowData.rowType !== 'task'

  const currencyFormatter = (val) => {
    if (val === null || val === undefined || val === '') return ''
    const normalized = String(val).replace(/[^0-9.-]/g, '')
    const num = Number(normalized)
    if (Number.isNaN(num)) return ''
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 2,
      maximumFractionDigits: 2
    }).format(num)
  }

  if (isDetailRow && hideRepeatedColumns.includes(prop)) {
    td.textContent = ''
    return td
  }

  if (['budget', 'actual_cost', 'budget_variance'].includes(prop)) {
    td.textContent = currencyFormatter(value)
    return td
  }

  Handsontable.renderers.TextRenderer.apply(this, arguments)
}

onMounted(async () => {
  await loadData()
})
</script>

<style scoped>
.project-page {
  padding: 0;
  background: #f5f7fb;
  min-height: 100vh;
  height: 100%;
}

/* ======================================
   Toolbar
====================================== */
.toolbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 12px;
  position: sticky;
  top: 0;
  z-index: 100;
  background: white;
  padding: 12px 16px;
  border-bottom: 1px solid #e5e7eb;
  border-radius: 12px 12px 0 0;
}

/* Date Filter Section */
.date-filter-box {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-wrap: wrap;
}

.date-filter-title {
  display: flex;
  align-items: center;
  gap: 6px;
}

.date-controls {
  display: flex;
  align-items: center;
  gap: 6px;
}

.date-step-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 34px;
  border-radius: 8px;
  border: 1px solid #d1d5db;
  background: #ffffff;
  color: #4b5563;
  cursor: pointer;
  transition: all 0.15s ease;
}

.date-step-btn:hover {
  background: #f3f4f6;
  color: #111827;
  border-color: #9ca3af;
}

:deep(.date-input-field) {
  width: 145px;
}

:deep(.date-input-field input) {
  padding: 6px 10px !important;
  font-size: 0.875rem !important;
  border-radius: 8px !important;
}

.quick-pill-btn {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 6px 12px;
  border-radius: 8px;
  font-size: 0.8125rem;
  font-weight: 600;
  border: 1px solid #d1d5db;
  background: #ffffff;
  color: #4b5563;
  cursor: pointer;
  transition: all 0.15s ease;
  white-space: nowrap;
}

.quick-pill-btn:hover {
  background: #f3f4f6;
  color: #111827;
}

.quick-pill-btn.active {
  background: #2563eb;
  color: #ffffff;
  border-color: #2563eb;
  box-shadow: 0 1px 3px rgba(37, 99, 235, 0.3);
}

/* Search Group */
.toolbar-search-group {
  display: flex;
  align-items: center;
  gap: 8px;
  flex: 1;
  max-width: 600px;
  min-width: 300px;
}

.toolbar-search-wrap {
  flex: 1;
  min-width: 0;
}

.search-input {
  width: 100%;
  padding: 7px 14px;
  font-size: 0.875rem;
  border: 1px solid #d1d5db;
  border-radius: 999px;
  color: #111827;
  background: #ffffff;
  transition: border-color 0.2s, box-shadow 0.2s;
}

.search-input:focus {
  outline: none;
  border-color: #2563eb;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.15);
}

/* Actions Group */
.toolbar-action-group {
  display: flex;
  align-items: center;
  gap: 8px;
}

.refresh-btn {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 9px 16px;
  border-radius: 10px;
  border: 1px solid #d1d5db;
  background: #ffffff;
  color: #374151;
  font-weight: 600;
  font-size: 0.8125rem;
  cursor: pointer;
  transition: all 0.2s;
}

.refresh-btn:hover:not(:disabled) {
  background: #f9fafb;
  border-color: #9ca3af;
  color: #111827;
}

.refresh-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.save-btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background: #dc2626;
  color: white;
  border: none;
  border-radius: 10px;
  padding: 9px 18px;
  font-size: 0.875rem;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: 0 4px 12px rgba(220, 38, 38, 0.25);
  white-space: nowrap;
}

.save-btn:hover:not(:disabled) {
  background: #b91c1c;
  transform: translateY(-1px);
}

.save-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

/* ======================================
   Card & Header
====================================== */
.table-card {
  background: white;
  border-radius: 18px;
  padding: 20px;
  border: 1px solid #e5e7eb;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.06);
}

.card-header {
  margin: 16px 0 14px 0;
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 16px;
  flex-wrap: wrap;
}

.header-left {
  flex: 1;
}

.title-row {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
}

.card-header h2 {
  margin: 0;
  font-size: 22px;
  font-weight: 700;
  color: #111827;
}

.active-date-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 4px 10px;
  border-radius: 999px;
  font-size: 0.8125rem;
  font-weight: 700;
  background: #eff6ff;
  color: #1d4ed8;
  border: 1px solid #bfdbfe;
}

.subtitle {
  margin-top: 4px;
  margin-bottom: 10px;
  color: #6b7280;
  font-size: 13px;
}

/* KPI Ribbon */
.kpi-ribbon {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
}

.kpi-chip {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 4px 10px;
  border-radius: 8px;
  font-size: 0.75rem;
  font-weight: 600;
  background: #f9fafb;
  border: 1px solid #e5e7eb;
  color: #4b5563;
}

.kpi-num {
  font-weight: 700;
  font-size: 0.875rem;
}

.chip-total .kpi-num {
  color: #1d4ed8;
}

.chip-tasks .kpi-num {
  color: #4338ca;
}

.chip-completed .kpi-num {
  color: #059669;
}

.chip-doing .kpi-num {
  color: #d97706;
}

.chip-delay .kpi-num {
  color: #6b7280;
}

.chip-delay.has-delay {
  background: #fef2f2;
  border-color: #fecaca;
  color: #b91c1c;
}

.chip-delay.has-delay .kpi-num {
  color: #dc2626;
}

/* Empty State Notification */
.empty-date-banner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  background: #f0f9ff;
  border: 1px solid #bae6fd;
  border-radius: 12px;
  padding: 12px 16px;
  margin-bottom: 14px;
}

.empty-content {
  display: flex;
  align-items: center;
  gap: 12px;
}

.empty-icon {
  font-size: 1.5rem;
  color: #0284c7;
}

.empty-title {
  font-weight: 700;
  color: #0369a1;
  font-size: 0.9375rem;
}

.empty-desc {
  font-size: 0.8125rem;
  color: #0c4a6e;
}

.empty-reset-btn {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  background: #0284c7;
  color: white;
  border: none;
  border-radius: 8px;
  padding: 8px 14px;
  font-size: 0.8125rem;
  font-weight: 600;
  cursor: pointer;
  white-space: nowrap;
  transition: background 0.15s;
}

.empty-reset-btn:hover {
  background: #0369a1;
}

/* View Switcher */
.view-switcher-wrapper {
  display: flex;
  align-items: center;
}

.view-switcher {
  display: inline-flex;
  background-color: #f3f4f6;
  padding: 4px;
  border-radius: 999px;
  border: 1px solid #e5e7eb;
}

.view-switcher button {
  border: none;
  background: transparent;
  color: #4b5563;
  padding: 7px 14px;
  border-radius: 999px;
  cursor: pointer;
  font-weight: 600;
  font-size: 13px;
  transition: all 0.15s ease-in-out;
  white-space: nowrap;
}

.view-switcher button:hover:not(.active) {
  color: #111827;
  background-color: rgba(255, 255, 255, 0.5);
}

.view-switcher button.active {
  background-color: #1d4ed8;
  color: #ffffff;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

/* Handsontable Wrapper */
.hot-wrapper {
  width: 100%;
  overflow: hidden;
}
</style>

<style>
/* ======================================
   Handsontable Styles (Global overrides)
====================================== */
.ht-theme-main thead th,
.ht_clone_top thead th {
  background: #1e3a8a !important;
  color: white !important;
  font-weight: 700;
  text-align: center;
  border-color: #274690 !important;
}

.ht_clone_left th,
.ht_master .htCore th {
  font-weight: 600;
}

.htCore td {
  vertical-align: middle;
}

.htCore tbody tr:nth-child(even) td {
  background: #f8fafc;
}

.current-row td {
  background: #dbeafe !important;
}

.current-col {
  background: #eff6ff !important;
}

.htDimmed {
  background: #f3f4f6 !important;
  color: #374151 !important;
}

.handsontable .wtHolder::-webkit-scrollbar {
  height: 10px;
  width: 10px;
}

.handsontable .wtHolder::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 10px;
}

.handsontable .htCore .project-header-row {
  background-color: #fff2cc !important;
  font-weight: bold !important;
}

.handsontable .htCore .project-summary-row {
  background-color: #e0f2fe !important;
  font-weight: 700 !important;
}

.handsontable .htCore .task-summary-row {
  background-color: #eef2ff !important;
  font-weight: 600 !important;
}
</style>

