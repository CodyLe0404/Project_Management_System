from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Any, Optional
from typing import List
from datetime import datetime
import pyodbc

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
    
app = FastAPI(title="Project Management Backend")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000", "http://10.13.227.60:8000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# def get_connection():
#     SERVER = '10.13.227.98,1433'  
#     DATABASE = 'Design_System'  # Updated to match your screenshot
#     USERNAME = 'hieplt'         # Matched to your login user
#     PASSWORD = 'Design@2026' 

#     # The magic string that matches SSMS behaviors on Driver 18:
#     conn_str = (
#         f'DRIVER={{ODBC Driver 18 for SQL Server}};'
#         f'SERVER={SERVER};'
#         f'DATABASE={DATABASE};'
#         f'UID={USERNAME};'
#         f'PWD={PASSWORD};'
#         f'Encrypt=no;'                 # Crucial: Tells Driver 18 not to expect a formal SSL cert
#         f'TrustServerCertificate=yes;' # Crucial: Explicitly trusts the server's self-signed identity
#         f'MultiSubnetFailover=yes;'    # Optimizes IP routing
#         f'Connection Timeout=15;'
#     )
#     try:
#         conn = pyodbc.connect(conn_str)
#     except Exception as e:
#         print(f"Lỗi kết nối: {e}")
        
#     return conn
    
# conn = get_connection()
   
@app.get("/testconnection")
def test_connection():
    SERVER = '10.13.227.98,1433'  
    DATABASE = 'Design_System'  # Updated to match your screenshot
    USERNAME = 'hieplt'         # Matched to your login user
    PASSWORD = 'Design@2026' 

    # The magic string that matches SSMS behaviors on Driver 18:
    conn_str = (
        f'DRIVER={{ODBC Driver 18 for SQL Server}};'
        f'SERVER={SERVER};'
        f'DATABASE={DATABASE};'
        f'UID={USERNAME};'
        f'PWD={PASSWORD};'
        f'Encrypt=no;'                 # Crucial: Tells Driver 18 not to expect a formal SSL cert
        f'TrustServerCertificate=yes;' # Crucial: Explicitly trusts the server's self-signed identity
        f'MultiSubnetFailover=yes;'    # Optimizes IP routing
        f'Connection Timeout=15;'
    )
    db_version = ""
    try:
        connection = pyodbc.connect(conn_str)
        print("Kết nối thành công bằng tài khoản SQL!")
        cursor = connection.cursor()
        cursor.execute("SELECT @@VERSION")
        db_version = cursor.fetchone()[0]
    except Exception as e:
        print(f"Lỗi kết nối: {e}")
    finally:
        cursor.close()
        connection.close()
    
    return {
        "status": "success",
        "message": "Connected to SQL Server Express successfully!",
        "database_version": db_version
    }

@app.get("/health")
def health_check():
    return {"status": "ok"}

# @app.post("/projects")
# def create_project(payload: ProjectPayload):
    
#     cursor = conn.cursor()

#     try:
#         # ==========================
#         # INSERT PROJECT
#         # ==========================

#         cursor.execute(
#             """
#             INSERT INTO projects (
#                 project_id,
#                 project_number,
#                 project_name
#             )
#             VALUES (?, ?, ?)
#             """,
#             (
#                 payload.general['no'],
#                 payload.general['projectNumber'],
#                 payload.general['projectName']
#             )
#         )

#         project_id = cursor.lastrowid

#         # ==========================
#         # BUILD BULK DATA
#         # ==========================

#         rows = []

#         for item in payload.items:

#             for subtask in item['subtasks'].strip().split('\n'):

#                 rows.append(
#                     (
#                         project_id,
#                         item['main_task'],
#                         subtask,
#                         item['qty'],
#                         item['budget']
#                     )
#                 )

#         # ==========================
#         # INSERT ALL TASKS
#         # ==========================

#         cursor.executemany(
#             """
#             INSERT INTO project_items (
#                 project_id,
#                 main_task,
#                 sub_task,
#                 qty,
#                 budget
#             )
#             VALUES (?, ?, ?, ?, ?)
#             """,
#             rows
#         )

#         conn.commit()

#         return {
#             "success": True,
#             "id": project_id,
#             "total_rows": len(rows)
#         }

#     except Exception as e:

#         conn.rollback()

#         raise HTTPException(
#             status_code=500,
#             detail=str(e)
#         )

# @app.get("/projects/details")
# def get_project_details():

#     cursor = conn.cursor()

#     cursor.execute("""
#         SELECT
#             p.id,
#             p.project_id,
#             p.project_number,
#             p.project_name,

#             pi.id as item_id,

#             pi.main_task,
#             pi.sub_task,

#             pi.qty,
#             pi.budget,

#             pi.assignee,
#             pi.percent,
#             pi.status,

#             pi.plan_start,
#             pi.plan_end,

#             pi.actual_start,
#             pi.actual_end,

#             pi.actual_cost,

#             pi.remark

#         FROM projects p
#         JOIN project_items pi
#             ON p.id = pi.project_id

#         ORDER BY
#             p.project_id, 
#             p.project_number,
#             pi.main_task,
#             pi.sub_task
#     """)

#     columns = [col[0] for col in cursor.description]

#     rows = [
#         dict(zip(columns, row))
#         for row in cursor.fetchall()
#     ]

#     return rows


# def parse_datetime(value: Optional[str]) -> Optional[datetime]:
#     if not value:
#         return None

#     for fmt in ("%Y-%m-%d", "%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S"):
#         try:
#             return datetime.strptime(value, fmt)
#         except ValueError:
#             continue

#     return None


# def get_project_status(plan_start: Optional[datetime], plan_end: Optional[datetime], actual_start: Optional[datetime], actual_end: Optional[datetime]) -> str:
#     if not plan_start and not plan_end:
#         return 'No plan'

#     if not actual_start and not actual_end:
#         return 'Not yet start'

#     if actual_start and not actual_end:
#         return 'On going'

#     if actual_end:
#         if plan_end and actual_end > plan_end:
#             return 'Delay'

#         if plan_end and actual_end < plan_end:
#             return 'Ahead of schedule'

#         return 'On Time'

#     return 'Not yet start'


# @app.get("/projects/summary")
# def get_project_summary():
#     cursor = conn.cursor()

#     cursor.execute(
#         """
#         SELECT
#             p.id as project_id,
#             pi.plan_start,
#             pi.plan_end,
#             pi.actual_start,
#             pi.actual_end
#         FROM projects p
#         LEFT JOIN project_items pi
#             ON p.id = pi.project_id
#         ORDER BY p.id
#         """
#     )

#     rows = cursor.fetchall()
#     grouped = {}

#     for project_id, plan_start, plan_end, actual_start, actual_end in rows:
#         if project_id not in grouped:
#             grouped[project_id] = []

#         grouped[project_id].append({
#             'plan_start': parse_datetime(plan_start),
#             'plan_end': parse_datetime(plan_end),
#             'actual_start': parse_datetime(actual_start),
#             'actual_end': parse_datetime(actual_end)
#         })

#     counts = {
#         'total_projects': len(grouped),
#         'completed_projects': 0,
#         'on_going_projects': 0,
#         'ahead_of_schedule_projects': 0,
#         'on_time_projects': 0,
#         'delayed_projects': 0,
#         'not_yet_start_projects': 0,
#         'no_plan_projects': 0
#     }

#     for project_rows in grouped.values():
#         plan_start = min((row['plan_start'] for row in project_rows if row['plan_start']), default=None)
#         plan_end = max((row['plan_end'] for row in project_rows if row['plan_end']), default=None)
#         actual_start = min((row['actual_start'] for row in project_rows if row['actual_start']), default=None)
#         actual_end = max((row['actual_end'] for row in project_rows if row['actual_end']), default=None)

#         status = get_project_status(plan_start, plan_end, actual_start, actual_end)

#         if status == 'No plan':
#             counts['no_plan_projects'] += 1
#         elif status == 'Not yet start':
#             counts['not_yet_start_projects'] += 1
#         elif status == 'On going':
#             counts['on_going_projects'] += 1
#         elif status == 'Ahead of schedule':
#             counts['ahead_of_schedule_projects'] += 1
#             counts['completed_projects'] += 1
#         elif status == 'On Time':
#             counts['on_time_projects'] += 1
#             counts['completed_projects'] += 1
#         elif status == 'Delay':
#             counts['delayed_projects'] += 1
#             counts['completed_projects'] += 1

#     return counts


# @app.put("/project-items/bulk-update")
# def bulk_update(items: List[ProjectItemUpdate]):

#     cursor = conn.cursor()
#     try:

#         for item in items:
            
#             cursor.execute(
#                 """
#                 UPDATE project_items
#                 SET
#                     assignee=?,
#                     plan_start=?,
#                     plan_end=?,
#                     actual_start=?,
#                     actual_end=?,
#                     actual_cost=?,
#                     remark=?
#                 WHERE id=?
#                 """,
#                 (
#                     item.assignee,
#                     item.plan_start,
#                     item.plan_end,
#                     item.actual_start,
#                     item.actual_end,
#                     item.actual_cost,
#                     item.remark,
#                     item.item_id
#                 )
#             )

#         conn.commit()

#         return {
#             "success": True,
#             "updated": len(items)
#         }

#     except Exception as e:

#         conn.rollback()

#         raise HTTPException(
#             status_code=500,
#             detail=str(e)
#         )
        
