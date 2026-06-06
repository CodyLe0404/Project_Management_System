from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Any, Optional
import sqlite3
import json
import os
from typing import List
import logging

class ProjectRow(BaseModel):
    data: dict[str, Any]

class ProjectRowsPayload(BaseModel):
    rows: list[dict[str, Any]]


class ProjectPayload(BaseModel):
    general: dict[str, Any]
    items: list[dict[str, Any]]

class ProjectItemUpdate(BaseModel):
    item_id: int
    assignee: Optional[str] = None
    plan_start: Optional[str] = None
    plan_end: Optional[str] = None
    actual_start: Optional[str] = None
    actual_end: Optional[str] = None
    actual_cost: Optional[float] = None
    remark: Optional[str] = None
    
BASE_DIR = os.path.dirname(__file__)
DB_PATH = os.path.join(BASE_DIR, "projects.db")

app = FastAPI(title="Project Management Backend")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)


conn = sqlite3.connect(DB_PATH, check_same_thread=False)
conn.execute(
    """
    CREATE TABLE IF NOT EXISTS projects (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        project_id INTEGER UNIQUE NOT NULL,
        project_number TEXT NOT NULL,
        project_name TEXT NOT NULL
    )
    """
)
conn.commit()

logger = logging.getLogger("uvicorn.error")

@app.get("/health")
def health_check():
    return {"status": "ok"}

# @app.post("/projectss")
# def create_projects(payload: ProjectPayload):
#     rows = []
#     for item in payload.items:

#         for subtask in item['subtasks'].split('\n'):
#             print("Processing item:", item['main_task'], "Subtask:", subtask)
#             rows.append(
#                 ( 
#                     item['main_task'],
#                     subtask,
#                     item['qty'],
#                     item['budget']
#                 )
#             )
    

@app.post("/projects")
def create_project(payload: ProjectPayload):
    cursor = conn.cursor()

    try:

        # ==========================
        # INSERT PROJECT
        # ==========================

        cursor.execute(
            """
            INSERT INTO projects (
                project_id,
                project_number,
                project_name
            )
            VALUES (?, ?, ?)
            """,
            (
                payload.general['no'],
                payload.general['projectNumber'],
                payload.general['projectName']
            )
        )

        project_id = cursor.lastrowid

        # ==========================
        # BUILD BULK DATA
        # ==========================

        rows = []

        for item in payload.items:

            for subtask in item['subtasks'].split('\n').strip():

                rows.append(
                    (
                        project_id,
                        item['main_task'],
                        subtask,
                        item['qty'],
                        item['budget']
                    )
                )

        # ==========================
        # INSERT ALL TASKS
        # ==========================

        cursor.executemany(
            """
            INSERT INTO project_items (
                project_id,
                main_task,
                sub_task,
                qty,
                budget
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            rows
        )

        conn.commit()

        return {
            "success": True,
            "id": project_id,
            "total_rows": len(rows)
        }

    except Exception as e:

        conn.rollback()

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

@app.get("/projects/details")
def get_project_details():

    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            p.id,
            p.project_id,
            p.project_number,
            p.project_name,

            pi.id as item_id,

            pi.main_task,
            pi.sub_task,

            pi.qty,
            pi.budget,

            pi.assignee,
            pi.percent,
            pi.status,

            pi.plan_start,
            pi.plan_end,

            pi.actual_start,
            pi.actual_end,

            pi.actual_cost,

            pi.remark

        FROM projects p
        JOIN project_items pi
            ON p.id = pi.project_id

        ORDER BY
            p.project_id, 
            p.project_number,
            pi.main_task,
            pi.sub_task
    """)

    columns = [col[0] for col in cursor.description]

    rows = [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

    return rows

@app.put("/project-items/bulk-update")
def bulk_update(items: List[ProjectItemUpdate]):

    cursor = conn.cursor()
    try:

        for item in items:
            
            cursor.execute(
                """
                UPDATE project_items
                SET
                    assignee=?,
                    plan_start=?,
                    plan_end=?,
                    actual_start=?,
                    actual_end=?,
                    actual_cost=?,
                    remark=?
                WHERE id=?
                """,
                (
                    item.assignee,
                    item.plan_start,
                    item.plan_end,
                    item.actual_start,
                    item.actual_end,
                    item.actual_cost,
                    item.remark,
                    item.item_id
                )
            )

        conn.commit()

        return {
            "success": True,
            "updated": len(items)
        }

    except Exception as e:

        conn.rollback()

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
        
