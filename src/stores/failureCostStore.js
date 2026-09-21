import { defineStore } from 'pinia';
import { ref, reactive } from 'vue';
import {
  getMasterData,
  getFailureCosts,
  getFailureCostById,
  createFailureCost,
  updateFailureCost,
  deleteFailureCost,
  getFailureCostDashboard,
  resetFailureCostsToDefault,
  updateFailureCostList
} from '../services/failureCostService.js';

import { editFailureCostList } from '../services/fcostService.js';

export const useFailureCostStore = defineStore('failureCost', () => {
  // Master data
  const masterData = ref({
    departments: [],
    errorCatalogsByDept: {},
    allErrorCatalogs: [],
    analysis4MList: [],
    statuses: [],
    projects: [],
    users: []
  });

  const masterDataLoaded = ref(false);

  // List data & pagination
  const records = ref([]);
  const totalRecords = ref(0);
  const pagination = reactive({
    page: 1,
    pageSize: 10,
    totalPages: 1
  });

  // Global / shared filter
  const filter = reactive({
    fromDate: '',
    toDate: '',
    departmentId: null,
    projectId: null,
    picUserId: null,
    checkerUserId: null,
    errorCatalogId: null,
    analysis4MId: null,
    statusId: null,
    keyword: ''
  });

  // Dashboard Aggregated Data
  const dashboardData = ref({
    kpis: {
      totalFailureCost: 0,
      totalErrors: 0,
      totalQuantity: 0,
      openErrors: 0,
      monitoringErrors: 0,
      closedErrors: 0,
      averageCostPerError: 0
    },
    charts: {
      costByMonth: [],
      costByDepartment: [],
      costByErrorCatalog: [],
      errorsBy4M: {
        counts: {},
        costs: {},
        total: 0
      }
    },
    recentRecords: []
  });

  // Selected or active record (Detail / Edit)
  const currentRecord = ref(null);

  // Status flags
  const loading = ref(false);
  const error = ref(null);

  /**
   * Fetch master data once
   */
  async function fetchMasterData() {
    if (masterDataLoaded.value) return masterData.value;
    try {
      const data = await getMasterData();
      masterData.value = data;
      masterDataLoaded.value = true;
      return data;
    } catch (err) {
      console.error('Failed to load master data:', err);
      error.value = err.message;
      throw err;
    }
  }

  /**
   * Fetch list records with current filter and pagination
   */
  async function fetchRecords() {
    loading.value = true;
    error.value = null;
    try {
      await fetchMasterData();
      const res = await getFailureCosts(filter, {
        page: pagination.page,
        pageSize: pagination.pageSize
      });
      records.value = res.data;
      totalRecords.value = res.total;
      pagination.totalPages = res.totalPages;
      return res;
    } catch (err) {
      console.error('Failed to fetch records:', err);
      error.value = err.message;
      throw err;
    } finally {
      loading.value = false;
    }
  }

  /**
   * Fetch Dashboard metrics and charts
   */
  async function fetchDashboard(customFilter = null) {
    loading.value = true;
    error.value = null;
    try {
      await fetchMasterData();
      const activeFilter = customFilter || filter;
      const res = await getFailureCostDashboard(activeFilter);
      dashboardData.value = res;
      return res;
    } catch (err) {
      console.error('Failed to fetch dashboard data:', err);
      error.value = err.message;
      throw err;
    } finally {
      loading.value = false;
    }
  }

  /**
   * Fetch single record by ID
   */
  async function fetchRecordById(id) {
    loading.value = true;
    error.value = null;
    try {
      await fetchMasterData();
      const record = await getFailureCostById(id);
      currentRecord.value = record;
      return record;
    } catch (err) {
      console.error(`Failed to fetch record #${id}:`, err);
      error.value = err.message;
      throw err;
    } finally {
      loading.value = false;
    }
  }

  /**
   * Create new Failure Cost record
   */
  async function createRecord(payload) {
    loading.value = true;
    error.value = null;
    try {
      const created = await createFailureCost(payload);
      // Refresh list & dashboard
      await fetchRecords();
      return created;
    } catch (err) {
      console.error('Failed to create record:', err);
      error.value = err.message;
      throw err;
    } finally {
      loading.value = false;
    }
  }

  /**
   * Update existing Failure Cost record
   */
  async function updateRecord(id, payload) {
    loading.value = true;
    error.value = null;
    try {
      const updated = await updateFailureCost(id, payload);
      currentRecord.value = updated;
      // Refresh list & dashboard
      await fetchRecords();
      return updated;
    } catch (err) {
      console.error(`Failed to update record #${id}:`, err);
      error.value = err.message;
      throw err;
    } finally {
      loading.value = false;
    }
  }

  async function updateRecordList(id, payload) {
    loading.value = true;
    error.value = null;
    try {
      // 1. Tạo new_payload dạng dictionary (object) có 'id' là key/property đầu tiên
      const new_payload = {
        errorId: id,
        ...payload
      };

      // 2. Gọi hàm editFailureCostList với new_payload
      const result = await editFailureCostList(new_payload);
      return result;
    } catch (err) {
      console.error(`Failed to edit record #${id}:`, err);
      error.value = err.message || 'An error occurred';
      throw err;
    } finally {
      loading.value = false;
    }
  }

  /**
   * Delete record by ID
   */
  async function deleteRecord(id) {
    loading.value = true;
    error.value = null;
    try {
      const success = await deleteFailureCost(id);
      await fetchRecords();
      return success;
    } catch (err) {
      console.error(`Failed to delete record #${id}:`, err);
      error.value = err.message;
      throw err;
    } finally {
      loading.value = false;
    }
  }

  /**
   * Filter controls
   */
  function setFilter(newFilter) {
    Object.assign(filter, newFilter);
    pagination.page = 1;
  }

  function resetFilter() {
    filter.fromDate = '';
    filter.toDate = '';
    filter.departmentId = null;
    filter.projectId = null;
    filter.picUserId = null;
    filter.checkerUserId = null;
    filter.errorCatalogId = null;
    filter.analysis4MId = null;
    filter.statusId = null;
    filter.keyword = '';
    pagination.page = 1;
  }

  function setPage(page) {
    pagination.page = page;
  }

  function setPageSize(size) {
    pagination.pageSize = size;
    pagination.page = 1;
  }

  async function resetToInitialDataset() {
    loading.value = true;
    try {
      await resetFailureCostsToDefault();
      resetFilter();
      await fetchRecords();
      await fetchDashboard();
    } finally {
      loading.value = false;
    }
  }

  return {
    masterData,
    masterDataLoaded,
    records,
    totalRecords,
    pagination,
    filter,
    dashboardData,
    currentRecord,
    loading,
    error,
    fetchMasterData,
    fetchRecords,
    fetchDashboard,
    fetchRecordById,
    createRecord,
    updateRecord,
    updateRecordList,
    deleteRecord,
    setFilter,
    resetFilter,
    setPage,
    setPageSize,
    resetToInitialDataset
  };
});


