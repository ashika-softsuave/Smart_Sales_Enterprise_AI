from sqlalchemy import Column,Integer,String,Float,ForeignKey
from app.core.database import Base
class Salesman(Base):
    __tablename__="Salesman"

    id=Column(Integer,primary_key=True)
    name=Column(String)
    email=Column(unique=True)
    role=Column(String)
    team_id=Column(Integer,ForeignKey="team.id")
    daily_travel=Column(Float,default=0.0)