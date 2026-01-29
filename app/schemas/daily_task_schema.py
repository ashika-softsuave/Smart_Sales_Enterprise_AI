from pydantic import BaseModel
from typing import List

class DailyTaskResponse(BaseModel):
    assigned_target: int
    tasks_reached:int
    tasks_pending:int
    route_assigned:List[int]

class DailyTaskResponse(BaseModel):
    assigned_target:int
    tasks_reached:int
    tasks_pending:int
    route_assigned:RouteSchema