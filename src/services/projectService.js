
import axios from 'axios'

const API_BASE = import.meta.env.VITE_API_BASE || "http://127.0.0.1:8000";

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


// export async function fetchProjects() {
//   if (cachedProjects) {
//     return cachedProjects
//   }

//   const response = await fetch(`${API_BASE}/projects`);
//   if (!response.ok) {
//     throw new Error(`Failed to load projects: ${response.status}`);
//   }

//   cachedProjects = await response.json();
//   return cachedProjects;
// }

// export async function fetchProjectDetails(projectId) {
//   if (cachedProjectDetails[projectId]) {
//     return cachedProjectDetails[projectId]
//   }

//   const response = await fetch(`${API_BASE}/projects/${projectId}/details`);
//   if (!response.ok) {
//     throw new Error(`Failed to load project details: ${response.status}`);
//   }

//   const details = await response.json();
//   cachedProjectDetails[projectId] = details
//   return details;
// }

// export async function saveProjectDetails(projectId, rows) {
//   const response = await fetch(`${API_BASE}/projects/${projectId}/details`, {
//     method: 'POST',
//     headers: { 'Content-Type': 'application/json' },
//     body: JSON.stringify({ rows }),
//   })
//   if (!response.ok) {
//     const text = await response.text()
//     throw new Error(`Failed to save details: ${response.status} ${text}`)
//   }

//   const result = await response.json()
//   cachedProjectDetails[projectId] = rows
//   return result
// }

// export async function saveProjects(allRows) {
//   const response = await fetch(`${API_BASE}/projects/bulk-update`, { // Thay đổi URL endpoint này tùy theo backend của bạn
//     method: "POST",
//     headers: {
//       "Content-Type": "application/json",
//     },
//     body: JSON.stringify({ rows: allRows }),
//   });

//   if (!response.ok) {
//     const errorText = await response.text();
//     throw new Error(`Failed to save bulk projects: ${response.status} ${errorText}`);
//   }

//   // Xóa cache để đảm bảo lần sau fetch dữ liệu mới nhất
//   cachedProjects = null;
//   cachedProjectDetails = {};

//   return response.json();
// }

