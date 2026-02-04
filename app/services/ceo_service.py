from app.utils.exporter import export_to_csv
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.team import Team
from app.models.salesman import Salesman
from app.models.daily_sales_log import DailySalesLog


# =========================
# CEO DASHBOARD (UNCHANGED – ALREADY CORRECT)
# =========================
def get_ceo_dashboard(db: Session):
    teams = db.query(Team).all()
    leaderboard = []

    for team in teams:
        logs = (
            db.query(
                func.coalesce(func.sum(DailySalesLog.items_sold), 0).label("sold"),
                func.coalesce(func.sum(DailySalesLog.items_pending), 0).label("pending")
            )
            .join(Salesman, Salesman.id == DailySalesLog.salesman_id)
            .filter(Salesman.team_id == team.id)
            .one()
        )

        sold = logs.sold
        pending = logs.pending
        total = sold + pending

        performance = round((sold / total) * 100, 2) if total > 0 else 0

        leaderboard.append({
            "team_id": team.id,
            "team_name": team.team_name,
            "manager_id": team.manager_id,
            "tasks_reached": sold,
            "total_tasks": total,
            "performance_percent": performance
        })

    leaderboard.sort(
        key=lambda x: x["performance_percent"],
        reverse=True
    )

    return {
        "status": "success",
        "leaderboard": leaderboard
    }


# =========================
# GET ALL SALESMEN (UNCHANGED)
# =========================
def get_all_salesmen(db: Session):
    salesmen = (
        db.query(Salesman)
        .filter(Salesman.role == "salesman")
        .all()
    )

    return {
        "salesman": [
            {
                "salesman_id": s.id,
                "name": s.name,
                "email": s.email,
                "team_id": s.team_id,
                "daily_travel_km": s.daily_travel_km
            }
            for s in salesman
        ]
    }


# =========================
# COMPANY SUMMARY (UNCHANGED – ALREADY CORRECT)
# =========================
def get_company_summary(db: Session):
    total_teams = db.query(Team).count()
    total_salesmen = (
        db.query(Salesman)
        .filter(Salesman.role == "salesman")
        .count()
    )

    totals = (
        db.query(
            func.coalesce(func.sum(DailySalesLog.items_sold), 0),
            func.coalesce(func.sum(DailySalesLog.items_pending), 0)
        )
        .one()
    )

    sold, pending = totals
    total_tasks = sold + pending

    return {
        "total_teams": total_teams,
        "total_salesmen": total_salesmen,
        "tasks_reached": sold,
        "total_tasks": total_tasks
    }


# =========================
# EXPORT COMPANY DATA (FIXED)
# =========================
def export_company_data(db: Session):
    teams = db.query(Team).all()

    # ✅ FIX 1: Aggregate team performance from DailySalesLog
    team_data = []

    for t in teams:
        stats = (
            db.query(
                func.coalesce(func.sum(DailySalesLog.items_sold), 0).label("sold"),
                func.coalesce(func.sum(DailySalesLog.items_pending), 0).label("pending")
            )
            .join(Salesman, Salesman.id == DailySalesLog.salesman_id)
            .filter(Salesman.team_id == t.id)
            .one()
        )

        sold = stats.sold
        pending = stats.pending
        total = sold + pending

        team_data.append({
            "team_id": t.id,
            "team_name": t.team_name,
            "manager_id": t.manager_id,
            "tasks_reached": sold,
            "total_tasks": total
        })

    # ✅ FIX 2: Export ONLY real salesmen (exclude CEO / Manager)
    salesmen = (
        db.query(Salesman)
        .filter(Salesman.role == "salesman")
        .all()
    )

    salesman_data = [
        {
            "salesman_id": s.id,
            "name": s.name,
            "email": s.email,
            "team_id": s.team_id,
            "daily_travel_km": round(
            sum(log.travel_km for log in s.daily_logs), 2
        )
        }
        for s in salesmen
    ]

    team_file = export_to_csv(team_data, "teams_report")
    salesman_file = export_to_csv(salesman_data, "salesmen_report")

    return {
        "status": "success",
        "files": {
            "teams": team_file,
            "salesmen": salesman_file
        }
    }
