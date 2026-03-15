from sqlalchemy.orm import Session
from restaurant_backend.models import DiningTable, Reservation


def find_available_table(db: Session, people: int, section: str):
    """
    Find an available table.
    Normalizes section input so 'ac'/'non_ac' from voice agent
    matches 'AC'/'Non-AC' stored in the database.
    """
    # Normalize section from voice agent format → DB format
    section_map = {
        "ac": "AC",
        "non_ac": "Non-AC",
        "non-ac": "Non-AC",
        # passthrough if already correct
        "AC": "AC",
        "Non-AC": "Non-AC",
    }
    normalized_section = section_map.get(section, section)

    tables = (
        db.query(DiningTable)
        .filter(
            DiningTable.capacity >= people,
            DiningTable.section == normalized_section,
        )
        .all()
    )

    if not tables:
        return None

    return tables[0]


def create_reservation(db: Session, req):
    table = find_available_table(db, req.people, req.section)

    if not table:
        return {
            "status": "no_table",
            "message": f"No available {req.section} table for {req.people} guests.",
        }

    reservation = Reservation(
        customer_name=req.name,
        email=req.email,
        date=req.date,
        time=req.time or req.meal_slot,  # use meal_slot as time fallback
        people=req.people,
        table_id=table.id,
        section=table.section,
        duration=req.meal_slot,  # store meal_slot in duration column
    )

    db.add(reservation)
    db.commit()

    return {
        "status": "confirmed",
        "table_id": table.id,
        "table_name": table.name,
        "message": f"Table {table.name} reserved for {req.name}.",
    }
