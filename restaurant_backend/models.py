from sqlalchemy import Column, Integer, String, Boolean
from restaurant_backend.database import Base


class DiningTable(Base):
    __tablename__ = "tables"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    capacity = Column(Integer)
    section = Column(String)  # AC / Non-AC


class Reservation(Base):
    __tablename__ = "reservations"

    id = Column(Integer, primary_key=True, index=True)

    customer_name = Column(String)
    email = Column(String)

    date = Column(String)
    time = Column(String)

    people = Column(Integer)

    table_id = Column(Integer)

    section = Column(String)

    duration = Column(String)  # breakfast / lunch / dinner
