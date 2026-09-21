const API_BASE = import.meta.env.VITE_API_BASE || "http://10.13.227.117:8000";


export async function getCommonDataFcost(payload) {
  const response = await fetch(`${API_BASE}/fcost/commondata`, {
    method: 'POST',
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(payload)
  });

  if (!response.ok) {
    const text = await response.text()
    throw new Error(`Failed to load common data: ${response.status} ${text}`)
  }

  return await response.json()
}

export async function getFailureCostRecords(payload = {}) {
  return getCommonDataFcost({
    userId: payload.userId || '',
    condition: 'Error_List'
  });
}

export async function createFailureCostList(payload) {
  const response = await fetch(`${API_BASE}/fcost/createlistitem`, {
    method: 'POST',
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(payload)
  });

  if (!response.ok) {
    const text = await response.text()
    throw new Error(`Failed to create failure cost item: ${response.status} ${text}`)
  }

  return await response.json()
}

export async function editFailureCostList(payload) {
  const response = await fetch(`${API_BASE}/fcost/editerrorlist`, {
    method: 'PUT',
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(payload)
  });

  if (!response.ok) {
    const text = await response.text()
    throw new Error(`Failed to modify failure cost list: ${response.status} ${text}`)
  }

  return await response.json()
}

