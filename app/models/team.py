from sqlalchemy import Column,Integer,String,JSON
from app.core.database import Base

class Team(Base):
    __tablename__="teams"

    id=Column(Integer,primary_key=True)
    name = Column(String, nullable=False)
    team_name=Column(String)
    manager_id=Column(Integer)
    teammates_names=Column(JSON)
    tasks_reached=Column(Integer,default=0)
    total_tasks=Column(Integer,default=0)