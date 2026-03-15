from typing import TypedDict, List, Optional
from langchain_core.messages import BaseMessage


class BookingState(TypedDict):
    messages: List[BaseMessage]

    # slots
    name: Optional[str]
    date: Optional[str]
    people: Optional[int]
    section: Optional[str]
    meal_slot: Optional[str]
