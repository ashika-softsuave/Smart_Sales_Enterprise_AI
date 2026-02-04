from sqlalchemy import Column, Integer, ForeignKey, DateTime, Date, Float
from sqlalchemy.orm import relationship
from app.core.database import Base
from datetime import datetime, date


class DailySalesLog(Base):
    __tablename__ = "daily_sales_logs"

    id = Column(Integer, primary_key=True, index=True)

    salesman_id = Column(
        Integer,
        ForeignKey("salesman.id"),
        nullable=False
    )

    work_date = Column(Date, default=date.today)
    start_time = Column(DateTime, default=datetime.utcnow)
    end_time = Column(DateTime, nullable=True)

    items_sold = Column(Integer, default=0)
    items_pending = Column(Integer, default=0)

    # ✅ THIS COLUMN MUST EXIST IN MODEL
    travel_km = Column(Float, default=0.0)

    salesman = relationship("Salesman", backref="daily_logs")
