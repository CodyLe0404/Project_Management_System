
import axios from 'axios'

// const API_BASE = import.meta.env.VITE_API_BASE || "http://10.13.227.98:8000";
const API_BASE = import.meta.env.VITE_API_BASE || "http://10.13.227.119:8000";

let cachedProjects = null
let cachedProjectDetails = {}

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

  cachedProjects = null
  return response.json();
}

export async function getProjectsDetails() {

  const response = await fetch(
    `${API_BASE}/projects/details`
  )

  if (!response.ok) {

    const text = await response.text()

    throw new Error(
      `Failed to load project details: ${response.status} ${text}`
    )
  }

  return await response.json()
}

export async function getProjectSummary() {
  const response = await fetch(`${API_BASE}/projects/summary`)

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

export async function deleteProjectRowData({ itemIds, userId }) {
  const response = await fetch(
    `${API_BASE}/project-items/delete`,
    {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ item_ids: itemIds, user_id: userId })
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


