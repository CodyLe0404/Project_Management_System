import json

from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Any, Optional, List, Generator
from datetime import datetime, date
import pyodbc, time
import logging
from logging.handlers import RotatingFileHandler
import configparser

# -- CONFIG LOG TRACKING --
# Tạo file log lưu tại thư mục hiện tại, mỗi ngày tạo file mới
log_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
log_handler = RotatingFileHandler('api_access.log', maxBytes=5*1024*1024, backupCount=5, encoding='utf-8')
log_handler.setFormatter(log_formatter)

logger = logging.getLogger("API_Logger")
logger.setLevel(logging.INFO)
logger.addHandler(log_handler)

daily_logger = logging.getLogger("PM_Tracker")
daily_logger.setLevel(logging.INFO)
current_log_date = None
daily_handler = None


def get_daily_handler():
    global current_log_date, daily_handler
    today = datetime.now().date()
    if daily_handler is None or current_log_date != today:
        if daily_handler is not None:
            daily_logger.removeHandler(daily_handler)
            daily_handler.close()

        filename = f"PM_log_tracking_{today.strftime('%Y_%m_%d')}.log"
        daily_handler = logging.FileHandler(filename, encoding='utf-8')
        daily_handler.setFormatter(logging.Formatter('%(message)s'))
        daily_logger.addHandler(daily_handler)
        current_log_date = today

    return daily_handler


def log_daily(message: str, level: int = logging.INFO):
    get_daily_handler()
    timestamped_message = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {message}"
    daily_logger.log(level, timestamped_message)

def extract_user_from_request(request: Request, body_text: str) -> str:
    user_id = None

    if 'userId' in request.query_params:
        user_id = request.query_params.get('userId')
    elif 'user_id' in request.query_params:
        user_id = request.query_params.get('user_id')

    if not user_id and body_text:
        try:
            payload = json.loads(body_text)
            if isinstance(payload, list) and payload:
                payload = payload[0]

            if isinstance(payload, dict):
                user_id = payload.get('userId') or payload.get('user_id') or payload.get('user')
        except json.JSONDecodeError:
            user_id = None

    return user_id or 'anonymous'

# --- APP CONFIGURATION ---
app = FastAPI(title="Project Management Backend")

# Middleware ghi nhận log chi tiết cho mỗi Request
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    body_bytes = await request.body()
    body_text = body_bytes.decode('utf-8', errors='replace') if body_bytes else ''
    user_id = extract_user_from_request(request, body_text)

    # Lấy IP của máy gọi tới (Xử lý cả trường hợp đi qua Proxy/Load Balancer nếu có)
    client_ip = request.headers.get("x-forwarded-for") or request.client.host
    
    response = await call_next(request)
    
    process_time = (time.time() - start_time) * 1000
    formatted_process_time = f"{process_time:.2f}ms"
    log_message = (
        f"IP: {client_ip} | User: {user_id} | Method: {request.method} | "
        f"Path: {request.url.path} | Status: {response.status_code} | Duration: {formatted_process_time}"
    )

    logger.info(log_message)
    log_daily(log_message)
    
    return response


# --- DATABASE CONNECTION UTILITY ---
def get_db_connection() -> Generator[pyodbc.Connection, None, None]:
    config = configparser.ConfigParser()
    config.read('config.ini')

    SERVER = config.get('DATABASE', 'server')
    DATABASE = config.get('DATABASE', 'database')
    USERNAME = config.get('DATABASE', 'username')
    PASSWORD = config.get('DATABASE', 'password')

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
    qty: Optional[int] = None
    user_id: str
    assignee: Optional[str] = None
    process: Optional[float] = None
    status: Optional[str] = None
    plan_start: Optional[str] = None
    plan_end: Optional[str] = None
    actual_start: Optional[str] = None
    actual_end: Optional[str] = None
    actual_cost: Optional[float] = None
    remark: Optional[str] = None

class DeleteRowRequest(BaseModel):
    item_ids: str
    user_id: str

class InsertRowRequest(BaseModel):
    user_id: str
    project_id: Optional[str] = None
    task_no: int
    main_task: str
    sub_task: Optional[str] = None
    qty: Optional[int] = None
    budget: Optional[float] = None
    actual_cost: Optional[float] = None
    assignee: Optional[str] = None
    plan_start: Optional[date] = None
    plan_end: Optional[date] = None
    actual_start: Optional[date] = None
    actual_end: Optional[date] = None
    order_no: Optional[int] = None
    
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

def check_duplicate_task(cursor, project_id, items):
    main_task_existed = []
    for item in items:
        main_task = item['main_task']
        cursor.execute("EXEC USP_DS_Check_Duplicate_Task ?, ?", project_id, main_task)
        result = cursor.fetchone()
        if result[0] != 'Not existed':
            main_task_existed.append(main_task)
    
    # If the list has data, format and return the message
    if main_task_existed:
        duplicate_tasks_str = ", ".join(main_task_existed)
        return f"Main task: {duplicate_tasks_str} existed"
        
    return []


@app.post("/projects")
def create_project(payload: ProjectPayload, conn: pyodbc.Connection = Depends(get_db_connection)):
    cursor = conn.cursor()
    project_id = payload.general['no']
    user_id = payload.general['userId']
    try:
        
        duplicate_task_message = check_duplicate_task(cursor, project_id, payload.items)
        if duplicate_task_message:
            return {
                "success": False,
                "message": duplicate_task_message,
                "id": project_id
            }
            
        cursor.execute("EXEC [Design_System].[dbo].[USP_PM_Create_Project] ?, ?, ?, ?",
            payload.general['no'],
            payload.general['projectNumber'],
            payload.general['projectName'],
            payload.general['userId']
        )

        result = cursor.fetchone()
        # Kiểm tra nếu SP có trả về dữ liệu và lấy message (giả sử message ở cột đầu tiên)
        sp_message = result[0] if result else 'Project created fail'

        # Nếu thất bại, dừng lại và trả về thông báo lỗi luôn, không chạy tiếp bên dưới
        if sp_message != 'Project created successfully':
            return {
                "success": False,
                "message": sp_message,
                "id": project_id
            }
        
        log_daily(f"[{user_id}] Create | Project ID: {project_id} | Project Name: {payload.general['projectName']} | Message: {sp_message}")
            
        rows = []
        for item in payload.items:
            # Safe boundary check for empty strings
            subtasks_raw = item.get('subtasks', '')
            if subtasks_raw:
                order_no = 0
                for subtask in subtasks_raw.strip().split('\n'):
                    order_no += 1
                    rows.append((
                        project_id,
                        item['task_name'],
                        item['main_task'],
                        subtask.strip(),
                        item['qty'],
                        order_no,
                        item['budget'],
                        user_id
                    ))

        if rows:
            cursor.executemany(
                """
                INSERT INTO [Design_System].[dbo].[DS_PM_Item] 
                (project_id, task_no, main_task, sub_task, qty, ord_no, budget, active_flag, created_at, updated_at, update_by)
                VALUES (?, ?, ?, ?, ?, ?, ?, 1, getdate(), getdate(), ?)
                """,
                rows
            )

        conn.commit()
        
        log_daily(f"[{user_id}] Insert | Total item: {len(rows)} | Project ID: {project_id} successfully.")
        
        return {
            "success": True,
            "message": sp_message,
            "id": project_id
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
        cursor.execute("EXEC [Design_System].[dbo].[USP_PM_Get_Project_Detail]")
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
        cursor.execute("EXEC [Design_System].[dbo].[USP_PM_Get_Project_Summary]")
        rows = cursor.fetchall()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
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


@app.post("/project-items/delete")
def delete_project_row(payload: DeleteRowRequest, conn: pyodbc.Connection = Depends(get_db_connection)):
    cursor = conn.cursor()
    try:
        result = cursor.execute(
            "EXEC USP_DS_PM_Delete_Item_Data ?, ?",
            payload.item_ids,
            payload.user_id
        ).fetchone()
        conn.commit()

        status = str(result[0]) if result else ''
        
        log_daily(f"[{payload.user_id}] Delete | items: {payload.item_ids} | Result: {status}")
        
        return {
            "success": status.upper() == 'SUCCESS',
            "result": status
        }
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()


@app.post("/project-items/insert")
def insert_project_row(payload: List[InsertRowRequest], conn: pyodbc.Connection = Depends(get_db_connection)):
    cursor = conn.cursor()
    success_count = 0
    results_summary = []

    try:
        # Lặp qua từng item trong list dữ liệu truyền vào
        for item in payload:
            cursor.execute(
                "EXEC USP_PM_Insert_Row_Data ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?", 
                item.project_id, 
                item.task_no,
                item.main_task,
                item.sub_task,
                item.qty,
                item.budget,
                item.actual_cost or 0,
                item.assignee or '',
                item.user_id,
                item.plan_start,
                item.plan_end,
                item.actual_start,
                item.actual_end,
                item.order_no
            )
            # Lấy kết quả trả về của từng dòng (nếu SP có sinh kết quả)
            row_result = cursor.fetchone()
            status = str(row_result[0]) if row_result else 'UNKNOWN'
            results_summary.append({"task_no": item.task_no, "status": status})
            
            log_daily(f"[{item.user_id}] Insert | Task No: {item.task_no} | Order No: {item.order_no} | Result: {status}")
            
            if status.upper() == 'SUCCESS':
                success_count += 1

        # Commit toàn bộ sau khi chạy lỗi/thành công hết vòng lặp
        conn.commit()

    except Exception as e:
        # Rollback lại toàn bộ nếu có bất kỳ dòng nào bị lỗi hệ thống/DB
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
    
    log_daily(f"[{payload[0].user_id if payload else 'unknown'}] Insert | Successfully inserted {success_count}/{len(payload)} rows.")
        
    return {
        "success": success_count == len(payload),
        "message": f"Successfully insert {success_count}/{len(payload)} rows.",
        "details": results_summary
    }


@app.put("/project-items/bulk-update")
def bulk_update(items: List[ProjectItemUpdate], conn: pyodbc.Connection = Depends(get_db_connection)):
    cursor = conn.cursor()
    # 🚀 Bật tính năng tối ưu hóa tốc độ gửi tham số hàng loạt cho pyodbc
    cursor.fast_executemany = True
    
    try:
        # 1. Chuyển đổi danh sách objects (Pydantic models) thành danh sách các tuples
        rows = []
        for item in items:
            rows.append((
                item.main_task,     # ? số 1
                item.sub_task,      # ? số 2
                item.qty,           # ? số 3
                item.assignee,      # ? số 4
                item.process,
                item.status,
                item.plan_start,    # ? số 5
                item.plan_end,      # ? số 6
                item.actual_start,  # ? số 7
                item.actual_end,    # ? số 8
                item.actual_cost,   # ? số 9
                item.remark,        # ? số 10
                item.user_id,       # ? số 11 (update_by)
                item.item_id        # ? số 12 (WHERE id_item=?)
            ))

        # 2. Thực thi cập nhật hàng loạt nếu có dữ liệu
        if rows:
            cursor.executemany(
                """
                UPDATE [Design_System].[dbo].[DS_PM_Item]
                SET main_task=?, sub_task=?, qty=?, assignee=?, [percent]=?, status=?, plan_start=?, plan_end=?, 
                    actual_start=?, actual_end=?, actual_cost=?, remark=?, updated_at=getdate(), update_by=?
                WHERE id_item=?
                """,
                rows
            )

        # 3. Commit một lần duy nhất cho toàn bộ các dòng được cập nhật
        conn.commit()
        
        log_daily(f"[{items[0].user_id if items else 'unknown'}] Update | Bulk update completed. Total items updated: {len(items)}.")
        
        return {
            "success": True,
            "updated": len(items)
        }
    except Exception as e:
        # Nếu bất kỳ dòng nào lỗi, hủy bỏ (rollback) toàn bộ tiến trình để đảm bảo tính nhất quán
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
        log_daily(f"[{request.userId}] Login | Failed")
        return {
            "message": "Invalid username or password",
            "setUserInfoStatus": -1,
            "user": None
        }

    log_daily(f"[{request.userId}] Login | Successful")
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
            log_daily(f"[{request.userId}] Change Password | Successfully changed password")
        else:
            log_daily(f"[{request.userId}] Change Password | Failed to change password: {message}")

        return {
            "status": status,
            "message": message
        }
    except Exception as e:
        conn.rollback()
        log_daily(f"[{request.userId}] Change Password | Error occurred while changing password: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()


