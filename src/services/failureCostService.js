/**
 * Failure Cost Service Layer (Mock Implementation)
 * Provides clean async API methods designed to be swapped with FastAPI endpoints later.
 */

import {
  mockDepartments,
  mockErrorCatalogsByDept,
  mockAllErrorCatalogs,
  mock4MAnalysisList,
  mockStatuses,
  mockProjects,
  mockUsers,
  initialFailureCostRecords
} from '../mock/failureCostMockData.js';

const STORAGE_KEY = 'failure_cost_records_v1';

// Helper: load records from localStorage with fallback to initial mock dataset
function loadRecords() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(initialFailureCostRecords));
      return [...initialFailureCostRecords];
    }
    const parsed = JSON.parse(raw);
    if (Array.isArray(parsed) && parsed.length > 0) {
      return parsed;
    }
    return [...initialFailureCostRecords];
  } catch (err) {
    console.error('Error loading failure cost records from localStorage:', err);
    return [...initialFailureCostRecords];
  }
}

// Helper: save records to localStorage
function saveRecords(records) {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(records));
  } catch (err) {
    console.error('Error saving failure cost records to localStorage:', err);
  }
}

// Simulated network latency for realistic UX feel
const delay = (ms = 120) => new Promise(resolve => setTimeout(resolve, ms));

/**
 * Get all master data (Departments, Catalogs, 4M, Statuses, Projects, Users)
 */
export async function getMasterData() {
  await delay(50);
  return {
    departments: mockDepartments,
    errorCatalogsByDept: mockErrorCatalogsByDept,
    allErrorCatalogs: mockAllErrorCatalogs,
    analysis4MList: mock4MAnalysisList,
    statuses: mockStatuses,
    projects: mockProjects,
    users: mockUsers
  };
}

/**
 * Reset records to original mock dataset (useful for testing)
 */
export async function resetFailureCostsToDefault() {
  await delay(100);
  localStorage.setItem(STORAGE_KEY, JSON.stringify(initialFailureCostRecords));
  return [...initialFailureCostRecords];
}

/**
 * Query and filter Failure Cost records
 */
export async function getFailureCosts(filterParams = {}, pagination = null) {
  await delay(150);
  let records = loadRecords();

  // 1. Apply Date Filter
  if (filterParams.fromDate) {
    records = records.filter(r => r.errorDate >= filterParams.fromDate);
  }
  if (filterParams.toDate) {
    records = records.filter(r => r.errorDate <= filterParams.toDate);
  }

  // 2. Apply Department / Team Filter
  if (filterParams.departmentId) {
    records = records.filter(r => r.departmentId === Number(filterParams.departmentId));
  }

  // 3. Apply Project Filter
  if (filterParams.projectId) {
    records = records.filter(r => r.projectId === Number(filterParams.projectId));
  }

  // 4. Apply PIC Filter
  if (filterParams.picUserId) {
    records = records.filter(r => r.picUserId === Number(filterParams.picUserId));
  }

  // 5. Apply Checker Filter
  if (filterParams.checkerUserId) {
    records = records.filter(r => r.checkerUserId === Number(filterParams.checkerUserId));
  }

  // 6. Apply Error Catalog Filter
  if (filterParams.errorCatalogId) {
    records = records.filter(r => r.errorCatalogId === Number(filterParams.errorCatalogId));
  }

  // 7. Apply 4M Filter
  if (filterParams.analysis4MId) {
    records = records.filter(r => r.analysis4MId === Number(filterParams.analysis4MId));
  }

  // 8. Apply Status Filter
  if (filterParams.statusId) {
    records = records.filter(r => r.statusId === Number(filterParams.statusId));
  }

  // 9. Keyword Search (searches multiple text fields)
  if (filterParams.keyword && filterParams.keyword.trim()) {
    const kw = filterParams.keyword.trim().toLowerCase();
    records = records.filter(r => {
      return (
        (r.projectNo && r.projectNo.toLowerCase().includes(kw)) ||
        (r.projectName && r.projectName.toLowerCase().includes(kw)) ||
        (r.defectDescription && r.defectDescription.toLowerCase().includes(kw)) ||
        (r.rootCause && r.rootCause.toLowerCase().includes(kw)) ||
        (r.correction && r.correction.toLowerCase().includes(kw)) ||
        (r.prevention && r.prevention.toLowerCase().includes(kw)) ||
        (r.remark && r.remark.toLowerCase().includes(kw)) ||
        (r.picName && r.picName.toLowerCase().includes(kw)) ||
        (r.errorCatalogName && r.errorCatalogName.toLowerCase().includes(kw))
      );
    });
  }

  // Sort by date descending by default
  records.sort((a, b) => new Date(b.errorDate) - new Date(a.errorDate) || b.id - a.id);

  const total = records.length;

  // Pagination if requested
  if (pagination && pagination.page && pagination.pageSize) {
    const page = Number(pagination.page);
    const pageSize = Number(pagination.pageSize);
    const startIndex = (page - 1) * pageSize;
    const endIndex = startIndex + pageSize;
    const paginatedRecords = records.slice(startIndex, endIndex);

    return {
      data: paginatedRecords,
      total,
      page,
      pageSize,
      totalPages: Math.ceil(total / pageSize) || 1
    };
  }

  return {
    data: records,
    total,
    page: 1,
    pageSize: total,
    totalPages: 1
  };
}

/**
 * Get a single record by ID
 */
export async function getFailureCostById(id) {
  await delay(100);
  const records = loadRecords();
  const record = records.find(r => r.id === Number(id));
  if (!record) {
    throw new Error(`Failure Cost record #${id} not found`);
  }
  return { ...record };
}

/**
 * Create a new Failure Cost record
 */
export async function createFailureCost(payload) {
  await delay(200);
  const records = loadRecords();

  const nextId = records.length > 0 ? Math.max(...records.map(r => r.id)) + 1 : 1;

  // Lookup master data names for clean denormalized presentation
  const dept = mockDepartments.find(d => d.id === Number(payload.departmentId));
  const project = mockProjects.find(p => p.id === Number(payload.projectId));
  const pic = mockUsers.find(u => u.id === Number(payload.picUserId));
  const checker = mockUsers.find(u => u.id === Number(payload.checkerUserId));
  const catalog = mockAllErrorCatalogs.find(c => c.id === Number(payload.errorCatalogId));
  const m4 = mock4MAnalysisList.find(m => m.analysis4MId === Number(payload.analysis4MId));
  const status = mockStatuses.find(s => s.id === Number(payload.statusId));

  const nowIso = new Date().toISOString();

  const newRecord = {
    id: nextId,
    errorDate: payload.errorDate,
    departmentId: Number(payload.departmentId),
    departmentName: dept ? dept.name : (payload.departmentName || ''),
    projectId: Number(payload.projectId),
    projectNo: project ? project.projectNo : (payload.projectNo || ''),
    projectName: project ? project.projectName : (payload.projectName || ''),
    picUserId: Number(payload.picUserId),
    picName: pic ? pic.name : (payload.picName || ''),
    checkerUserId: Number(payload.checkerUserId),
    checkerName: checker ? checker.name : (payload.checkerName || ''),
    errorCatalogId: Number(payload.errorCatalogId),
    errorCatalogName: catalog ? catalog.name : (payload.errorCatalogName || ''),
    defectDescription: payload.defectDescription || '',
    quantity: Number(payload.quantity) || 1,
    failureCostUSD: Number(payload.failureCostUSD) || 0,
    analysis4MId: Number(payload.analysis4MId),
    analysis4MName: m4 ? m4.name : (payload.analysis4MName || ''),
    rootCause: payload.rootCause || '',
    correction: payload.correction || '',
    prevention: payload.prevention || '',
    statusId: Number(payload.statusId),
    statusName: status ? status.name : (payload.statusName || 'Open'),
    remark: payload.remark || '',
    createdAt: nowIso,
    updatedAt: nowIso
  };

  records.unshift(newRecord);
  saveRecords(records);
  return { ...newRecord };
}

/**
 * Update an existing Failure Cost record
 */
export async function updateFailureCost(id, payload) {
  await delay(200);
  const records = loadRecords();
  const index = records.findIndex(r => r.id === Number(id));
  if (index === -1) {
    throw new Error(`Failure Cost record #${id} not found`);
  }

  const existing = records[index];

  const dept = mockDepartments.find(d => d.id === Number(payload.departmentId));
  const project = mockProjects.find(p => p.id === Number(payload.projectId));
  const pic = mockUsers.find(u => u.id === Number(payload.picUserId));
  const checker = mockUsers.find(u => u.id === Number(payload.checkerUserId));
  const catalog = mockAllErrorCatalogs.find(c => c.id === Number(payload.errorCatalogId));
  const m4 = mock4MAnalysisList.find(m => m.analysis4MId === Number(payload.analysis4MId));
  const status = mockStatuses.find(s => s.id === Number(payload.statusId));

  const updatedRecord = {
    ...existing,
    errorDate: payload.errorDate || existing.errorDate,
    departmentId: payload.departmentId ? Number(payload.departmentId) : existing.departmentId,
    departmentName: dept ? dept.name : (payload.departmentName || existing.departmentName),
    projectId: payload.projectId ? Number(payload.projectId) : existing.projectId,
    projectNo: project ? project.projectNo : (payload.projectNo || existing.projectNo),
    projectName: project ? project.projectName : (payload.projectName || existing.projectName),
    picUserId: payload.picUserId ? Number(payload.picUserId) : existing.picUserId,
    picName: pic ? pic.name : (payload.picName || existing.picName),
    checkerUserId: payload.checkerUserId ? Number(payload.checkerUserId) : existing.checkerUserId,
    checkerName: checker ? checker.name : (payload.checkerName || existing.checkerName),
    errorCatalogId: payload.errorCatalogId ? Number(payload.errorCatalogId) : existing.errorCatalogId,
    errorCatalogName: catalog ? catalog.name : (payload.errorCatalogName || existing.errorCatalogName),
    defectDescription: payload.defectDescription !== undefined ? payload.defectDescription : existing.defectDescription,
    quantity: payload.quantity !== undefined ? Number(payload.quantity) : existing.quantity,
    failureCostUSD: payload.failureCostUSD !== undefined ? Number(payload.failureCostUSD) : existing.failureCostUSD,
    analysis4MId: payload.analysis4MId ? Number(payload.analysis4MId) : existing.analysis4MId,
    analysis4MName: m4 ? m4.name : (payload.analysis4MName || existing.analysis4MName),
    rootCause: payload.rootCause !== undefined ? payload.rootCause : existing.rootCause,
    correction: payload.correction !== undefined ? payload.correction : existing.correction,
    prevention: payload.prevention !== undefined ? payload.prevention : existing.prevention,
    statusId: payload.statusId ? Number(payload.statusId) : existing.statusId,
    statusName: status ? status.name : (payload.statusName || existing.statusName),
    remark: payload.remark !== undefined ? payload.remark : existing.remark,
    updatedAt: new Date().toISOString()
  };

  records[index] = updatedRecord;
  saveRecords(records);
  return { ...updatedRecord };
}

/**
 * Delete a Failure Cost record
 */
export async function deleteFailureCost(id) {
  await delay(150);
  const records = loadRecords();
  const filtered = records.filter(r => r.id !== Number(id));
  if (filtered.length === records.length) {
    throw new Error(`Failure Cost record #${id} not found`);
  }
  saveRecords(filtered);
  return true;
}

/**
 * Calculate Dashboard Metrics and Chart Data dynamically
 */
export async function getFailureCostDashboard(filterParams = {}) {
  await delay(150);
  const { data: records } = await getFailureCosts(filterParams);

  // 1. KPI Calculations
  const totalFailureCost = records.reduce((sum, r) => sum + (Number(r.failureCostUSD) || 0), 0);
  const totalErrors = records.length;
  const totalQuantity = records.reduce((sum, r) => sum + (Number(r.quantity) || 0), 0);
  const openErrors = records.filter(r => r.statusName === 'Open').length;
  const monitoringErrors = records.filter(r => r.statusName === 'Monitoring').length;
  const closedErrors = records.filter(r => r.statusName === 'Closed').length;
  const averageCostPerError = totalErrors > 0 ? (totalFailureCost / totalErrors) : 0;

  // 2. Chart 1 — Failure Cost by Month (Jan to Dec 2026)
  const monthNames = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
  const monthlyCostMap = {};
  const monthlyCountMap = {};
  monthNames.forEach(m => {
    monthlyCostMap[m] = 0;
    monthlyCountMap[m] = 0;
  });

  records.forEach(r => {
    if (r.errorDate) {
      const date = new Date(r.errorDate);
      if (!isNaN(date.getTime())) {
        const m = monthNames[date.getMonth()];
        monthlyCostMap[m] = (monthlyCostMap[m] || 0) + (Number(r.failureCostUSD) || 0);
        monthlyCountMap[m] = (monthlyCountMap[m] || 0) + 1;
      }
    }
  });

  const costByMonth = monthNames.map(m => ({
    month: m,
    cost: monthlyCostMap[m],
    count: monthlyCountMap[m]
  }));

  // 3. Chart 2 — Failure Cost by Department / Team
  const deptCostMap = {};
  const deptCountMap = {};
  mockDepartments.forEach(d => {
    deptCostMap[d.name] = 0;
    deptCountMap[d.name] = 0;
  });

  records.forEach(r => {
    const dept = r.departmentName || 'Other';
    deptCostMap[dept] = (deptCostMap[dept] || 0) + (Number(r.failureCostUSD) || 0);
    deptCountMap[dept] = (deptCountMap[dept] || 0) + 1;
  });

  const costByDepartment = mockDepartments.map(d => ({
    department: d.name,
    cost: deptCostMap[d.name] || 0,
    count: deptCountMap[d.name] || 0
  }));

  // 4. Chart 3 — Failure Cost by Error Catalog
  const catalogCostMap = {};
  const catalogCountMap = {};
  records.forEach(r => {
    const cat = r.errorCatalogName || 'Unspecified';
    catalogCostMap[cat] = (catalogCostMap[cat] || 0) + (Number(r.failureCostUSD) || 0);
    catalogCountMap[cat] = (catalogCountMap[cat] || 0) + 1;
  });

  const costByErrorCatalog = Object.keys(catalogCostMap).map(cat => ({
    catalog: cat,
    cost: catalogCostMap[cat],
    count: catalogCountMap[cat]
  })).sort((a, b) => b.cost - a.cost);

  // 5. Chart 4 — Errors by 4M Analysis (Man, Machine, Material, Method)
  const count4MMap = {
    Man: 0,
    Machine: 0,
    Material: 0,
    Method: 0
  };
  const cost4MMap = {
    Man: 0,
    Machine: 0,
    Material: 0,
    Method: 0
  };

  records.forEach(r => {
    const m = r.analysis4MName || 'Method';
    if (count4MMap[m] !== undefined) {
      count4MMap[m]++;
      cost4MMap[m] += (Number(r.failureCostUSD) || 0);
    }
  });

  const errorsBy4M = {
    counts: count4MMap,
    costs: cost4MMap,
    total: totalErrors
  };

  // 6. Recent Failure Cost Records (latest 6-8 records)
  const recentRecords = records.slice(0, 8);

  return {
    kpis: {
      totalFailureCost,
      totalErrors,
      totalQuantity,
      openErrors,
      monitoringErrors,
      closedErrors,
      averageCostPerError
    },
    charts: {
      costByMonth,
      costByDepartment,
      costByErrorCatalog,
      errorsBy4M
    },
    recentRecords
  };
}
