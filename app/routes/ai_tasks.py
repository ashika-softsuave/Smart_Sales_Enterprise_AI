from fastapi import APIRouter,Depends
from app.services.task_allocator import allocate_task
from app.schemas.daily_task_schema import DailyTaskResponse

router=APIRouter()

@router.post("get-daily-task", response_model=DailyTaskResponse)
def get_daily_task(salesman_id:int):
    return allocate_task(salesman_id)