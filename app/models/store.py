from sqlalchemy import Column, Integer, Float, String, Boolean, ForeignKey
from app.core.database import Base

class Store(Base):
    __tablename__ = "stores"

    id = Column(Integer, primary_key=True, index=True)
    store_name = Column(String, nullable=False)
    latitude = Column(Float)
    longitude = Column(Float)

    product_id = Column(Integer, ForeignKey("products.id"))
    is_assigned = Column(Boolean, default=False)
