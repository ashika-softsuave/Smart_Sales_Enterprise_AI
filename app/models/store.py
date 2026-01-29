from sqlalchemy import Column,Integer,Float,String
from app.core.database import Base

class Store(Base):
    __table_name__="stores"

    id=Column(Integer,primary_key=True)
    store_name=Column(String)
    latitude=Column(Float)
    longitude=Column(Float)
    product_id=Column(Integer)