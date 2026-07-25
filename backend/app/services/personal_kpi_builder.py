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
            "subTask": [],
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
            
            employee["subTask"].append({
                "itemName": row.get("sub_task") or "",
                "projectStatus": row.get("status") or ""
            })
            
        result = []
        for employee in self.employees.values():
            result.append({
                "id": employee["id"],
                "userId": employee["userId"],
                "name": employee["name"],
                "title": employee["title"],
                "part": employee["part"],
                "projectCount": len(employee["projects"]),
                "mainTasksCount": len(employee["mainTasks"]),
                "subTasksCount": employee["subTasksCount"],
                "onTime": employee["statusCounter"]["On Time"],
                "Doing": employee["statusCounter"]["Doing"],
                "delayed": employee["statusCounter"]["Delay"] + employee["statusCounter"]["Delayed"],
                "ahead":employee["statusCounter"]["Ahead of schedule"],
                "noPlan":employee["statusCounter"]["No plan"],
                "notYetStart":employee["statusCounter"]["Not yet start"],
                "subTask": employee["subTask"]
            })
        return result
        
        