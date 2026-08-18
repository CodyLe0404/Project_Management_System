from datetime import datetime
from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field


# SUB TASK
@dataclass
class SubTask:
    name: str
    progress: float = 0
    status: str = "No plan"
    plan_start: Optional[datetime] = None
    plan_end: Optional[datetime] = None
    actual_start: Optional[datetime] = None
    actual_end: Optional[datetime] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "status": self.status,
            "progress": self.progress
        }


# MAIN TASK
@dataclass
class MainTask:
    name: str
    progress: float = 0
    status: str = "No plan"
    plan_start: Optional[datetime] = None
    plan_end: Optional[datetime] = None
    actual_start: Optional[datetime] = None
    actual_end: Optional[datetime] = None
    sub_tasks: List[SubTask] = field(default_factory=list)
    counts: Dict[str, int] = field(default_factory=lambda: {
        "total": 0,
        "onTime": 0,
        "noPlan": 0,
        "delayed": 0,
        "doing": 0,
        "notYetStart": 0
    })

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "progress": self.progress,
            "status": self.status,
            "subTasks": [sub_task.to_dict() for sub_task in self.sub_tasks],
            "counts": self.counts
        }


# PROJECT
@dataclass
class Project:
    name: str
    deadline: Optional[datetime] = None
    progress: float = 0
    status: str = "No plan"
    main_tasks: List[MainTask] = field(default_factory=list)
    tasks: Dict[str, Dict[str, int]] = field(default_factory=lambda: {
        "main": {
            "total": 0,
            "onTime": 0,
            "noPlan": 0,
            "delayed": 0,
            "doing": 0,
            "notYetStart": 0
        },
        "sub": {
            "total": 0,
            "onTime": 0,
            "noPlan": 0,
            "delayed": 0,
            "doing": 0,
            "notYetStart": 0
        }
    })
    dept: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "deadline": (self.deadline.strftime("%Y-%m-%d") if self.deadline else None),
            "progress": self.progress,
            "status": self.status,
            "mainTasks": [main_task.to_dict() for main_task in self.main_tasks],
            "tasks": self.tasks,
            "dept": self.dept
        }  
        
              
@dataclass
class SummaryProject:
    project: int = 0

    main_task: Dict[str, int] = field(default_factory=lambda: {
        "total": 0,
        "onTime": 0,
        "noPlan": 0,
        "delayed": 0,
        "doing": 0,
        "notYetStart": 0
    })

    sub_task: Dict[str, Dict[str, int]] = field(default_factory=lambda: {
        "Design (E)": {
            "total": 0,
            "onTime": 0,
            "noPlan": 0,
            "delayed": 0,
            "doing": 0,
            "notYetStart": 0
        },
        "Design (M)": {
            "total": 0,
            "onTime": 0,
            "noPlan": 0,
            "delayed": 0,
            "doing": 0,
            "notYetStart": 0
        }
    })

    active_user: int = 0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "project": self.project,
            "mainTask": self.main_task,
            "subTask": self.sub_task,
            "activeUser": self.active_user
        }


# PROJECT KPI BUILDER        
class DeptKPIBuilder:
    def __init__(self):
        self.summary_data = SummaryProject()
    
    @staticmethod
    def parse_date(value) -> Optional[datetime]:
        if value is None:
            return None

        if isinstance(value, datetime):
            return value

        value = str(value).strip()
        if not value:
            return None

        formats = [
            "%Y-%m-%d",
            "%Y-%m-%d %H:%M:%S",
            "%Y-%m-%dT%H:%M:%S",
            "%Y-%m-%dT%H:%M:%S.%f"
        ]

        for fmt in formats:
            try:
                return datetime.strptime(value, fmt)
            except ValueError:
                continue

        return None

    # MIN DATE
    @staticmethod
    def min_date(values) -> Optional[datetime]:
        values = [value for value in values if value is not None]
        if not values:
            return None
        return min(values)

    # MAX DATE
    @staticmethod
    def max_date(values) -> Optional[datetime]:
        values = [value for value in values if value is not None]
        if not values:
            return None
        return max(values)

    # STATUS
    @staticmethod
    def get_header_status(
        plan_start: Optional[datetime],
        plan_end: Optional[datetime],
        actual_start: Optional[datetime],
        actual_end: Optional[datetime]
        ) -> str:

        if not plan_start and not plan_end:
            return "No plan"

        if not actual_start and not actual_end:
            return "Not yet start"

        if actual_start and not actual_end:
            return "Doing"

        if actual_end:
            if plan_end and actual_end > plan_end:
                return "Delay"
            if plan_end and actual_end < plan_end:
                return "On Time"
            return "On Time"

        return "Not yet start"

    # PROGRESS
    @staticmethod
    def calculate_average_progress(items) -> float:
        if not items:
            return 0
        total = 0
        for item in items:
            try:
                progress = float(item.progress)
            except (TypeError, ValueError):
                progress = 0
            total += progress
        return round(total / len(items), 2)

    def calculate_task_counts(self, items) -> Dict[str, int]:
        counts = {
            "total": len(items),
            "onTime": 0,
            "noPlan": 0,
            "delayed": 0,
            "doing": 0,
            "notYetStart": 0
        }

        for item in items:
            status = item.status
            if status == "On Time" or status == "Ahead of schedule":
                counts["onTime"] += 1
            elif status == "No plan":
                counts["noPlan"] += 1
            elif status == "Delay":
                counts["delayed"] += 1
            elif status == "Doing":
                counts["doing"] += 1
            elif status == "Not yet start":
                counts["notYetStart"] += 1

        return counts

    def build_sub_task(self, row: Dict[str, Any]) -> SubTask:
        progress = row.get("progress", 0)
        try:
            progress = float(progress)
        except (TypeError, ValueError):
            progress = 0

        return SubTask(
            name=row.get("sub_task", ""),
            progress=progress,
            status=row.get("status", "No plan"),
            plan_start=self.parse_date(row.get("plan_start")),
            plan_end=self.parse_date(row.get("plan_end")),
            actual_start=self.parse_date(row.get("actual_start")),
            actual_end=self.parse_date(row.get("actual_end"))
        )

    def build_main_task(self, main_task_name: str, rows: List[Dict[str, Any]]) -> MainTask:
        sub_tasks = [self.build_sub_task(row) for row in rows]
        plan_start = self.min_date([task.plan_start for task in sub_tasks])
        plan_end = self.max_date([task.plan_end for task in sub_tasks])
        actual_start = self.min_date([task.actual_start for task in sub_tasks])
        actual_end = self.max_date([task.actual_end for task in sub_tasks])
        status = self.get_header_status(plan_start, plan_end, actual_start,actual_end)
        progress = self.calculate_average_progress(sub_tasks)
        counts = self.calculate_task_counts(sub_tasks)

        return MainTask(
            name=main_task_name,
            progress=progress,
            status=status,
            plan_start=plan_start,
            plan_end=plan_end,
            actual_start=actual_start,
            actual_end=actual_end,
            sub_tasks=sub_tasks,
            counts=counts
        )

    # BUILD PROJECT
    def build_project(self, rows: List[Dict[str, Any]]) -> Project:

        if not rows:
            raise ValueError("Project data cannot be empty.")

        project_name = rows[0].get("project_name", "")
        dept = rows[0].get("department")
        
        # Group rows by Main Task
        grouped_main_tasks = {}

        for row in rows:
            main_task_name = row.get("main_task", "")
            if main_task_name not in grouped_main_tasks:
                grouped_main_tasks[main_task_name] = []
            grouped_main_tasks[main_task_name].append(row)

        # Build Main Tasks
        main_tasks = []
        for (main_task_name, main_task_rows) in grouped_main_tasks.items():
            main_task = self.build_main_task(main_task_name, main_task_rows)
            main_tasks.append(main_task)

        plan_start = self.min_date([task.plan_start for task in main_tasks])
        plan_end = self.max_date([task.plan_end for task in main_tasks])
        actual_start = self.min_date([task.actual_start for task in main_tasks])
        actual_end = self.max_date([task.actual_end for task in main_tasks])
        progress = self.calculate_average_progress(main_tasks)
        status = "Doing" if progress < 100 and progress > 0 else self.get_header_status(plan_start, plan_end, actual_start, actual_end)
        main_task_counts = self.calculate_task_counts(main_tasks)
        
        all_sub_tasks = []
        for main_task in main_tasks:
            all_sub_tasks.extend(main_task.sub_tasks)

        sub_task_counts = self.calculate_task_counts(all_sub_tasks)
        tasks = {"main": main_task_counts, "sub": sub_task_counts}

        return Project(
            name=project_name,
            deadline=plan_end,
            progress=progress,
            status=status,
            main_tasks=main_tasks,
            tasks=tasks,
            dept=dept
        )

    def transform(self, rows: List[Dict[str, Any]]):
        if not rows:
            return [], SummaryProject().to_dict()

        # BUILD SUMMARY PROJECT
        summary_project = self.build_summary(rows)

        # GROUP BY PROJECT
        grouped_projects = {}
        for row in rows:
            project_id = row.get("project_id")
            if project_id not in grouped_projects:
                grouped_projects[project_id] = []
            grouped_projects[project_id].append(row)

        # BUILD PROJECTS
        projects_detail = []
        for project_rows in grouped_projects.values():
            project = self.build_project(project_rows)
            projects_detail.append(project.to_dict())

        return projects_detail, summary_project.to_dict()
        
    def build_summary(self, rows: List[Dict[str, Any]]) -> SummaryProject:
        if not rows:
            return SummaryProject()

        # 1. GROUP BY PROJECT
        grouped_projects = {}
        for row in rows:
            project_id = row.get("project_id")
            if project_id not in grouped_projects:
                grouped_projects[project_id] = []
            grouped_projects[project_id].append(row)

        # 2. PROJECT COUNT
        project_count = len(grouped_projects)

        # 3. BUILD MAIN TASK
        all_main_tasks = []
        for project_rows in grouped_projects.values():
            grouped_main_tasks = {}
            for row in project_rows:
                main_task_name = row.get("main_task", "")
                if main_task_name not in grouped_main_tasks:
                    grouped_main_tasks[main_task_name] = []
                grouped_main_tasks[main_task_name].append(row)

            # Build MainTask
            for (main_task_name, main_task_rows) in grouped_main_tasks.items():
                main_task = self.build_main_task(main_task_name, main_task_rows)
                all_main_tasks.append(main_task)

        # 4. MAIN TASK SUMMARY
        main_task_counts = self.calculate_task_counts(all_main_tasks)

        # 5. SUB TASK SUMMARY
        sub_task_summary = {
            "Design (E)": {
                "total": 0,
                "onTime": 0,
                "noPlan": 0,
                "delayed": 0,
                "doing": 0,
                "notYetStart": 0
            },
            "Design (M)": {
                "total": 0,
                "onTime": 0,
                "noPlan": 0,
                "delayed": 0,
                "doing": 0,
                "notYetStart": 0
            }
        }

        # Group SubTask theo department
        sub_tasks_by_department = {}
        for row in rows:
            department = row.get("department")
            if not department:
                continue
            if department not in sub_tasks_by_department:
                sub_tasks_by_department[department] = []
            sub_task = self.build_sub_task(row)
            sub_tasks_by_department[department].append(sub_task)

        # Calculate KPI từng department
        for department, sub_tasks in (sub_tasks_by_department.items()):
            counts = self.calculate_task_counts(sub_tasks)
            sub_task_summary[department] = counts

        # 6. ACTIVE USER
        active_users = set()
        for row in rows:
            user = row.get("assignee")
            if user:
                active_users.add(user.upper())
        active_user_count = len(active_users)

        # 7. CREATE SUMMARY PROJECT
        summary = SummaryProject(
            project=project_count,
            main_task=main_task_counts,
            sub_task=sub_task_summary,
            active_user=active_user_count
        )

        return summary
    