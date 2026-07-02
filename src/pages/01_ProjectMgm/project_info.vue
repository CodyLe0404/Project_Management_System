<route>
{
  meta: {
    title: "Thông Tin Dự Án",
    icon: "pi pi-objects-column",
    permission: ["DS_PMS_PI"],
  }
}
</route>

<template>
  
  <div class="project-page">
  <section class="table-card">
    <!-- Toolbar -->
    <div class="toolbar">
      <div class="toolbar-search-wrap">
        <input
          ref="searchInput"
          v-model="searchQuery"
          type="text"
          placeholder="Search Project"
          class="search-input"
        />
      </div>

      <button
        @click="calculateAndSave"
        class="save-btn"
        :disabled="isSaving"
      >
        <i class="pi pi-save"></i>
        {{ isSaving ? 'SAVING...' : 'CALCULATE & SAVE' }}
      </button>
    </div>

    <!-- Project Information Card -->
    
      <div class="card-header header-with-toggle">
        <div>
          <h2>📊 Thông tin dự án</h2>
        </div>

        <div class="summary-toggle-wrapper">
          <span class="summary-toggle-title">Summary Task</span>
          <label class="toggle-container">
            <input type="checkbox" v-model="summaryTask" />
            <span class="slider"></span>
          </label>
        </div>
      </div>

      <div
        ref="hotContainer"
        class="hot-wrapper ht-theme-main"
      />
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, toRaw, watch } from 'vue'

import Handsontable from 'handsontable'

import 'handsontable/styles/handsontable.css'
import 'handsontable/styles/ht-theme-main.css'

import {
  registerAllModules
} from 'handsontable/registry'

import {
  getProjectsDetails,
  saveProjectItems,
  deleteProjectRowData,
  insertProjectRowData
} from '../../services/projectService'

import { useAuthStore } from '../../stores/auth';

registerAllModules()

const authStore = useAuthStore();

const hotContainer = ref(null)
const searchInput = ref(null)
const tableData = ref([])
const summaryTask = ref(false)
const searchQuery = ref('')
const isSaving = ref(false)

let hot = null
const changedRows = new Set()
let deletedItemIds = ""
let insertedRowsToSave = []
const insertedRowMap = new Map()  // Keep newly inserted rows in a map so their values can be updated immediately as the user edits cells in Handsontable.

const calculateAndSave = async () => {
  if (isSaving.value) return

  try {
    if (!hot) return

    if (deletedItemIds) {
      await deleteProjectRowData(deletedItemIds, authStore.user.userId)
      deletedItemIds = ""
      await loadData()
    }

    if (insertedRowsToSave.length) {
      await insertProjectRowData(insertedRowsToSave)
      insertedRowsToSave = []
      await loadData()
    }

    if (!changedRows.size) {
      alert('Saved successfully')
      return
    }

    isSaving.value = true

    const source = tableData.value.filter(
      row => !row.is_header && changedRows.has(row.id_item)
    )
    
    const payload = source.map(row => ({
      item_id: row.id_item,
      main_task: row.main_task || '',
      sub_task: row.sub_task || '',
      user_id: authStore.user.userId,
      assignee: row.assignee || null,

      plan_start: row.plan_start || null,
      plan_end: row.plan_end || null,

      actual_start: row.actual_start || null,
      actual_end: row.actual_end || null,

      actual_cost:
        row.actual_cost === ''
          ? null
          : Number(row.actual_cost),

      remark: row.remark || ''
    }))

    await saveProjectItems(payload)

    alert('Saved successfully')
    changedRows.clear()
    
    await loadData()
  }
  catch (error) {
    console.error(error)
    alert('Save failed')
  }
  finally {
    isSaving.value = false
  }
}
const loadData = async () => {
  try {
    deletedItemIds = ""
    const rawData = await getProjectsDetails()

    tableData.value = buildProjectRows(rawData || [])
    changedRows.clear()
    insertedRowsToSave = []
    insertedRowMap.clear()

    const projectNameWidth = getAutoFitColumnWidth(tableData.value, 'project_name')
    const mainTaskWidth = getAutoFitColumnWidth(tableData.value, 'main_task')

    if (hot) {
      hot.destroy()
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
          // 'Weight',
          // 'Contrib',
          'Budget',
          'Actual Cost',
          'Budget Variance',
          'Remark'
        ],

        fixedColumnsStart: 0,

        columnSorting: true,
        filters: true,
        dropdownMenu: true,
        contextMenu: true,

        currentRowClassName: 'current-row',
        currentColClassName: 'current-col',

        outsideClickDeselects: false,

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
            // readOnly: true
          },
          {
            data: 'qty'
          },
          {
            data: 'assignee'
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
            correctFormat: true
          },
          {
            data: 'plan_end',
            type: 'date',
            dateFormat: 'YYYY-MM-DD',
            correctFormat: true
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
            correctFormat: true
          },
          {
            data: 'actual_end',
            type: 'date',
            dateFormat: 'YYYY-MM-DD',
            correctFormat: true
          },
          {
            data: 'actual_day',
            type: 'numeric',
            readOnly: true
          },
          // {
          //   data: 'weight',
          //   type: 'numeric',
          //   readOnly: true
          // },
          // {
          //   data: 'contrib',
          //   type: 'numeric',
          //   readOnly: true
          // },
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

          if (rowData?.is_header) {
            cellProperties.className = 'project-header-row'

            const prop = this.instance.colToProp(col)
            // Allow editing of both 'main_task' and 'actual_cost' in the header row
            if (prop === 'main_task') {
              cellProperties.readOnly = false
            } else if (prop !== 'actual_cost') {
              cellProperties.readOnly = true
            }
          }

          return cellProperties
        },
        //id_item of any deleted rows for tracking
        beforeRemoveRow(index, amount) {
          const removedIds = []
          for (let i = 0; i < amount; i++) {
            const rowIndex = index + i
            const rowData = this.getSourceDataAtRow(rowIndex)

            if (rowData?.id_item) {
              removedIds.push(rowData.id_item)
            }
          }

          if (removedIds.length) {
            deletedItemIds = removedIds.join(',')
          }

          return true
        },
        afterCreateRow(index, amount) {
          const insertedRows = []

          for (let i = 0; i < amount; i++) {
            const newRowIndex = index + i
            const previousRow = this.getSourceDataAtRow(newRowIndex - 1)
            const newRow = this.getSourceDataAtRow(newRowIndex)

            if (previousRow && newRow) {
              const columnsToCopy = [
                'project_id',
                'project_number',
                'project_name',
                'task_no',
                'main_task',
                'qty',
                'budget',
                'actual_cost'
              ]

              columnsToCopy.forEach(column => {
                if (previousRow[column] !== undefined) {
                  this.setDataAtRowProp(newRowIndex, column, previousRow[column])
                  newRow[column] = previousRow[column]
                }
              })
            }

            const payloadRow = {
              project_id: newRow?.project_id || '',
              project_number: newRow?.project_number || '',
              project_name: newRow?.project_name || '',
              task_no: newRow?.task_no || '',
              main_task: newRow?.main_task || '',
              sub_task: newRow?.sub_task || '',
              assignee: newRow?.assignee || '',
              qty: newRow?.qty || 0,
              budget: newRow?.budget || 0,
              actual_cost: newRow?.actual_cost || 0,
              user_id: authStore.user.userId,
              plan_start: newRow?.plan_start || null,
              plan_end: newRow?.plan_end || null,
              actual_start: newRow?.actual_start || null,
              actual_end: newRow?.actual_end || null
            }

            insertedRows.push(payloadRow)
            insertedRowsToSave.push(payloadRow)
            insertedRowMap.set(newRowIndex, payloadRow)
          }

        },
        // Ended log
        afterChange(changes, source) {    // Triggered automatically after any cell value changes in Handsontable
          if (!changes || source === 'loadData') return   // Ignore if there are no changes or if the changes were caused by loadData()

          changes.forEach(change => {     // Loop through every changed cell
            const [row, prop, oldValue, newValue] = change    // row = row index of the edited cell
            const rowData = this.getSourceDataAtRow(row)      // Get the complete data object of the edited row

            if (!rowData) return

            // Check whether the edited row is a header/summary row
            if (rowData.is_header) {    
              // Handle main_task change propagation from header to detail rows
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

              // Only process when: 1. The edited column is "actual_cost" and 2. The value has actually changed
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

            const rowKey = row  //uses the row index as the lookup key.
            const insertedRow = insertedRowMap.get(rowKey)  //checks whether that row was previously created as a new

            if (insertedRow) {        //If the row exists in the map, it immediately updates the matching field
              insertedRow[prop] = newValue        // writes the new cell value into the saved object
              insertedRow.user_id = authStore.user.userId       //ensures the row also has the current user ID
              return        //stops the rest of the change handling, so this inserted row is not treated like a normal existing row.
            }

            // For normal row if the row has an item ID and the value really changed, record this row as modified
            if (rowData.id_item && oldValue !== newValue) {
              changedRows.add(rowData.id_item)
            }
          })
        },
        licenseKey: 'non-commercial-and-evaluation'
      }
    )
  }
  catch (error) {
    console.error(error)
  }
}

function getDisplayedRows() {
  const baseRows = summaryTask.value
    ? tableData.value.filter(row => row.is_header)
    : tableData.value

  const query = String(searchQuery.value || '').trim().toLowerCase()
  if (!query) {
    return baseRows
  }

  return baseRows.filter(row => {
    const projectNumber = String(row.project_number || '').toLowerCase()
    const projectName = String(row.project_name || '').toLowerCase()

    return (
      projectNumber.includes(query) ||
      projectName.includes(query)
    )
  })
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

  const values = rows
    .map(row => row.status || '')
    .concat('Status')

  const maxWidth = values.reduce((max, value) => {
    const width = context.measureText(value).width
    return width > max ? width : max
  }, 0)

  return Math.ceil(maxWidth + 50)
}

let searchTimer = null

watch(summaryTask, () => {
  if (hot) {
    hot.loadData(toRaw(getDisplayedRows()))
  }
})

watch(searchQuery, () => {
  if (!hot) return

  clearTimeout(searchTimer)
  searchTimer = setTimeout(() => {
    hot.loadData(toRaw(getDisplayedRows()))
    searchInput.value?.focus()
  }, 180)
})

onBeforeUnmount(() => {
  clearTimeout(searchTimer)
})

function getRowProcess(row) {
  const hasPlanStart = Boolean(row.plan_start)
  const hasPlanEnd = Boolean(row.plan_end)
  const hasActualStart = Boolean(row.actual_start)
  const hasActualEnd = Boolean(row.actual_end)

  return hasPlanStart && hasPlanEnd && hasActualStart && hasActualEnd
    ? 100
    : 0
}

function getHeaderProcess(rows) {
  if (!rows.length) {
    return 0
  }

  const total = rows.reduce(
    (sum, row) => sum + Number(row.percent || 0),
    0
  )

  return Math.round(total / rows.length)
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

  if (!planStart && !planEnd) {
    return 'No plan'
  }

  if (!actualStart && !actualEnd) {
    return 'Not yet start'
  }

  if (actualStart && !actualEnd) {
    return 'Doing'
  }

  if (actualEnd) {
    if (planEnd && actualEnd > planEnd) {
      return 'Delay'
    }

    if (planEnd && actualEnd < planEnd) {
      return 'Ahead of schedule'
    }

    return 'On Time'
  }

  return 'Not yet start'
}

function getHeaderStatus(headerRow) {
  if (!headerRow) {
    return 'Pending'
  }

  return getTaskStatus(headerRow)
}

function calculateDays(startDate, endDate) {
  if (!startDate || !endDate) return 0

  const start = new Date(startDate)
  const end = new Date(endDate)

  return Math.ceil(
    (end - start) / (1000 * 60 * 60 * 24)
  )
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

function buildProjectRows(rows) {
  const grouped = new Map()

  rows.forEach(row => {
    const key = `${row.project_id}_${row.main_task}`

    if (!grouped.has(key)) {
      grouped.set(key, [])
    }

    grouped.get(key).push(row)
  })

  const result = []

  const currentGroups = Array.from(grouped.values())

  // 3. Duyệt qua từng nhóm để tính toán dữ liệu hiển thị
  currentGroups.forEach(projectRows => {
    const firstRow = projectRows[0]

    const planStart = getMinDate(
      projectRows,
      'plan_start'
    )

    const planEnd = getMaxDate(
      projectRows,
      'plan_end'
    )

    const actualStart = getMinDate(
      projectRows,
      'actual_start'
    )

    const actualEnd = getMaxDate(
      projectRows,
      'actual_end'
    )

    const budget = projectRows.reduce(
      (sum, row) =>
        sum + Number(row.budget || 0),
      0
    )

    const actualCost = projectRows.reduce(
      (sum, row) =>
        sum + Number(row.actual_cost || 0),
      0
    )

    const detailRows = projectRows.map(row => ({
      ...row,
      status: getTaskStatus(row),
      percent: getRowProcess(row),
      plan_day: calculateDays(row.plan_start, row.plan_end),
      actual_day: calculateDays(row.actual_start, row.actual_end)
    }))

    const headerRow = {
      is_header: true,

      project_id: firstRow.project_id,
      project_number: firstRow.project_number,
      project_name: firstRow.project_name,
      task_no : firstRow.task_no,
      main_task: firstRow.main_task,

      sub_task: 'Switchgears',

      qty: firstRow.qty,

      assignee: firstRow.assignee || "",

      percent: getHeaderProcess(detailRows),

      status: null,

      plan_start: planStart,
      plan_end: planEnd,

      plan_day: detailRows.reduce(
        (sum, row) =>
          sum + Number(row.plan_day || 0),
        0
      ),

      actual_start: actualStart,
      actual_end: actualEnd,

      actual_day: detailRows.reduce(
        (sum, row) =>
          sum + Number(row.actual_day || 0),
        0
      ),

      weight: projectRows.reduce(
        (sum, row) =>
          sum + Number(row.weight || 0),
        0
      ),

      contrib: projectRows.reduce(
        (sum, row) =>
          sum + Number(row.contrib || 0),
        0
      ),

      budget: firstRow.budget,

      actual_cost: firstRow.actual_cost,

      budget_variance:
        firstRow.budget - firstRow.actual_cost,

      remark: ''
    }

    headerRow.status = getHeaderStatus(headerRow)

    result.push(headerRow)
    result.push(...detailRows)
  })

  return result
}

const hideRepeatedColumns = [
  'project_number',
  'project_name',
  'task_no',
  'main_task',
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

  // Helper: format numeric values as USD currency
  const currencyFormatter = (val) => {
    if (val === null || val === undefined || val === '') return ''
    const normalized = String(val).toString().replace(/[^0-9.-]/g, '')
    const num = Number(normalized)
    if (Number.isNaN(num)) return ''
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 2,
      maximumFractionDigits: 2
    }).format(num)
  }

  // If this is a detail row and the column is in hideRepeatedColumns, hide repeated values
  if (rowData && !rowData.is_header && hideRepeatedColumns.includes(prop)) {
    td.textContent = ''
    return td
  }

  // Render currency columns with formatting
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
  justify-content: flex-end;
  position: relative;
  gap: 16px;

  position: sticky;
  top: 0;

  z-index: 100;
  background: white;
  padding: 10px 1px;
  border-bottom: 1px solid #e5e7eb;
}

.toolbar-search-wrap {
  position: absolute;
  left: 50%;
  transform: translateX(-50%);
  width: min(420px, calc(100% - 240px));
}

.search-input {
  width: 100%;
  padding: 10px 14px;
  font-size: 0.95rem;
  border: 1px solid #d1d5db;
  border-radius: 999px;
  color: #111827;
  background: #ffffff;
}

.search-input:focus {
  outline: none;
  border-color: #2563eb;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.15);
}

/* ======================================
   Save Button
====================================== */

.save-btn {
  display: flex;
  align-items: center;
  gap: 10px;

  background: #dc2626;
  color: white;

  border: none;
  border-radius: 12px;

  padding: 12px 24px;

  font-size: 16px;
  font-weight: 700;

  cursor: pointer;

  transition: all 0.25s ease;

  box-shadow:
    0 8px 20px rgba(220, 38, 38, 0.25);
}

.save-btn:hover {
  background: #b91c1c;
  transform: translateY(-2px);
}

.save-btn:active {
  transform: translateY(0);
}

/* ======================================
   Card
====================================== */

.table-card {
  background: white;

  border-radius: 18px;

  padding: 24px;

  border: 1px solid #e5e7eb;

  box-shadow:
    0 10px 30px rgba(0,0,0,0.06);
}

.card-header {
  margin-bottom: 10px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 16px;
}

.card-header h2 {
  margin: 0;
  font-size: 24px;
  font-weight: 700;

  color: #111827;
}

.header-with-toggle {
  flex-wrap: wrap;
}

.card-header p {
  margin-top: 6px;

  color: #6b7280;
  font-size: 14px;
}

/* ======================================
   Handsontable Wrapper
====================================== */

.hot-wrapper {
  width: 100%;
  overflow: hidden;
}

.summary-toggle-wrapper {
  display: flex;
  align-items: flex-end;
  gap: 12px;
  margin: 0;
  padding-top: 20px;
}

.summary-toggle-title {
  font-weight: 700;
  color: #111827;
}

.toggle-switch {
  width: 50px;
  height: 25px;
  border-radius: 999px;
  border: none;
  background: #cbd5e1;
  position: relative;
  cursor: pointer;
  transition: background 0.2s ease;
  outline: none;
}

.toggle-switch-on {
  background: #1e3a8a;
}

.toggle-switch-handle {
  position: absolute;
  top: 3px;
  left: 3px;
  width: 22px;
  height: 22px;
  border-radius: 50%;
  background: #ffffff;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.2);
  transition: left 0.2s ease;
}

.toggle-switch-on .toggle-switch-handle {
  left: calc(50% - 25px);
}

</style>

<style>

/* ======================================
   Handsontable Header
====================================== */

.ht-theme-main thead th,
.ht_clone_top thead th {
  background: #1e3a8a !important;
  color: white !important;

  font-weight: 700;
  text-align: center;

  border-color: #274690 !important;
}

/* ======================================
   Row Header
====================================== */

.ht_clone_left th,
.ht_master .htCore th {
  font-weight: 600;
}

/* ======================================
   Cell
====================================== */

.htCore td {
  vertical-align: middle;
}

/* ======================================
   Zebra Rows
====================================== */

.htCore tbody tr:nth-child(even) td {
  background: #f8fafc;
}

/* ======================================
   Selected Row
====================================== */

.current-row td {
  background: #dbeafe !important;
}

/* ======================================
   Selected Column
====================================== */

.current-col {
  background: #eff6ff !important;
}

/* ======================================
   Readonly Cells
====================================== */

.htDimmed {
  background: #f3f4f6 !important;
  color: #374151 !important;
}

/* ======================================
   Scrollbar
====================================== */

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

</style>

<style>
    /* 1. Thiết lập vùng chứa bao quanh */
    .toggle-container {
      display: inline-block;
      position: relative;
      width: 48px;
      height: 26px;
    }

    /* 2. Ẩn checkbox mặc định của trình duyệt */
    .toggle-container input {
      opacity: 0;
      width: 0;
      height: 0;
    }

    /* 3. Khung nền của Toggle (Trạng thái TẮT - Mặc định) */
    .slider {
      position: absolute;
      cursor: pointer;
      top: 0;
      left: 0;
      right: 0;
      bottom: 0;
      background-color: #cbd5e1; /* Màu xám nhạt */
      border-radius: 999px; /* Bo tròn hoàn toàn */
      transition: background-color 0.2s ease;
    }

    /* 4. Vòng tròn nhỏ bên trong */
    .slider::before {
      content: "";
      position: absolute;
      height: 20px;
      width: 20px;
      left: 3px;
      bottom: 3px;
      background-color: white;
      border-radius: 50%;
      box-shadow: 0 1px 3px rgba(0, 0, 0, 0.2);
      /* Tạo hiệu ứng di chuyển mượt mà */
      transition: transform 0.2s ease;
    }

    /* 5. THAY ĐỔI KHI BẬT (Khi checkbox được check) */
    
    /* Đổi màu nền thành màu đen giống ảnh mẫu */
    input:checked + .slider {
      background-color: #063377; 
    }

    /* Dịch chuyển vòng tròn nhỏ sang bên phải */
    input:checked + .slider::before {
      /* Tổng chiều rộng 50px - nút tròn 22px - lề trái 3px = cách lề phải 3px.
         Dịch chuyển chính xác 22px là vừa vặn nhất */
      transform: translateX(22px);
    }
  </style>
