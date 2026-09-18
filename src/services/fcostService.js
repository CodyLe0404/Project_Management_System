const API_BASE = import.meta.env.VITE_API_BASE || "http://10.13.227.22:8000";


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

