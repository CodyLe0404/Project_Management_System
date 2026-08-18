from __future__ import annotations

from datetime import datetime
from typing import Any

from app.core.exceptions import ServiceError
from app.core.middleware import log_daily
from app.repositories.project_repository import ProjectRepository
from app.services.personal_kpi_builder import PersonalKPIBuilder
from app.services.dept_kpi_builder import DeptKPIBuilder
from app.services.dashboard_builder import DashboardBuilder
from app.utils.security import decrypt_password, encrypt_password


class ProjectService:
    def __init__(self, repository: ProjectRepository) -> None:
        self.repository = repository

    def create_project(self, payload: dict[str, Any], user_id: str) -> dict[str, Any]:
        duplicate_tasks = self.repository.check_duplicate_task(payload["general"]["no"], payload["items"])
        if duplicate_tasks:
            raise ServiceError(
                f"Main task: {', '.join(duplicate_tasks)} existed",
                status_code=400,
            )

        sp_message = self.repository.create_project(
            payload["general"]["no"],
            payload["general"]["projectNumber"],
            payload["general"]["projectName"],
            user_id,
        )
        if sp_message != "Project created successfully":
            raise ServiceError(sp_message, status_code=400)
        
        log_daily(f"[{user_id}] Create | Project ID: {payload["general"]["no"]} | Project Name: {payload["general"]["projectName"]} | Message: {sp_message}")
        
        rows: list[tuple[Any, ...]] = []
        for item in payload["items"]:
            subtasks_raw = item.get("subtasks", "")
            if subtasks_raw:
                order_no = 0
                for subtask in subtasks_raw.strip().split("\n"):
                    order_no += 1
                    rows.append(
                        (
                            payload["general"]["no"],
                            item["task_name"],
                            item["main_task"],
                            subtask.strip(),
                            item["qty"],
                            order_no,
                            item["budget"],
                            user_id,
                        )
                    )

        self.repository.insert_project_items(payload["general"]["no"], rows, user_id)
        log_daily(f"[{user_id}] Insert | Total item: {len(rows)} | Project ID: {payload["general"]["no"]} successfully.")
        return {"success": True, "message": sp_message, "id": payload["general"]["no"]}

    def get_project_details(self) -> list[dict[str, Any]]:
        return self.repository.get_project_details()

    def get_project_summary(self) -> dict[str, int]:
        rows = self.repository.get_project_summary()
        grouped: dict[str, list[dict[str, Any]]] = {}

        for _, project_id, plan_start, plan_end, actual_start, actual_end in rows:
            grouped.setdefault(project_id, []).append(
                {
                    "plan_start": self._parse_datetime(str(plan_start) if plan_start else None),
                    "plan_end": self._parse_datetime(str(plan_end) if plan_end else None),
                    "actual_start": self._parse_datetime(str(actual_start) if actual_start else None),
                    "actual_end": self._parse_datetime(str(actual_end) if actual_end else None),
                }
            )

        counts = {
            "total_projects": len(grouped),
            "completed_projects": 0,
            "on_going_projects": 0,
            "ahead_of_schedule_projects": 0,
            "on_time_projects": 0,
            "delayed_projects": 0,
            "not_yet_start_projects": 0,
            "no_plan_projects": 0,
        }

        for project_rows in grouped.values():
            plan_start_min = min((row["plan_start"] for row in project_rows if row["plan_start"]), default=None)
            plan_end_max = max((row["plan_end"] for row in project_rows if row["plan_end"]), default=None)
            actual_start_min = min((row["actual_start"] for row in project_rows if row["actual_start"]), default=None)
            actual_end_max = max((row["actual_end"] for row in project_rows if row["actual_end"]), default=None)
            status = self._get_project_status(plan_start_min, plan_end_max, actual_start_min, actual_end_max)

            if status == "No plan":
                counts["no_plan_projects"] += 1
            elif status == "Not yet start":
                counts["not_yet_start_projects"] += 1
            elif status == "On going":
                counts["on_going_projects"] += 1
            elif status == "Ahead of schedule":
                counts["ahead_of_schedule_projects"] += 1
                counts["completed_projects"] += 1
            elif status == "On Time":
                counts["on_time_projects"] += 1
                counts["completed_projects"] += 1
            elif status == "Delay":
                counts["delayed_projects"] += 1
                counts["completed_projects"] += 1

        return counts

    def delete_project_row(self, item_ids: str, user_id: str) -> dict[str, Any]:
        status = self.repository.delete_project_row(item_ids, user_id)
        log_daily(f"[{user_id}] Delete | items: {item_ids} | Result: {status}")
        return {"success": status.upper() == "SUCCESS", "result": status}

    def insert_project_row(self, items: list[dict[str, Any]], payload) -> dict[str, Any]:
        success_count = 0
        results_summary = []
        for item in items:
            status = self.repository.insert_project_row(item)
            results_summary.append({"task_no": item.get("task_no"), "status": status})
            user_id = item.get("user_id", "N/A")
            task_no = item.get("task_no", "N/A")
            order_no = item.get("order_no", "N/A")
            log_daily(f"[{user_id}] Insert | Task No: {task_no} | Order No: {order_no} | Result: {status}")
            if status.upper() == "SUCCESS":
                success_count += 1
                
        log_daily(f"[{payload[0].user_id if payload else 'unknown'}] Insert | Successfully inserted {success_count}/{len(payload)} rows.")
        
        return {
            "success": success_count == len(items),
            "message": f"Successfully insert {success_count}/{len(items)} rows.",
            "details": results_summary,
        }

    def bulk_update(self, items: list[dict[str, Any]]) -> dict[str, Any]:
        rows = []
        for item in items:
            rows.append(
                (
                    item.get("main_task"),
                    item.get("sub_task"),
                    item.get("qty"),
                    item.get("assignee"),
                    item.get("process"),
                    item.get("status"),
                    item.get("plan_start"),
                    item.get("plan_end"),
                    item.get("actual_start"),
                    item.get("actual_end"),
                    item.get("actual_cost"),
                    item.get("remark"),
                    item.get("user_id"),
                    item.get("item_id"),
                )
            )
        self.repository.bulk_update_items(rows)
        
        log_daily(f"[{items[0].get("user_id") if items else 'unknown'}] Update | Bulk update completed. Total items updated: {len(items)}.")
        
        return {"success": True, "updated": len(items)}

    def login(self, user_id: str, password: str) -> dict[str, Any]:
        encrypted_password = encrypt_password(password)
        user = self.repository.check_login(user_id, encrypted_password)
        if user is None:
            log_daily(f"[{user_id}] Login | Failed")
            raise ServiceError("Invalid username or password", status_code=401)
        
        log_daily(f"[{user_id}] Login | Successful")
        return {"message": "Login successful", "setUserInfoStatus": 0, "user": user}

    def change_user_password(self, user_id: str, current_password: str, new_password: str) -> dict[str, Any]:
        current_pw = encrypt_password(current_password)
        new_pw = encrypt_password(new_password)
        status, message = self.repository.change_user_password(user_id, current_pw, new_pw)
        if status == 1:
            log_daily(f"[{user_id}] Change Password | Successfully changed password")
            return {"status": status, "message": message}
        
        log_daily(f"[{user_id}] Change Password | Failed to change password: {message}")
        raise ServiceError(message, status_code=400)

    def get_personal_kpi_data(self) -> dict[str, Any]:
        raw_data = self.repository.get_kpi_all_data()
        builder = PersonalKPIBuilder()
        personal_detail, total_summary = builder.build(raw_data)
        personalKpiData = {
            'totalSummary' : total_summary,
            'personalKpiSummary' : personal_detail,
            'personalKpiDetail' : raw_data
        }
        return personalKpiData

    def get_dept_kpi_data(self) -> dict[str, Any]:
            raw_data = self.repository.get_kpi_all_data()
            builder = DeptKPIBuilder()
            projects_detail, summary_project = builder.transform(raw_data)
            deptKpiData = {
                'deptKpiSummary' : summary_project,
                'deptKpiDetail' : projects_detail
            }
            return deptKpiData
    
    def get_dashboard_data(self)-> list[dict[str, Any]]:
        raw_data = self.repository.get_dashboard_summary()
        dashboard = DashboardBuilder()
        return dashboard.create_dashboard_data(raw_data)

    @staticmethod
    def _parse_datetime(value: str | None) -> datetime | None:
        if not value:
            return None
        for fmt in ("%Y-%m-%d", "%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S"):
            try:
                return datetime.strptime(value, fmt)
            except ValueError:
                continue
        return None

    @staticmethod
    def _get_project_status(
        plan_start: datetime | None,
        plan_end: datetime | None,
        actual_start: datetime | None,
        actual_end: datetime | None,
    ) -> str:
        if not plan_start and not plan_end:
            return "No plan"
        if not actual_start and not actual_end:
            return "Not yet start"
        if actual_start and not actual_end:
            return "On going"
        if actual_end:
            if plan_end and actual_end > plan_end:
                return "Delay"
            if plan_end and actual_end < plan_end:
                return "Ahead of schedule"
            return "On Time"
        return "Not yet start"
