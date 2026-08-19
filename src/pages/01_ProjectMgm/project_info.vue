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
      <div class="toolbar-search-group">
        <div class="toolbar-search-wrap">
          <input
            ref="searchInput"
            v-model="searchQuery"
            type="text"
            placeholder="Search Project"
            class="search-input"
          />
        </div>

        <div class="toolbar-search-wrap">
          <input
            ref="taskInput"
            v-model="taskQuery"
            type="text"
            placeholder="Search Main Task"
            class="search-input"
          />
        </div>
        <div class="toolbar-search-wrap">
          <input
            ref="assigneeInput"
            v-model="assigneeQuery"
            type="text"
            placeholder="Search Assignee"
            class="search-input"
          />
        </div>
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
const tableData = ref([])
const rawRows = ref([])
const searchInput = ref(null)
const taskInput = ref(null)
const assigneeInput = ref(null)
const searchQuery = ref('')
const taskQuery = ref('')
const assigneeQuery = ref('')
const isSaving = ref(false)

const VIEW_MODES = {
  PROJECT: 'project-summary',
  TASK: 'task-summary',
  FULL: 'full-detail'
}

const viewMode = ref(VIEW_MODES.FULL)

const setViewMode = (mode) => {
  viewMode.value = mode
}

let hot = null
const changedRows = new Set()
let deletedItemIds = []
let insertedRowsToSave = []
const insertedRowMap = new Map()  // Keep newly inserted rows in a map so their values can be updated immediately as the user edits cells in Handsontable.

const getDeleteCount = () => new Set(deletedItemIds).size

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
    user_id: authStore.user.userId,
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

const calculateAndSave = async () => {
  if (isSaving.value || !hot) return

  const hasDeletes = deletedItemIds.length > 0
  const hasInserts = insertedRowsToSave.length > 0
  const hasUpdates = changedRows.size > 0

  if (!hasDeletes && !hasInserts && !hasUpdates) {
    alert('Saved successfully')
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
        alert(`⚠️Quá nhiều dữ liệu được xóa cùng lúc. Vui lòng xóa dữ liệu theo từng nhóm nhỏ hơn 500 rows!`)
      }
      else{
        await deleteProjectRowData(removeRows, authStore.user.userId)
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

    alert('Saved successfully')
    changedRows.clear()
    deletedItemIds = []
    insertedRowsToSave = []
    insertedRowMap.clear()

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
    const rawData = await getProjectsDetails(authStore.user.userId)
    // console.log(rawData)

    // Store original values of plan_start and plan_end for all persisted rows (for permission checks)
    if (rawData) {
      rawData.forEach(row => {
        if (row.id_item) { // Only for rows that came from the database
          row._original_plan_start = row.plan_start
          row._original_plan_end = row.plan_end
        }
      })
    }
    
    rawRows.value = rawData || []
    tableData.value = buildProjectHierarchy(rawRows.value)
    changedRows.clear()
    insertedRowsToSave = []
    insertedRowMap.clear()

    const projectNameWidth = getAutoFitColumnWidth(tableData.value, 'project_name')
    const mainTaskWidth = getAutoFitColumnWidth(tableData.value, 'main_task')
    const subtaskWidth = getAutoFitColumnWidth(tableData.value, 'sub_task')
    const asssigneeWidth = getAutoFitColumnWidth(tableData.value, 'assignee')
    const planStartWidth = getAutoFitColumnWidth(tableData.value, 'plan_start')
    const planEndWidth = getAutoFitColumnWidth(tableData.value, 'plan_end')
    const actualStartWidth = getAutoFitColumnWidth(tableData.value, 'actual_start')
    const actualEndWidth = getAutoFitColumnWidth(tableData.value, 'actual_end')

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
          // 'Weight',
          // 'Contrib',
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
            // readOnly: true
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
          const prop = this.instance.colToProp(col)
          
          // Check if user has the 'DS_PMS_PI_M' permission (manager permission)
          const hasModifyPermission = authStore.user.userConfig.includes('DS_PMS_PI_M') || false
          
          // We track original values to allow editing unsaved changes even after they're entered
          if ((prop === 'plan_start' || prop === 'plan_end') && !hasModifyPermission) {
            // Always allow editing for new rows (no id_item)
            const isNewRow = !rowData?.id_item

            // This allows users to edit values they just entered (unsaved changes)
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
        // Hook that runs before a cell begins editing - final permission check
        beforeBeginEditing(row, col, originalEvent, cellProperties) {
          const prop = this.colToProp(col)
          const rowData = this.getSourceDataAtRow(row)
          const hasModifyPermission = authStore.user.userConfig.includes('DS_PMS_PI_M') || false
          
          // Only block if: row is persisted (has id_item) AND the cell originally had data when loaded from server
          if ((prop === 'plan_start' || prop === 'plan_end') && !hasModifyPermission) {
            if (rowData?.id_item && rowData?.[`_original_${prop}`]) {
              return false // Prevent editing
            }
          }
          return true // Allow editing
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
            deletedItemIds.push(...removedIds)
          }

          return true
        },
        afterCreateRow(index, amount) {
          // const insertedRows = []
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
                'actual_cost',
                'order_no'
              ]

              columnsToCopy.forEach(column => {
                if (previousRow[column] !== undefined) {
                  this.setDataAtRowProp(newRowIndex, column, previousRow[column])
                  newRow[column] = previousRow[column]
                }
              })
            }

            const payloadRow = {
              rowType: 'detail',
              is_header: false,
              project_id: newRow?.project_id || '',
              project_number: newRow?.project_number || '',
              project_name: newRow?.project_name || '',
              task_no: newRow?.task_no || '',
              main_task: newRow?.main_task || '',
              sub_task: newRow?.sub_task || '',
              assignee: newRow?.assignee || '',
              percent: getRowProcess(newRow) || 0,
              status: getTaskStatus(newRow) || '',
              qty: newRow?.qty || 0,
              budget: newRow?.budget || 0,
              actual_cost: newRow?.actual_cost || 0,
              user_id: authStore.user.userId,
              plan_start: newRow?.plan_start || null,
              plan_end: newRow?.plan_end || null,
              actual_start: newRow?.actual_start || null,
              actual_end: newRow?.actual_end || null,
              order_no: newRow?.order_no + 1 || null,
              remark: newRow?.remark || ''
            }

            if (newRow) {
              newRow.rowType = 'detail'
              newRow.is_header = false
            }

            insertedRowsToSave.push(payloadRow)
            insertedRowMap.set(newRowIndex, payloadRow)
          }
        },
        
        beforeChange(changes, source) {
          if (!changes || source === 'loadData') return

          const hasModifyPermission = authStore.user.userConfig.includes('DS_PMS_PI_M') || false

          for (const [row, prop, oldValue, newValue] of changes) {
            const rowData = this.getSourceDataAtRow(row)
            if (!rowData) continue

            // Keep the original insert flow intact: only protect persisted rows.
            // Newly inserted rows are copied programmatically during afterCreateRow.
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

            const rowKey = row  // uses the row index as the lookup key.
            const insertedRow = insertedRowMap.get(rowKey)  // checks whether that row was previously created as a new

            if (insertedRow) {        // If the row exists in the map, it immediately updates the matching field
              insertedRow[prop] = newValue        // writes the new cell value into the saved object
              insertedRow.user_id = authStore.user.userId       // ensures the row also has the current user ID

              if (['plan_start', 'plan_end', 'actual_start', 'actual_end'].includes(prop)) {
                insertedRow.percent = getRowProcess(insertedRow)
                insertedRow.status = getTaskStatus(insertedRow)
                this.setDataAtRowProp(row, 'percent', insertedRow.percent)
                this.setDataAtRowProp(row, 'status', insertedRow.status)
              }

              return        //stops the rest of the change handling, so this inserted row is not treated like a normal existing row.
            }

            // For normal row if the row has an item ID and the value really changed, record this row as modified
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
  catch (error) {
    console.error(error)
  }
}

function getDisplayedRows() {
  // 1. Normalize search queries
  const projectQuery = String(searchQuery.value || '').trim().toLowerCase()
  const taskQueryValue = String(taskQuery.value || '').trim().toLowerCase()
  const assigneeQueryValue = String(assigneeQuery.value || '').trim().toLowerCase()

  // 2. Identify projects that match project filter
  const matchingProjectIds = new Set()

  for (const row of tableData.value) {
    const projectId = String(row.project_id ?? '')
    const projectNumber = String(row.project_number || '').toLowerCase()
    const projectName = String(row.project_name || '').toLowerCase()

    // No project filter -> all projects are valid
    const projectMatches = !projectQuery || projectNumber.includes(projectQuery) || projectName.includes(projectQuery)

    if (projectMatches) {
      matchingProjectIds.add(projectId)
    }
  }

  // 3. Identify Main Task / Sub Task that match within the matching projects
  const matchingTaskKeys = new Set()

  for (const row of tableData.value) {
    const projectId = String(row.project_id ?? '')

    // Skip rows belonging to non-matching projects
    if (!matchingProjectIds.has(projectId)) {
      continue
    }

    const mainTask = String(row.main_task || '').toLowerCase()
    const subTask = String(row.sub_task || '').toLowerCase()
    const taskNo = String(row.task_no || '').toLowerCase()

    // Empty task filter -> all tasks are valid
    const taskMatches = !taskQueryValue || taskNo.includes(taskQueryValue) || mainTask.includes(taskQueryValue) || subTask.includes(taskQueryValue)
    if (taskMatches) {
      matchingTaskKeys.add(`${projectId}__${row.main_task}`)
    }
  }

  // 4. Identify rows that satisfy ALL filters Project AND Main Task / Sub Task AND Assignee
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
  
  // 5. Build hierarchy from matching rows Matching Detail -> Matching Main Task -> Matching Project
  const visibleProjectIds = new Set()
  const visibleTaskKeys = new Set()

  for (const row of tableData.value) {
    const rowId =
      row.id_item ||
      `${String(row.project_id ?? '')}__${row.main_task}`

    if (!directlyMatchingRowIds.has(rowId)) {
      continue
    }

    const projectId = String(row.project_id ?? '')
    const taskKey = `${projectId}__${row.main_task}`

    visibleProjectIds.add(projectId)
    visibleTaskKeys.add(taskKey)
  }

  // 6. View modes
  const showProjectSummaries = viewMode.value === VIEW_MODES.PROJECT
  const showTaskSummaries = viewMode.value === VIEW_MODES.TASK
  const showFullDetail = viewMode.value === VIEW_MODES.FULL

  // 7. Build final result
  const result = []
  for (const row of tableData.value) {
    const projectId = String(row.project_id ?? '')
    const taskKey = `${projectId}__${row.main_task}`
    const visibleProject = visibleProjectIds.has(projectId)
    const visibleTask = visibleTaskKeys.has(taskKey)

    // PROJECT VIEW Only show project summary rows
    if (showProjectSummaries) {
      if (row.rowType !== 'project') {
        continue
      }

      if (!visibleProject) {
        continue
      }

      result.push(row)
      continue
    }

    // TASK VIEW Show project + task summary rows - Only show tasks that match the filter
    if (showTaskSummaries) {
      if (row.rowType === 'detail') {
        continue
      }

      if (!visibleProject || !visibleTask) {
        continue
      }

      result.push(row)
      continue
    }

    // FULL VIEW Show project + task + detail rows belonging to matching Project / Task hierarchy
    if (showFullDetail) {
      if (!visibleProject || !visibleTask) {
        continue
      }
      result.push(row)
    }
  }

  return result
}

function getHiddenColumns() {
  if (viewMode.value === VIEW_MODES.PROJECT) {
    return [3, 7]
    // return []
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

let searchTimer = null

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

  const budget = sample.budget
  const actualCost = sample.actualCost

  const result = {
    rowType,
    is_header: true,
    project_id: sample.project_id,
    project_number: sample.project_number,
    project_name: sample.project_name,
    task_no: rowType === 'task' ? sample.task_no : '',
    main_task: rowType === 'task' ? sample.main_task : '',
    sub_task: rowType === 'task' ? `${totalSubTasks} subtask` || '' : '',
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
    const totalSubTaskCount = totalSubTasks

    result.main_task = `${uniqueMainTaskCount} main task`
    result.sub_task = `Total ${totalSubTaskCount} subtask`
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
      // taskSummary.sub_task = 'Switchgears'
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
      // return 'Ahead of schedule'
      return 'On Time'
    }

    return 'On Time'
  }

  return 'Not yet start'
}

function getHeaderStatus(planStart, planEnd, actualStart, actualEnd) {
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
      // return 'Ahead of schedule'
      return 'On Time'
    }

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
    // const dayOfWeek = current.getDay()
    // if (dayOfWeek !== 0 && dayOfWeek !== 6) {
      count++
    // }

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
      // const dayOfWeek = current.getDay()
      // if (dayOfWeek !== 0 && dayOfWeek !== 6) {
        activeDates.add(formatDateKey(current))
      // }

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

  // Helper: format numeric values consistently, without blocking rendering.
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

.toolbar-search-group {
  position: absolute;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  gap: 6px;
  width: min(1100px, calc(100% - 500px));
}

.toolbar-search-wrap {
  flex: 1;
  min-width: 0;
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
/* Đảm bảo Header và cụm nút nằm cùng 1 hàng ngang */
.card-header.header-with-toggle {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.view-switcher-wrapper {
  display: flex;
  align-items: center;
}

/* Khung viền chung chứa 3 button */
.view-switcher {
  display: inline-flex;
  background-color: #f3f4f6; /* Màu nền xám nhạt làm khung */
  padding: 4px;
  border-radius: 999px;
  border: 1px solid #e5e7eb;
}

/* Kiểu dáng các button bên trong khung */
.view-switcher button {
  border: none;
  background: transparent;
  color: #4b5563;
  padding: 8px 16px;
  border-radius: 999px;
  cursor: pointer;
  font-weight: 600;
  font-size: 14px;
  transition: all 0.15s ease-in-out;
  white-space: nowrap;
}

/* Hiệu ứng khi rê chuột qua button chưa active */
.view-switcher button:hover:not(.active) {
  color: #111827;
  background-color: rgba(255, 255, 255, 0.5);
}

/* Button đang được chọn (Active) */
.view-switcher button.active {
  background-color: #1d4ed8; /* Màu xanh chủ đạo */
  color: #ffffff;
  box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
}

.toggle-switch {
  width: 40px;
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

  .handsontable .htCore .project-summary-row {
    background-color: #e0f2fe !important;
    font-weight: 700 !important;
  }

  .handsontable .htCore .task-summary-row {
    background-color: #eef2ff !important;
    font-weight: 600 !important;
  }
</style>