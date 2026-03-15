from agents.tools import reserve_table
from agents.slot_extractor import extract_slots


# ==========================================================
# SLOT MEMORY PER USER
# ==========================================================

slot_memory: dict = {}


def initialize_user_slots(user_id: str):
    if user_id not in slot_memory:
        slot_memory[user_id] = {
            "name": None,
            "date": None,
            "people": None,
            "section": None,
            "meal_slot": None,
        }


def reset_user_slots(user_id: str):
    slot_memory[user_id] = {
        "name": None,
        "date": None,
        "people": None,
        "section": None,
        "meal_slot": None,
    }


# ==========================================================
# BOOKING AGENT
# ==========================================================


def run_booking_agent(user_id: str, query: str) -> str:
    initialize_user_slots(user_id)

    user_slots = slot_memory[user_id]

    # ----------------------------------------------------------
    # Extract slots from current message
    # ----------------------------------------------------------
    slots = extract_slots(query)

    print(f"DEBUG extracted slots : {slots}")
    print(f"DEBUG memory before   : {user_slots}")

    # Name — accept any time
    if slots.get("name"):
        user_slots["name"] = slots["name"]

    # Date — accept any time
    if slots.get("date"):
        user_slots["date"] = slots["date"]

    # Meal slot — accept any time
    if slots.get("meal_slot"):
        user_slots["meal_slot"] = slots["meal_slot"]

    # ✅ People — ONLY accept after date + meal_slot are confirmed
    # This prevents stray numbers inside date phrases (e.g. "March 14")
    # from being mistaken as the guest count
    if slots.get("people") and user_slots["date"] and user_slots["meal_slot"]:
        user_slots["people"] = slots["people"]

    # Section — accept any time
    if slots.get("section"):
        user_slots["section"] = slots["section"]

    print(f"DEBUG memory after    : {user_slots}")

    # ----------------------------------------------------------
    # SLOT FILLING — ask one question at a time in order
    # ----------------------------------------------------------

    if not user_slots["name"]:
        return (
            "Welcome to Aurora Dining! I'd be happy to help you reserve a table. "
            "May I know your name please?"
        )

    name = user_slots["name"]

    if not user_slots["date"]:
        return (
            f"Thank you, {name}! What date would you like to book the table? "
            "You can say something like 'tomorrow' or 'this Saturday'."
        )

    if not user_slots["meal_slot"]:
        return (
            f"Got it! Would you prefer breakfast, lunch, or dinner on that day, {name}?"
        )

    if not user_slots["people"]:
        return f"How many people will be dining, {name}?"

    if not user_slots["section"]:
        return f"And would you prefer AC dining or Non-AC dining, {name}?"

    # ----------------------------------------------------------
    # ALL SLOTS FILLED → BOOK
    # ----------------------------------------------------------

    meal_display = user_slots["meal_slot"].capitalize()
    section_display = "AC" if user_slots["section"] == "ac" else "Non-AC"

    try:
        result = reserve_table.invoke(
            {
                "name": user_slots["name"],
                "date": user_slots["date"],
                "meal_slot": user_slots["meal_slot"],
                "people": user_slots["people"],
                "section": user_slots["section"],
            }
        )

        reset_user_slots(user_id)

        return (
            f"Your table has been successfully reserved, {name}! "
            f"Here's a summary: {user_slots['people']} guest(s), "
            f"{meal_display} on {user_slots['date']}, "
            f"{section_display} section. "
            f"We look forward to seeing you at Aurora Dining!"
        )

    except Exception as e:
        reset_user_slots(user_id)
        return (
            f"I'm sorry {name}, something went wrong while booking your table. "
            f"Please try again or call us directly. Error: {str(e)}"
        )
