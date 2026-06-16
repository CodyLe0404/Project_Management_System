<route>
{
  meta: {
    title: "Thông Tin Dự Án",
    icon: "pi pi-objects-column"
  }
}
</route>

<template>
  
  <div class="project-page">
  <section class="table-card">
    <!-- Toolbar -->
    <div class="toolbar">
      <button
        @click="calculateAndSave"
        class="save-btn"
      >
        <i class="pi pi-save"></i>
        CALCULATE & SAVE
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
import { ref, onMounted, toRaw, watch } from 'vue'

import Handsontable from 'handsontable'

import 'handsontable/styles/handsontable.css'
import 'handsontable/styles/ht-theme-main.css'

import {
  registerAllModules
} from 'handsontable/registry'

import {
  getProjectsDetails,
  saveProjectItems
} from '../../services/projectService'

registerAllModules()

const hotContainer = ref(null)
const tableData = ref([])
const summaryTask = ref(false)

let hot = null

const calculateAndSave = async () => {
  try {
    if (!hot) return

    const source = hot.getSourceData().filter(row => !row.is_header)
    
    const payload = source.map(row => ({
      item_id: row.item_id,

      assignee: row.assignee || null,

      plan_start: row.plan_start || null,
      plan_end: row.plan_end || null,

      actual_start: row.actual_start || null,
      actual_end: row.actual_end || null,

      actual_cost:
        row.actual_cost === ''
          ? null
          : Number(row.actual_cost),

      remark: row.remark || null
    }))

    await saveProjectItems(payload)

    alert('Saved successfully')
    
    await loadData()
  }
  catch (error) {
    console.error(error)
    alert('Save failed')
  }
}

const loadData = async () => {
  try {
    const rawData = await getProjectsDetails()
    tableData.value = buildProjectRows(rawData || [])

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
            renderer: hideRepeatedRenderer
          },
          {
            data: 'main_task',
            readOnly: true,
            renderer: hideRepeatedRenderer
          },
          {
            data: 'sub_task',
            readOnly: true
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
            readOnly: true
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

            // make header read-only except for 'actual_cost'
            const prop = this.instance.colToProp(col)
            if (prop !== 'actual_cost') {
              cellProperties.readOnly = true
            }
          }

          return cellProperties
        },
        afterChange(changes, source) {
          if (!changes || source === 'loadData') return

          changes.forEach(change => {
            const [row, prop, oldValue, newValue] = change

            if (prop === 'actual_cost' && oldValue !== newValue) {
              const rowData = this.getSourceDataAtRow(row)

              // only react when user changed header actual_cost
              if (rowData && rowData.is_header) {
                const nextRow = row + 1
                const nextRowData = this.getSourceDataAtRow(nextRow)

                if (nextRowData && !nextRowData.is_header) {
                  // copy value into the row below
                  this.setDataAtRowProp(nextRow, 'actual_cost', newValue)
                }
              }
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
  return summaryTask.value
    ? tableData.value.filter(row => row.is_header)
    : tableData.value
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

watch(summaryTask, () => {
  if (hot) {
    hot.loadData(toRaw(getDisplayedRows()))
  }
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

function buildProjectRows(rows) {
  const grouped = {}

  rows.forEach(row => {
    const key = `${row.project_id}_${row.main_task}`

    if (!grouped[key]) {
      grouped[key] = []
    }

    grouped[key].push(row)
  })

  const result = []

  Object.values(grouped).forEach(projectRows => {
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
  'main_task',
  'budget',
  'actual_cost'
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

  if (
    rowData &&
    !rowData.is_header &&
    hideRepeatedColumns.includes(prop)
  ) {
    td.textContent = ''
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
  padding: 1px;
  background: #f5f7fb;
  min-height: 100vh;
  height: 100%;
}

/* ======================================
   Toolbar
====================================== */

.toolbar {
  display: flex;
  justify-content: flex-end;

  position: sticky;
  top: 0;

  z-index: 100;
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
