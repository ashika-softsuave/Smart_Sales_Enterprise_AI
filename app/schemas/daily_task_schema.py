from pydantic import BaseModel
from typing import List


class RouteStep(BaseModel):
    location: str
    latitude: float | None = None
    longitude: float | None = None


class DailyTaskResponse(BaseModel):
    assigned_target: int
    tasks_reached: int
    tasks_pending: int
    route_assigned: List[RouteStep]

    class Config:
        from_attributes = True
