from sqlalchemy.orm import Session
from datetime import date

from app.models.sales_report import SalesReport
from app.models.daily_task import DailyTask
from app.models.salesman import Salesman
from app.models.team import Team

def analyze_sales_performance(
    db:Session,
    salesman_id:int,
    today:date
):
    """
    Core Performance analyzer for a salesman

    """
     daily_task=db.query(DailyTask).filter(
         DailyTask.salesman_id==salesman_id,
         DailyTask.date==today
     ).first()

    if not daily_task:
        raise Exception("Daily task not found")

    #Fetch today's Sales
    sales=db.query(SalesReport).filter(
        SalesReport.salesman_id==salesman_id,
        SalesReport.date==today
    ).all()

    total_sales=sum(s.quantity_sold for s in sales)

    #Update daily task progress
    daily_task.tasks_reached=total_sales
    daily_task.tasks_pending=max(
        daily_task.assigned_target-total_sales,0
    )

    #Determine performance status
    if total_sales>daily_task.assigned_target:
        performnace_status="EXCEEDED"
    elif total_sales==daily_task.assigned_target:
        performance_status="MET"
    else:
        performance_status="NOT_MET"

    #Fetch Salesman
    salesman=db.query(Salesman).filter(Salesman.id==salesman_id
    ).first()

    #Calculate efficiency
    efficiency=0
    if salesman.daily_travel_km>0:
        efficiency=round(
            total_sales/salesman.daily_travel_km,2
        )

    #Update team states
    team=db.query(Team).filter(Team.id==Salesman.team_id).first()

    if team:
        team.tasks_reached+=total_sales
        teams.total_tasks+=daily_task.assigned_target

    db.commit()

    return{
        "salesman_id":salesman_id,
        "date":str(today)
        "target":daily_task.assigned_target,
        "achieved":total_sales,
        "pending":daily_task.tasks_pending,
        "status":performance_status,
        "distance_travelled_km":salesman.daily_travel_km,
        "efficiency":efficiency
    }