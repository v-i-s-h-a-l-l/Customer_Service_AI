from sqlalchemy.orm import Session
from restaurant_backend.models import DiningTable, Reservation


def find_available_table(db: Session, people: int, section: str):
    tables = (
        db.query(DiningTable)
        .filter(DiningTable.capacity >= people, DiningTable.section == section)
        .all()
    )

    if not tables:
        return None

    return tables[0]


def create_reservation(db: Session, req):
    table = find_available_table(db, req.people, req.section)

    if not table:
        return {"status": "no_table"}

    reservation = Reservation(
        customer_name=req.name,
        email=req.email,
        date=req.date,
        time=req.time,
        people=req.people,
        table_id=table.id,
        section=req.section,
        duration=req.duration,
    )

    db.add(reservation)
    db.commit()

    return {"status": "confirmed", "table_id": table.id}
