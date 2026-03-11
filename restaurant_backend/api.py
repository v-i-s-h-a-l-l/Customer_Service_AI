from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from restaurant_backend.database import SessionLocal
from restaurant_backend.schemas import ReservationRequest
from restaurant_backend.booking_service import create_reservation

router = APIRouter(prefix="/restaurant", tags=["restaurant"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/reserve")
def reserve_table(req: ReservationRequest, db: Session = Depends(get_db)):
    result = create_reservation(db, req)

    return result
