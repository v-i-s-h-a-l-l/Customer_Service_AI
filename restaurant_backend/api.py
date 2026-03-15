from fastapi import APIRouter, Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from restaurant_backend.database import SessionLocal
from restaurant_backend.schemas import ReservationRequest
from restaurant_backend.booking_service import create_reservation
from restaurant_backend.models import Reservation

# Main FastAPI application
app = FastAPI(title="Aurora Restaurant Backend")

# Allow frontend (Next.js dev/prod) to call the API from the browser
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Router for restaurant operations
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


@router.get("/orders")
def get_orders(db: Session = Depends(get_db)):
    reservations = db.query(Reservation).order_by(Reservation.id.desc()).all()
    return [
        {
            "id": r.id,
            "customer_name": r.customer_name,
            "email": r.email,
            "date": r.date,
            "time": r.time,
            "people": r.people,
            "section": r.section,
            "duration": r.duration,
            "table_id": r.table_id,
        }
        for r in reservations
    ]


# Attach router to app
app.include_router(router)
