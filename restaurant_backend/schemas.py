from pydantic import BaseModel


class ReservationRequest(BaseModel):
    name: str
    email: str

    date: str
    time: str

    people: int

    section: str

    duration: str
