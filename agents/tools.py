import requests
from langchain.tools import tool


@tool
def reserve_table(
    name: str,
    email: str,
    date: str,
    time: str,
    people: int,
    section: str,
    duration: str,
):
    """Reserve a restaurant table"""

    response = requests.post(
        "http://localhost:8000/restaurant/reserve",
        json={
            "name": name,
            "email": email,
            "date": date,
            "time": time,
            "people": people,
            "section": section,
            "duration": duration,
        },
    )

    return response.json()
