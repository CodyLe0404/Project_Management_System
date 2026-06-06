# Project Management System

A task and project management dashboard built with **Vue 3 + Vite** on the frontend and **FastAPI + SQLite** on the backend.

This repo focuses on managing project items, updating project costs, and saving task details in a local SQLite database.

## Key Features

- **Handsontable project grid** with editable task fields.
- **Header row `actual_cost` editing** and propagation into the detail row below.
- **Bulk persistence** of project item fields via backend APIs.
- **FastAPI backend** using SQLite for local storage.
- **Data-driven frontend routes** using `vite-plugin-pages` and custom `_meta.json` metadata.

## Technology Stack

| Category | Technology | Description |
| :--- | :--- | :--- |
| **Frontend** | Vue 3 | Composition API + `<script setup>` |
| **Build Tool** | Vite | Fast development server and production build |
| **UI Library** | PrimeVue | Enterprise-ready UI components |
| **Table** | Handsontable | Spreadsheet-style editable grid |
| **State** | Pinia | Vue state management |
| **Backend** | FastAPI | Python web API framework |
| **Database** | SQLite | Local file-based persistence |

## Project Structure

```text
backend/
  main.py                 # FastAPI application and SQLite integration
  requirements.txt        # Python dependencies
  projects.db             # SQLite database file (created automatically)

src/
  pages/
    ProjectMgm/
      project_info.vue    # Main project management page
  services/
    projectService.js     # Frontend API calls
  stores/                 # Pinia stores
  utils/                  # Utility helpers
  App.vue
  main.js

package.json
vite.config.js
README.md
```

## Backend APIs

### `GET /projects/details`
Returns all projects joined with their `project_items` rows.

### `PUT /project-items/bulk-update`
Updates project item fields, including:
- `assignee`
- `plan_start`
- `plan_end`
- `actual_start`
- `actual_end`
- `actual_cost`
- `remark`

### `PUT /project-items/update-by-keys`
Updates `actual_cost` in `project_items` using the project keys:
- `project_id`
- `project_number`
- `project_name`
- `main_task`

This endpoint supports the workflow where the header row `actual_cost` value is entered and then persisted into the matching detail row.

## Installation & Setup

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

## Usage

1. Open the project management page.
2. Edit the header row's **Actual Cost** cell.
3. The value is copied into the row immediately below.
4. Click **CALCULATE & SAVE** to persist changes to SQLite.

## Notes

- The project uses a local SQLite database stored in `backend/projects.db`.
- `src/pages/ProjectMgm/project_info.vue` contains the Handsontable setup and save logic.
- `src/services/projectService.js` handles the API calls.
- `backend/main.py` contains the FastAPI routes and database updates.

## Summary
This project is a lightweight management dashboard for project items, with editable actual costs and a backend that saves data into SQLite.
