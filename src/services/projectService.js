
import axios from 'axios'

const API_BASE = import.meta.env.VITE_API_BASE || "http://10.13.227.253:8000";

export async function createProject(project) {
  const response = await fetch(`${API_BASE}/projects`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(project),
  });

  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(`Failed to save project: ${response.status} ${errorText}`);
  }

  return response.json();
}

export async function getProjectsDetails(userId) {

  const response = await fetch(`${API_BASE}/projects/details?userId=${userId}`)

  if (!response.ok) {

    const text = await response.text()

    throw new Error(
      `Failed to load project details: ${response.status} ${text}`
    )
  }

  return await response.json()
}

export async function getProjectSummary(userId) {
  // URL sẽ thành: http://10.13.226.247:8000/projects/summary?userId=123
  const response = await fetch(`${API_BASE}/projects/summary?userId=${userId}`, {
    method: 'GET',
    headers: {
      'Accept': 'application/json'
    }
  });

  if (!response.ok) {
    const text = await response.text()
    throw new Error(`Failed to load project summary: ${response.status} ${text}`)
  }

  return await response.json()
}

export async function saveProjectItems(items) {
  
  const response = await fetch(
    `${API_BASE}/project-items/bulk-update`,
    {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(items)
    }
  )

  if (!response.ok) {

    const text = await response.text()

    throw new Error(
      `Failed to save project items: ${response.status} ${text}`
    )
  }

  return await response.json()
}

export async function deleteProjectRowData(item_id, username) {
  // console.log('Deleting project row data:', { item_ids: item_id, user_id: username })
  const response = await fetch(
    `${API_BASE}/project-items/delete`,
    {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ item_ids: item_id, user_id: username })
    }
  )

  if (!response.ok) {
    const text = await response.text()
    throw new Error(`Failed to delete project row: ${response.status} ${text}`)
  }

  return await response.json()
}

export async function insertProjectRowData(payload) {
  const response = await fetch(
    `${API_BASE}/project-items/insert`,
    {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(payload)
    }
  )

  if (!response.ok) {
    const text = await response.text()
    throw new Error(`Failed to insert project row: ${response.status} ${text}`)
  }

  return await response.json()
}

export async function changeUserPassword({ userId, currentPassword, newPassword }) {
  const response = await fetch(
    `${API_BASE}/changeuserpw`,
    {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ userId, currentPassword, newPassword })
    }
  )

  if (!response.ok) {
    const text = await response.text()
    throw new Error(`Failed to change password: ${response.status} ${text}`)
  }

  return await response.json()
}

