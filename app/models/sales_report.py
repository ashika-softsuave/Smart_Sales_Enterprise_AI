from sqlalchemy import Column, Integer, String, Date
from app.core.database import Base


class SalesReport(Base):
    __tablename__ = "sales_reports"

    id = Column(Integer, primary_key=True)
    salesman_id = Column(Integer)
    store_id = Column(Integer)
    product_id = Column(Integer)
    product_name = Column(String)
    quantity_sold = Column(Integer)
    date = Column(Date)