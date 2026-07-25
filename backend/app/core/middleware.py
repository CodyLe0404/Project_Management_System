import logging, json
import time
from fastapi import Request
from datetime import datetime
from pathlib import Path

# -- CONFIG LOG TRACKING --
# Disable file logging to api_access.log and keep logging quiet
logger = logging.getLogger("API_Logger")
logger.setLevel(logging.INFO)
logger.propagate = False

daily_logger = logging.getLogger("PM_Tracker")
daily_logger.setLevel(logging.INFO)
current_log_date = None
daily_handler = None


BASE_DIR = Path(__file__).resolve().parent.parent
LOG_DIR = BASE_DIR / "log"


def get_daily_handler():
    global current_log_date, daily_handler
    today = datetime.now().date()

    if daily_handler is None or current_log_date != today:
        if daily_handler is not None:
            daily_logger.removeHandler(daily_handler)
            daily_handler.close()

        # 1. Tạo đường dẫn thư mục: backend/app/log/YYYY/MM
        year_str = today.strftime("%Y")
        month_str = today.strftime("%m")
        target_dir = LOG_DIR / year_str / month_str

        # 2. Tự động tạo thư mục nếu chưa tồn tại (bao gồm cả thư mục cha)
        target_dir.mkdir(parents=True, exist_ok=True)

        # 3. Tạo đường dẫn file đầy đủ
        filename = f"PM_log_tracking_{today.strftime('%Y_%m_%d')}.log"
        log_file_path = target_dir / filename

        # 4. Gắn đường dẫn đã tạo vào FileHandler
        daily_handler = logging.FileHandler(log_file_path, encoding="utf-8")
        daily_handler.setFormatter(logging.Formatter("%(message)s"))
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

def register_request_logging(app) -> None:
    @app.middleware("http")
    async def log_requests(request: Request, call_next):
        if request.method == "OPTIONS":
            return await call_next(request)
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
