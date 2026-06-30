from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Any, Optional, List, Generator
from datetime import datetime
from contextlib import contextmanager
import pyodbc, time
import logging
from logging.handlers import RotatingFileHandler

# -- CONFIG LOG TRACKING --
# Tạo file log lưu tại thư mục hiện tại, tối đa 5MB/file, giữ lại tối đa 5 file backup
log_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
log_handler = RotatingFileHandler('api_access.log', maxBytes=5*1024*1024, backupCount=5, encoding='utf-8')
log_handler.setFormatter(log_formatter)

logger = logging.getLogger("API_Logger")
logger.setLevel(logging.INFO)
logger.addHandler(log_handler)

# --- APP CONFIGURATION ---
app = FastAPI(title="Project Management Backend")

# Middleware ghi nhận log chi tiết cho mỗi Request
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    
    # Lấy IP của máy gọi tới (Xử lý cả trường hợp đi qua Proxy/Load Balancer nếu có)
    client_ip = request.headers.get("x-forwarded-for") or request.client.host
    
    response = await call_next(request)
    
    process_time = (time.time() - start_time) * 1000
    formatted_process_time = f"{process_time:.2f}ms"
    
    # Ghi log: Thời gian, IP, Method, URL, Status Code, Thời gian xử lý
    logger.info(f"IP: {client_ip} | Method: {request.method} | Path: {request.url.path} | Status: {response.status_code} | Duration: {formatted_process_time}")
    
    return response


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
    main_task: Optional[str] = None
    sub_task: str
    user_id: str
    assignee: Optional[str] = None
    plan_start: Optional[str] = None
    plan_end: Optional[str] = None
    actual_start: Optional[str] = None
    actual_end: Optional[str] = None
    actual_cost: Optional[float] = None
    remark: Optional[str] = None

class LoginRequest(BaseModel):
    ldapName: str
    userId: str
    password: str


class ChangePasswordRequest(BaseModel):
    userId: str
    currentPassword: str
    newPassword: str


class UserInfo(BaseModel):
    userId: str
    displayName: str
    email: str
    userConfig: list[str]


class LoginResponse(BaseModel):
    message: str
    setUserInfoStatus: int
    user: UserInfo | None = None
    
# --- APP CONFIGURATION ---
app = FastAPI(title="Project Management Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", 
                   "http://10.13.227.98:8000", 
                   "http://10.13.227.98", 
                   "http://localhost:8000", 
                   "http://10.13.227.119:8000"],
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


def encrypt_password(password: str, key: str = "LSE") -> str:
    encrypted = []

    for i, ch in enumerate(password):
        xor_value = ord(ch) ^ ord(key[i % len(key)])
        encrypted.append(f"{xor_value:02X}")

    return ''.join(encrypted)

def decrypt_password(encrypted_hex: str, key: str = "LSE") -> str:
    result = []

    for i in range(0, len(encrypted_hex), 2):
        value = int(encrypted_hex[i:i+2], 16)
        original = value ^ ord(key[(i // 2) % len(key)])
        result.append(chr(original))

    return ''.join(result)
    
def check_login(user_id: str, password: str, conn: pyodbc.Connection):

    try:
        cursor = conn.cursor()

        cursor.execute("""EXEC DS_PM_Check_User_Login ?, ?""",user_id,password)
        row = cursor.fetchone()

        if not row:
            return None
        
        cursor.execute("EXEC DS_PM_Get_Permission_Codes ?", row.permission_id)
        get_per = cursor.fetchone()
        
        if not get_per:
            return None
        
        return {
            "userId": row.username,
            "displayName": row.fullname,
            "email": row.email,
            "userConfig": get_per.permission_codes.split(';') if get_per.permission_codes else []
        }

    finally:
        cursor.close()
        
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
            INSERT INTO [Design_System].[dbo].[DS_PM_Project] 
            (project_id, project_number, project_name, active_flag, created_at, updated_at, create_by)
            VALUES (?, ?, ?, 1, getdate(), getdate(), ?)
            """,
            (
                payload.general['no'],
                payload.general['projectNumber'],
                payload.general['projectName'],
                payload.general['userId']
            )
        )

        project_id = payload.general['no']
        user_id = payload.general['userId']
        rows = []
        for item in payload.items:
            # Safe boundary check for empty strings
            subtasks_raw = item.get('subtasks', '')
            if subtasks_raw:
                for subtask in subtasks_raw.strip().split('\n'):
                    rows.append((
                        project_id,
                        item['task_name'],
                        item['main_task'],
                        subtask.strip(),
                        item['qty'],
                        item['budget'],
                        user_id
                    ))

        if rows:
            cursor.executemany(
                """
                INSERT INTO [Design_System].[dbo].[DS_PM_Item] 
                (project_id, task_no, main_task, sub_task, qty, budget, active_flag, created_at, updated_at, update_by)
                VALUES (?, ?, ?, ?, ?, ?, 1, getdate(), getdate(), ?)
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
                pi.id_item, pi.task_no, pi.main_task, pi.sub_task, pi.qty, pi.budget,
                pi.assignee, pi.[percent], pi.status,
                pi.plan_start, pi.plan_end, pi.actual_start, pi.actual_end,
                pi.actual_cost, pi.remark
            FROM [Design_System].[dbo].[DS_PM_Project] p
            JOIN [Design_System].[dbo].[DS_PM_Item] pi 
                ON p.project_id = pi.project_id
            WHERE p.active_flag = 1
            ORDER BY p.id, p.project_number, pi.id_item
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
                FROM [Design_System].[dbo].[DS_PM_Project] p
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
                SET main_task=?, sub_task=?, assignee=?, plan_start=?, plan_end=?, actual_start=?, actual_end=?, actual_cost=?, remark=?, updated_at=getdate(), update_by=?
                WHERE id_item=?
                """,
                (
                    item.main_task, item.sub_task, item.assignee, item.plan_start, item.plan_end,
                    item.actual_start, item.actual_end, item.actual_cost,
                    item.remark, item.user_id, item.item_id
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


@app.post("/Common/Login", response_model=LoginResponse)
def login(request: LoginRequest, conn: pyodbc.Connection = Depends(get_db_connection)):
    encrypted = encrypt_password(request.password)
    
    user = check_login(
        request.userId,
        encrypted,
        conn
    )

    if user is None:
        return {
            "message": "Invalid username or password",
            "setUserInfoStatus": -1,
            "user": None
        }

    return {
        "message": "Login successful",
        "setUserInfoStatus": 0,
        "user": user
    }

@app.post("/changeuserpw")
def change_user_password(request: ChangePasswordRequest, conn: pyodbc.Connection = Depends(get_db_connection)):
    current_pw = encrypt_password(request.currentPassword)
    new_pw = encrypt_password(request.newPassword)
    cursor = conn.cursor()
    try:
        # Execute the stored procedure and capture output values
        result = cursor.execute("EXEC USP_DS_PM_ChangeUserPassword ?, ?, ?", request.userId, current_pw, new_pw)

        row = result.fetchone()
        if row is None or len(row) < 2:
            raise HTTPException(status_code=500, detail="Stored procedure did not return expected response.")

        status = int(row[0])
        message = str(row[1])

        if status == 1:
            conn.commit()

        return {
            "status": status,
            "message": message
        }
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()


