from sqlalchemy import Column, Integer, String, DateTime, ForeignKey,JSON
from app.core.database import Base

class DailyTask(Base):
    __tablename__ = 'daily_tasks'

    id = Column(Integer, primary_key=True)
    salesman_id = Column(Integer, ForeignKey("salesman.id"))
    date = Column(DateTime)
    assigned_target=Column(Integer)
    tasks_reached=Column(Integer,default=0)
    tasks_pending=Column(Integer)
    route_assigned=Column(JSON)