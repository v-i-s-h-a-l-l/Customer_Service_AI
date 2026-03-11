import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))


from restaurant_backend.database import engine, SessionLocal
from restaurant_backend.models import Base, DiningTable

Base.metadata.create_all(bind=engine)

db = SessionLocal()

tables = [
    {"name": "T1", "capacity": 2, "section": "AC"},
    {"name": "T2", "capacity": 2, "section": "Non-AC"},
    {"name": "T3", "capacity": 4, "section": "AC"},
    {"name": "T4", "capacity": 4, "section": "Non-AC"},
    {"name": "T5", "capacity": 6, "section": "AC"},
    {"name": "T6", "capacity": 6, "section": "Non-AC"},
    {"name": "T7", "capacity": 8, "section": "AC"},
    {"name": "T8", "capacity": 8, "section": "Non-AC"},
    {"name": "T9", "capacity": 10, "section": "AC"},
    {"name": "T10", "capacity": 10, "section": "Non-AC"},
]

for t in tables:
    db.add(DiningTable(**t))

db.commit()

print("✅ 10 restaurant tables created")
