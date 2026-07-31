from collections import defaultdict
from typing import Any

class PersonalKPIBuilder:

    def __init__(self) -> None:
        # Dictionary lớn nhất
        # Key = assignee
        self.employees: dict[str, dict[str, Any]] = {}

        # Auto increase id
        self.current_id = 1
    
    def create_employee(self, row: dict[str, Any], original_assignee: str) -> dict[str, Any]:
        return {
            "id": self.current_id,
            # Lưu giá trị assignee gốc (ví dụ: "HungCC") ở lần đầu xuất hiện
            "userId": original_assignee,
            "name": row.get("fullname") or "",
            "title": row.get("title") or "",
            "part": row.get("department") or "",
            "projects": set(),  # Temporary Data
            "mainTasks": set(),  # Temporary Data
            "subTasksCount": 0,
            "statusCounter": defaultdict(int),
            
        }
        
    def update_project(self, employee: dict[str, Any], row: dict[str, Any]) -> None:
        project_id = row.get("project_id")
        if project_id:
            employee["projects"].add(project_id)

    def update_subtask(self, employee: dict[str, Any], row: dict[str, Any]) -> None:
        employee["subTasksCount"] += 1

    def update_status(self, employee: dict[str, Any], row: dict[str, Any]) -> None:
        status = row.get("status")
        if status:
            employee["statusCounter"][status] += 1

    def build(self, raw_data: list[dict[str, Any]]) -> list[dict[str, Any]]:
        for row in raw_data:
            assignee = row.get("assignee")
            if not assignee:
                continue
            
            assignee_key = assignee.lower()
            if assignee_key not in self.employees:
                self.employees[assignee_key] = self.create_employee(
                    row, assignee
                )
                self.current_id += 1
            
            employee = self.employees[assignee_key]
            self.update_project(employee, row)
            
            main_task = row.get("main_task")
            if main_task:
                employee["mainTasks"].add(main_task)
                
            self.update_subtask(employee, row)
            self.update_status(employee, row)
            
            
        result = []
        total_summary = {}
        
        no_plan = 0
        not_started = 0
        doing = 0
        onTime = 0
        delay = 0
        ahead = 0
        total_task = 0

        for employee in self.employees.values():
            # Lấy statusCounter của từng nhân viên để code gọn và an toàn hơn
            status = employee.get("statusCounter", {})

            # Lấy giá trị của từng trạng thái (dùng .get() để tránh KeyError nếu thiếu key)
            emp_on_time = status.get("On Time", 0)
            emp_doing = status.get("Doing", 0)
            emp_delay = status.get("Delay", 0) + status.get("Delayed", 0)
            emp_ahead = status.get("Ahead of schedule", 0)
            emp_no_plan = status.get("No plan", 0)
            emp_not_started = status.get("Not yet start", 0)

            # Tính tổng số task của nhân viên này
            emp_total_task = (
                emp_on_time
                + emp_doing
                + emp_delay
                + emp_ahead
                + emp_no_plan
                + emp_not_started
            )

            # Append vào danh sách kết quả từng nhân viên
            result.append(
                {
                    "id": employee["id"],
                    "userId": employee["userId"],
                    "name": employee["name"],
                    "title": employee["title"],
                    "part": employee["part"],
                    "projectCount": len(employee["projects"]),
                    "mainTasksCount": len(employee["mainTasks"]),
                    "subTasksCount": employee["subTasksCount"],
                    "onTime": emp_on_time,
                    "Doing": emp_doing,
                    "delayed": emp_delay,
                    "ahead": emp_ahead,
                    "noPlan": emp_no_plan,
                    "notYetStart": emp_not_started,
                }
            )

            # 2. Cộng dồn vào các biến tổng tổng quát (total)
            onTime += emp_on_time
            doing += emp_doing
            delay += emp_delay
            ahead += emp_ahead
            no_plan += emp_no_plan
            not_started += emp_not_started
            total_task += emp_total_task

        # 3. Tạo dict total_summary chứa kết quả tổng sau khi lặp xong
        total_summary = {
            "no_plan": no_plan,
            "not_started": not_started,
            "doing": doing,
            "onTime": onTime,
            "delay": delay,
            "ahead": ahead,
            "total_task": total_task,
        }
            
            
            
        return result, total_summary
        
        