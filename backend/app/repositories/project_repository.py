from __future__ import annotations

from typing import Any
import pyodbc


class ProjectRepository:
    def __init__(self, conn: pyodbc.Connection) -> None:
        self.conn = conn

    def check_duplicate_task(self, project_id: str, items: list[dict[str, Any]]) -> list[str]:
        duplicates: list[str] = []
        cursor = self.conn.cursor()
        try:
            for item in items:
                main_task = item["main_task"]
                cursor.execute("EXEC USP_DS_Check_Duplicate_Task ?, ?", project_id, main_task)
                result = cursor.fetchone()
                if result and result[0] != "Not existed":
                    duplicates.append(main_task)
            return duplicates
        finally:
            self.conn.commit()
            cursor.close()

    def create_project(self, project_id: str, project_number: str, project_name: str, user_id: str) -> str:
        cursor = self.conn.cursor()
        try:
            cursor.execute(
                "EXEC [Design_System].[dbo].[USP_PM_Create_Project] ?, ?, ?, ?",
                project_id,
                project_number,
                project_name,
                user_id,
            )
            result = cursor.fetchone()
            return result[0] if result else "Project created fail"
        finally:
            self.conn.commit()
            cursor.close()

    def insert_project_items(self, project_id: str, rows: list[tuple[Any, ...]], user_id: str) -> None:
        cursor = self.conn.cursor()
        try:
            if rows:
                cursor.executemany(
                    """
                    INSERT INTO [Design_System].[dbo].[DS_PM_Item]
                    (project_id, task_no, main_task, sub_task, qty, ord_no, budget, active_flag, created_at, updated_at, update_by)
                    VALUES (?, ?, ?, ?, ?, ?, ?, 1, getdate(), getdate(), ?)
                    """,
                    rows,
                )
        finally:
            self.conn.commit()
            cursor.close()

    def get_project_details(self) -> list[dict[str, Any]]:
        cursor = self.conn.cursor()
        try:
            cursor.execute("EXEC [Design_System].[dbo].[USP_PM_Get_Project_Detail]")
            columns = [col[0] for col in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]
        finally:
            cursor.close()

    def get_project_summary(self) -> list[tuple[Any, ...]]:
        cursor = self.conn.cursor()
        try:
            cursor.execute("EXEC [Design_System].[dbo].[USP_PM_Get_Project_Summary]")
            return cursor.fetchall()
        finally:
            cursor.close()

    def delete_project_row(self, item_ids: str, user_id: str) -> str:
        cursor = self.conn.cursor()
        try:
            result = cursor.execute("EXEC USP_DS_PM_Delete_Item_Data ?, ?", item_ids, user_id).fetchone()
            return str(result[0]) if result else ""
        finally:
            self.conn.commit()
            cursor.close()

    def insert_project_row(self, item: dict[str, Any]) -> str:
        cursor = self.conn.cursor()
        try:
            cursor.execute(                 
                "EXEC USP_PM_Insert_Row_Data ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?",
                item.get("project_id"),
                item.get("task_no"),
                item.get("main_task"),
                item.get("sub_task"),
                item.get("qty"),
                item.get("budget"),
                item.get("actual_cost") or 0,
                item.get("assignee") or "",
                item.get("user_id"),
                item.get("plan_start"),
                item.get("plan_end"),
                item.get("actual_start"),
                item.get("actual_end"),
                item.get("order_no"),
            )
            row_result = cursor.fetchone()
            self.conn.commit()
            return str(row_result[0]) if row_result else "UNKNOWN"
        finally:
            cursor.close()

    def bulk_update_items(self, rows: list[tuple[Any, ...]]) -> None:
        cursor = self.conn.cursor()
        try:
            if rows:
                cursor.executemany(
                    """
                    UPDATE [Design_System].[dbo].[DS_PM_Item]
                    SET main_task=?, sub_task=?, qty=?, assignee=?, [percent]=?, status=?, plan_start=?, plan_end=?,
                        actual_start=?, actual_end=?, actual_cost=?, remark=?, updated_at=getdate(), update_by=?
                    WHERE id_item=?
                    """,
                    rows,
                )
            self.conn.commit()
        finally:
            cursor.close()

    def check_login(self, user_id: str, password: str) -> dict[str, Any] | None:
        cursor = self.conn.cursor()
        try:
            cursor.execute("EXEC DS_PM_Check_User_Login ?, ?", user_id, password)
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
                "userConfig": get_per.permission_codes.split(";") if get_per.permission_codes else [],
            }
        finally:
            cursor.close()

    def change_user_password(self, user_id: str, current_pw: str, new_pw: str) -> tuple[int, str]:
        cursor = self.conn.cursor()
        try:
            result = cursor.execute("EXEC USP_DS_PM_ChangeUserPassword ?, ?, ?", user_id, current_pw, new_pw)
            row = result.fetchone()
            if row is None or len(row) < 2:
                raise ValueError("Stored procedure did not return expected response.")
            return int(row[0]), str(row[1])
        finally:
            self.conn.commit()
            cursor.close()

    def get_kpi_summary(self) -> list[dict[str, Any]]:
        cursor = self.conn.cursor()
        try:
            cursor.execute("EXEC [Design_System].[dbo].[USP_PM_Get_KPI_Summary] 'Get_all'")
            columns = [col[0] for col in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]
        finally:
            cursor.close()

    def get_dashboard_summary(self) -> list[dict[str, Any]]:
        cursor = self.conn.cursor()
        try:
            cursor.execute("EXEC [Design_System].[dbo].[USP_PM_Dashboard_Summary]")
            columns = [col[0] for col in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]
        finally:
            cursor.close()
    
        