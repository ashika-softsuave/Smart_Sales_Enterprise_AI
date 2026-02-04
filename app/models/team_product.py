from sqlalchemy import Column, Integer, ForeignKey
from app.core.database import Base

class TeamProduct(Base):
    __tablename__ = "team_products"

    id = Column(Integer, primary_key=True)
    team_id = Column(Integer, ForeignKey("teams.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    daily_target = Column(Integer)
