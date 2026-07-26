from typing import Any

class DashboardBuilder:
    def __init__(self):
        self.dashboard_data: dict[str, Any] = {}
        
    def create_dashboard_data(self, raw_data: list[dict[str, Any]]):
        project = []
        not_started = 0
        inprogress = 0
        completed = 0
        per_1_25 = 0
        per_26_50 = 0
        per_51_75 = 0
        per_76_99 = 0
        
        for item in raw_data:
              
            if item['project_id'] not in project:
                project.append(item['project_id'])
            
            if item['progress'] == 0:
                not_started += 1
            elif item['progress'] > 0 and item['progress'] <= 25:
                per_1_25 += 1
            elif item['progress'] > 25 and item['progress'] <= 50:
                per_26_50 += 1
            elif item['progress'] > 50 and item['progress'] <= 75:
                per_51_75 += 1
            elif item['progress'] > 75 and item['progress'] <= 99:
                per_76_99 += 1
            elif item['progress'] == 100:
                completed += 1
        
        inprogress = per_1_25 + per_26_50 + per_51_75 + per_76_99
        total_task = len(raw_data)
        
        self.dashboard_data = {
            'total_project' : len(project),
            'total_task' : total_task,
            'not_started' : not_started,
            'inprogress' : inprogress,
            'completed' : completed,
            'per_1_25' : per_1_25,
            'per_26_50' : per_26_50,
            'per_51_75' : per_51_75,
            'per_76_99' : per_76_99
        }
        
        return self.dashboard_data
    
    
    