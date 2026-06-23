from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Any, Optional, List, Generator
from datetime import datetime
from contextlib import contextmanager
import pyodbc

# --- DATABASE CONNECTION UTILITY ---
def get_db_connection() -> Generator[pyodbc.Connection, None, None]:
    SERVER = '10.13.227.98,1433'  
    DATABASE = 'Design_System'  
    USERNAME = 'hieplt'         
    PASSWORD = 'Design@2026' 

    conn_str = (
        f'DRIVER={{ODBC Driver 18 for SQL Server}};'
        f'SERVER={SERVER};'
        f'DATABASE={DATABASE};'
        f'UID={USERNAME};'
        f'PWD={PASSWORD};'
        f'Encrypt=no;'                 
        f'TrustServerCertificate=yes;' 
        # f'MultiSubnetFailover=yes;'    
        # f'Connection Timeout=15;'
    )
    
    conn = None
    try:
        conn = pyodbc.connect(conn_str)
        yield conn
    except Exception as e:
        print(f"Database connection error: {e}")
        raise HTTPException(status_code=500, detail=f"Database connection error: {str(e)}")
    finally:
        if conn:
            conn.close()

# --- PYDANTIC SCHEMAS ---
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

# --- APP CONFIGURATION ---
app = FastAPI(title="Project Management Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", 
                   "http://10.13.227.98:8000", 
                   "http://10.13.227.98", 
                   "http://localhost:8000", 
                   "http://10.13.227.60:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- HELPER FUNCTIONS ---
def parse_datetime(value: Optional[str]) -> Optional[datetime]:
    if not value:
        return None
    for fmt in ("%Y-%m-%d", "%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S"):
        try:
            return datetime.strptime(value, fmt)
        except ValueError:
            continue
    return None

def get_project_status(
    plan_start: Optional[datetime], 
    plan_end: Optional[datetime], 
    actual_start: Optional[datetime], 
    actual_end: Optional[datetime]
) -> str:
    if not plan_start and not plan_end:
        return 'No plan'
    if not actual_start and not actual_end:
        return 'Not yet start'
    if actual_start and not actual_end:
        return 'On going'
    if actual_end:
        if plan_end and actual_end > plan_end:
            return 'Delay'
        if plan_end and actual_end < plan_end:
            return 'Ahead of schedule'
        return 'On Time'
    return 'Not yet start'

# --- API ENDPOINTS ---

@app.get("/testconnection")
def test_connection(conn: pyodbc.Connection = Depends(get_db_connection)):
    db_version = ""
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT @@VERSION")
        db_version = cursor.fetchone()[0]
        cursor.close()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Query failed: {str(e)}")
    
    return {
        "status": "success",
        "message": "Connected to SQL Server Express successfully!",
        "database_version": db_version
    }

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/projects")
def create_project(payload: ProjectPayload, conn: pyodbc.Connection = Depends(get_db_connection)):
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO [Design_System].[dbo].[Project] (project_id, project_number, project_name, active_flag, created_at, updated_at)
            VALUES (?, ?, ?, 1, getdate(), getdate())
            """,
            (
                payload.general['no'],
                payload.general['projectNumber'],
                payload.general['projectName']
            )
        )

        project_id = payload.general['no']
        task_no = payload.general['taskNo']
        rows = []
        for item in payload.items:
            # Safe boundary check for empty strings
            subtasks_raw = item.get('subtasks', '')
            if subtasks_raw:
                for subtask in subtasks_raw.strip().split('\n'):
                    rows.append((
                        project_id,
                        task_no,
                        item['main_task'],
                        subtask.strip(),
                        item['qty'],
                        item['budget']
                    ))

        if rows:
            cursor.executemany(
                """
                INSERT INTO [Design_System].[dbo].[DS_PM_Item] (project_id, task_no, main_task, sub_task, qty, budget, active_flag, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, 1, getdate(), getdate())
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
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()

@app.get("/projects/details")
def get_project_details(conn: pyodbc.Connection = Depends(get_db_connection)):
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT
                p.id, p.project_id, p.project_number, p.project_name,
                pi.item_id, pi.task_no, pi.main_task, pi.sub_task, pi.qty, pi.budget,
                pi.assignee, pi.[percent], pi.status,
                pi.plan_start, pi.plan_end, pi.actual_start, pi.actual_end,
                pi.actual_cost, pi.remark
            FROM [Design_System].[dbo].[Project] p
            JOIN [Design_System].[dbo].[DS_PM_Item] pi ON p.project_id = pi.project_id
            WHERE p.active_flag = 1
            ORDER BY p.project_id, p.project_number, pi.id_item
        """)

        columns = [col[0] for col in cursor.description]
        rows = [dict(zip(columns, row)) for row in cursor.fetchall()]
        return rows
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()

@app.get("/projects/summary")
def get_project_summary(conn: pyodbc.Connection = Depends(get_db_connection)):
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            SELECT p.id, p.project_id, pi.plan_start, pi.plan_end, pi.actual_start, pi.actual_end
                FROM [Design_System].[dbo].[Project] p
                LEFT JOIN [Design_System].[dbo].[DS_PM_Item] pi 
                    ON p.project_id = pi.project_id
                ORDER BY p.id
            """
        )

        rows = cursor.fetchall()
        grouped = {}

        for id, project_id, plan_start, plan_end, actual_start, actual_end in rows:
            if project_id not in grouped:
                grouped[project_id] = []

            grouped[project_id].append({
                'plan_start': parse_datetime(str(plan_start) if plan_start else None),
                'plan_end': parse_datetime(str(plan_end) if plan_end else None),
                'actual_start': parse_datetime(str(actual_start) if actual_start else None),
                'actual_end': parse_datetime(str(actual_end) if actual_end else None)
            })

        counts = {
            'total_projects': len(grouped),
            'completed_projects': 0,
            'on_going_projects': 0,
            'ahead_of_schedule_projects': 0,
            'on_time_projects': 0,
            'delayed_projects': 0,
            'not_yet_start_projects': 0,
            'no_plan_projects': 0
        }

        for project_rows in grouped.values():
            plan_start_min = min((row['plan_start'] for row in project_rows if row['plan_start']), default=None)
            plan_end_max = max((row['plan_end'] for row in project_rows if row['plan_end']), default=None)
            actual_start_min = min((row['actual_start'] for row in project_rows if row['actual_start']), default=None)
            actual_end_max = max((row['actual_end'] for row in project_rows if row['actual_end']), default=None)

            status = get_project_status(plan_start_min, plan_end_max, actual_start_min, actual_end_max)

            if status == 'No plan':
                counts['no_plan_projects'] += 1
            elif status == 'Not yet start':
                counts['not_yet_start_projects'] += 1
            elif status == 'On going':
                counts['on_going_projects'] += 1
            elif status == 'Ahead of schedule':
                counts['ahead_of_schedule_projects'] += 1
                counts['completed_projects'] += 1
            elif status == 'On Time':
                counts['on_time_projects'] += 1
                counts['completed_projects'] += 1
            elif status == 'Delay':
                counts['delayed_projects'] += 1
                counts['completed_projects'] += 1

        return counts
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()

@app.put("/project-items/bulk-update")
def bulk_update(items: List[ProjectItemUpdate], conn: pyodbc.Connection = Depends(get_db_connection)):
    cursor = conn.cursor()
    try:
        for item in items:
            cursor.execute(
                """
                UPDATE [Design_System].[dbo].[DS_PM_Item]
                SET assignee=?, plan_start=?, plan_end=?, actual_start=?, actual_end=?, actual_cost=?, remark=?
                WHERE id=?
                """,
                (
                    item.assignee, item.plan_start, item.plan_end,
                    item.actual_start, item.actual_end, item.actual_cost,
                    item.remark, item.item_id
                )
            )

        conn.commit()
        return {
            "success": True,
            "updated": len(items)
        }
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
