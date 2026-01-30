from sqlalchemy.orm import Session
from app.models.team import Team
from app.models.salesman import Salesman
from app.utils.exporter import export_to_csv

def get_ceo_dashboard(db: Session):
    teams = db.query(Team).all()

    leaderboard = []

    for team in teams:
        performance = 0
        if team.total_tasks > 0:
            performance = (team.tasks_reached / team.total_tasks) * 100

        leaderboard.append({
            "team_id": team.id,
            "team_name": team.team_name,
            "manager_id": team.manager_id,
            "tasks_reached": team.tasks_reached,
            "total_tasks": team.total_tasks,
            "performance_percent": round(performance, 2)
        })

    leaderboard.sort(key=lambda x: x["performance_percent"], reverse=True)

    return {
        "status": "success",
        "leaderboard": leaderboard
    }

def get_all_salesmen(db: Session):
    salesmen = db.query(Salesman).all()

    return {
        "salesmen": [
            {
                "salesman_id": s.id,
                "name": s.name,
                "email": s.email,
                "team_id": s.team_id,
                "daily_travel_km": s.daily_travel
            }
            for s in salesmen
        ]
    }

def get_company_summary(db: Session):
    total_teams = db.query(Team).count()
    total_salesmen = db.query(Salesman).count()

    teams = db.query(Team).all()

    total_tasks = sum(t.total_tasks for t in teams)
    tasks_reached = sum(t.tasks_reached for t in teams)

    return {
        "total_teams": total_teams,
        "total_salesmen": total_salesmen,
        "tasks_reached": tasks_reached,
        "total_tasks": total_tasks
    }

def export_company_data(db: Session):
    teams = db.query(Team).all()
    salesmen = db.query(Salesman).all()

    data = {
        "teams": [
            {
                "team_id": t.id,
                "team_name": t.team_name,
                "manager_id": t.manager_id,
                "tasks_reached": t.tasks_reached,
                "total_tasks": t.total_tasks
            } for t in teams
        ],
        "salesmen": [
            {
                "salesman_id": s.id,
                "name": s.name,
                "email": s.email,
                "team_id": s.team_id,
                "daily_travel_km": s.daily_travel
            } for s in salesmen
        ]
    }

    file_path = export_to_csv(data, filename="company_report.csv")

    return {
        "status": "success",
        "file": file_path
    }
