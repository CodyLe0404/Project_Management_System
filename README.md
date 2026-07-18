# Project Management System

This project is a web-based management dashboard for monitoring project activities, tracking task progress, and updating project financial data. It is built as a full-stack application with a Vue 3 frontend and a FastAPI backend, designed to support design teams in reviewing work status, planning schedules, and saving updates into a central database.

## What this system is for

The application helps users:

- manage project information and task breakdowns
- review project progress by main task and subtask
- update assignees, dates, costs, and remarks
- calculate and save project-related changes efficiently
- inspect KPI and department-level summaries for reporting purposes

It is especially useful for project control, execution tracking, and internal reporting workflows.

## Main flow of the application

1. The user opens the project management page.
2. The frontend loads project and item data from the backend.
3. The data is displayed in a spreadsheet-style table using Handsontable.
4. The user edits fields such as assignee, dates, cost, or remarks.
5. Changes can be saved either as normal row updates or as grouped operations such as summary/header updates.
6. The backend receives the payload and writes the changes to the database.
7. The UI refreshes so the latest project state is shown immediately.

## Core business process

The system follows a simple project-control workflow:

- Project data is loaded from the database.
- Each project is grouped by main task and displayed as a header row plus detail rows.
- Summary rows allow users to edit shared values like budget or actual cost.
- When a summary value is changed, the related detail rows are updated as well.
- The user clicks the save action to persist all tracked changes.
- The backend validates and stores the updated values.

## Key features

- Spreadsheet-style editing with Handsontable
- Header row and detail row structure for project task grouping
- Inline editing of project dates, cost, assignee, and remarks
- Summary synchronization for shared values such as actual cost
- FastAPI backend services for CRUD-style project updates
- Department and KPI views for broader reporting and monitoring
- Authentication and role-based page access support

## Technology stack

| Layer | Technology | Purpose |
| :--- | :--- | :--- |
| Frontend | Vue 3 | Main UI framework using the Composition API |
| Build tool | Vite | Fast development and production build pipeline |
| UI components | PrimeVue | UI elements and styling support |
| Table grid | Handsontable | Editable spreadsheet-style interface |
| State management | Pinia | Application state handling |
| Backend | FastAPI | API layer for loading and saving project data |
| Database | SQL Server | Persistent storage for project and task records |
| Authentication | Custom backend + frontend store | User login and permission handling |

## Project structure

```text
backend/
  main.py                 # FastAPI application, API routes, and database access
  config.ini              # Database connection configuration
  requirements.txt        # Python dependencies

src/
  pages/
    01_ProjectMgm/
      project_info.vue    # Main project management screen
    02_KpiSytem/
      deptKpi.vue         # Department KPI dashboard
  components/              # Reusable UI sections and dashboard widgets
  services/                # Frontend service calls to the backend
  stores/                  # Pinia stores for auth and shared state
  router.js                # Route definitions
  App.vue
  main.js

package.json
vite.config.js
README.md
```

## Backend API responsibilities

The backend exposes endpoints that support loading project details and saving updates. It acts as the bridge between the Vue interface and the SQL Server database.

### Main API behaviors

- load project rows with related task details
- update existing project item records
- delete rows when users remove entries
- insert new rows for added tasks
- support grouped updates for summary fields like actual cost

## How the frontend works

The project page uses Handsontable to present a large editable grid. Each row represents a task entry, while grouped header rows summarize the main task. Users can change values directly, and the page tracks which records were changed so they can be saved efficiently.

The UI is also designed to support:

- search and filter within the grid
- summary toggles to show or hide grouped data
- role-based access based on permissions
- KPI and analytics views for broader reporting

## How the backend works

The FastAPI service receives requests from the frontend and uses SQL Server connection settings from the backend configuration file. It prepares the database payloads, executes updates, and returns results to the UI.

This keeps the presentation layer separated from the data layer and makes the system easier to maintain.

## Setup and run

```bash
# Install frontend dependencies
npm install

# Install backend dependencies
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
cd ..

# Run backend server
cd backend
.venv\Scripts\activate
uvicorn main:app --reload --host 127.0.0.1 --port 8000

# Run frontend server
cd ..
npm run dev
```

## Typical user workflow

1. Open the project management screen.
2. Review the project task list and grouped summary rows.
3. Edit values such as budget, actual cost, dates, assignee, or remarks.
4. Use the save button to persist the updates.
5. Refresh or revisit the page to confirm the new values are stored.

## Summary

This project is a practical internal project management dashboard that combines a Vue-based user interface with a FastAPI backend and SQL Server data layer. It is intended to help teams manage project execution data, keep task records updated, and make reporting more transparent and efficient.
