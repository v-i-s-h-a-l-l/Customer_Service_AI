from pydantic import BaseModel
from typing import Optional


class ReservationRequest(BaseModel):
    name: str
    date: str
    meal_slot: str  # breakfast / lunch / dinner
    people: int
    section: str  # ac / non_ac

    # Optional fields — not collected by voice agent
    email: Optional[str] = "not_provided@aurora.com"
    time: Optional[str] = None
    duration: Optional[str] = None
