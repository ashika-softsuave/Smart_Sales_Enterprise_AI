from sqlalchemy import Column, Integer, String, Float, ForeignKey
from app.core.database import Base

class Salesman(Base):
    __tablename__ = "salesman"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    role = Column(String, default="salesman")

    team_id = Column(Integer, ForeignKey("teams.id"), nullable=True)

    daily_travel = Column(Float, default=0.0)
