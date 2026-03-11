from typing import TypedDict, List
from langchain_core.messages import BaseMessage


class BookingState(TypedDict):
    messages: List[BaseMessage]
