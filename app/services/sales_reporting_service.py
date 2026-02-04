from datetime import datetime, date
from sqlalchemy.orm import Session
from app.models.daily_sales_log import DailySalesLog


def record_sales_summary(
    db: Session,
    salesman_id: int,
    sold_items: int,
    pending_items: int,
    start_time: datetime,
    end_time: datetime
):
    # One log per salesman per day
    log = (
        db.query(DailySalesLog)
        .filter(
            DailySalesLog.salesman_id == salesman_id,
            DailySalesLog.work_date == date.today()
        )
        .first()
    )

    if not log:
        log = DailySalesLog(
            salesman_id=salesman_id,
            start_time=start_time
        )
        db.add(log)

    log.items_sold = sold_items
    log.items_pending = pending_items
    log.end_time = end_time

    db.commit()
    db.refresh(log)

    return log
