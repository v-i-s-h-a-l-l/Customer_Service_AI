import requests
from langchain.tools import tool


@tool
def reserve_table(
    name: str,
    date: str,
    meal_slot: str,
    people: int,
    section: str,
):
    """
    Reserve a restaurant table at Aurora Dining.

    Args:
        name:      Guest's full name
        date:      Reservation date in YYYY-MM-DD format
        meal_slot: One of 'breakfast', 'lunch', or 'dinner'
        people:    Number of guests
        section:   'ac' or 'non_ac'
    """

    response = requests.post(
        "http://localhost:8000/restaurant/reserve",
        json={
            "name": name,
            "date": date,
            "meal_slot": meal_slot,
            "people": people,
            "section": section,
        },
        timeout=10,
    )

    response.raise_for_status()
    return response.json()
