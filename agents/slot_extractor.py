import re
import dateparser
from difflib import get_close_matches


# ==========================================================
# NUMBER WORDS
# ==========================================================

NUMBER_WORDS = {
    "one": 1,
    "won": 1,
    "wan": 1,
    "two": 2,
    "to": 2,
    "too": 2,
    "tue": 2,
    "three": 3,
    "tree": 3,
    "free": 3,
    "four": 4,
    "for": 4,
    "fore": 4,
    "five": 5,
    "fife": 5,
    "six": 6,
    "sicks": 6,
    "seven": 7,
    "eight": 8,
    "ate": 8,
    "nine": 9,
    "nein": 9,
    "ten": 10,
    "tin": 10,
}

# ==========================================================
# MEAL SLOT ALIASES
# ==========================================================

MEAL_SLOT_ALIASES = {
    "breakfast": [
        "breakfast",
        "break fast",
        "brekfast",
        "breakfest",
        "breakfas",
        "morning",
        "morni",
        "mornin",
        "early meal",
        "brakefast",
        "brakfast",
        "brekfest",
        "breakfeast",
    ],
    "lunch": [
        "lunch",
        "launch",
        "lonch",
        "lunsh",
        "luch",
        "lnch",
        "lunchtime",
        "lunch time",
        "afternoon",
        "noon",
        "midday",
        "lawnch",
        "lanch",
        "lunche",
    ],
    "dinner": [
        "dinner",
        "diner",
        "dinr",
        "dinne",
        "supper",
        "evening",
        "night",
        "nite",
        "eve",
        "evenin",
        "evenning",
        "dinnr",
        "dinnner",
        "dinar",
        "dyner",
    ],
}

# ==========================================================
# SECTION ALIASES
# ==========================================================

SECTION_ALIASES = {
    "ac": [
        "ac",
        "a c",
        "air conditioned",
        "air conditioning",
        "air-conditioned",
        "with ac",
        "with a c",
        "cooled",
        "air cool",
        "airconditioned",
    ],
    "non_ac": [
        "non ac",
        "non-ac",
        "non a c",
        "no ac",
        "without ac",
        "without a c",
        "non air",
        "open",
        "outdoor",
        "outside",
        "no air",
        "non airconditioned",
    ],
}

# ==========================================================
# FUZZY MATCH
# ==========================================================


def fuzzy_match(text: str, aliases: dict) -> str | None:
    text = text.lower().strip()

    for canonical, words in aliases.items():
        for alias in words:
            if alias in text:
                return canonical

    all_aliases = []
    alias_to_canonical = {}
    for canonical, words in aliases.items():
        for alias in words:
            all_aliases.append(alias)
            alias_to_canonical[alias] = canonical

    tokens = re.findall(r"\b\w+\b", text)
    for token in tokens:
        matches = get_close_matches(token, all_aliases, n=1, cutoff=0.75)
        if matches:
            return alias_to_canonical[matches[0]]

    matches = get_close_matches(text, all_aliases, n=1, cutoff=0.65)
    if matches:
        return alias_to_canonical[matches[0]]

    return None


# ==========================================================
# NAME BLACKLIST — words that must never be treated as names
# ==========================================================

NAME_BLACKLIST = {
    "here",
    "calling",
    "speaking",
    "there",
    "fine",
    "good",
    "okay",
    "ok",
    "yes",
    "no",
    "sure",
    "hello",
    "hi",
    "hey",
    "thanks",
    "thank",
    "please",
    "breakfast",
    "lunch",
    "dinner",
    "morning",
    "evening",
    "night",
    "ac",
    "booking",
    "table",
    "reserve",
    "reservation",
    "dining",
    "restaurant",
    "today",
    "tomorrow",
    "monday",
    "tuesday",
    "wednesday",
    "thursday",
    "friday",
    "saturday",
    "sunday",
    "january",
    "february",
    "march",
    "april",
    "may",
    "june",
    "july",
    "august",
    "september",
    "october",
    "november",
    "december",
    "want",
    "like",
    "need",
    "prefer",
    "would",
    "could",
    "ek",
    "first",
    "second",
    "third",
    "one",
    "two",
    "three",
    "four",
    "five",
    "six",
    "seven",
    "eight",
    "nine",
    "ten",
    "actually",
    "exactly",
    "just",
}


def extract_name(text: str) -> str | None:
    text = text.strip()

    # Pattern 1: explicit name phrases
    patterns = [
        r"(?:my name is|i am|i'm|this is|call me|it'?s|name is)\s+([A-Za-z]+(?:\s+[A-Za-z]+)?)",
    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            name = match.group(1).strip()
            words = name.lower().split()
            if not any(w in NAME_BLACKLIST for w in words):
                return name.title()

    # Pattern 2: bare short response (user just said their name)
    # Only trigger if text is 1-2 alpha words AND not blacklisted
    words = text.strip().split()
    if 1 <= len(words) <= 2:
        if all(w.isalpha() for w in words):
            if not any(w.lower() in NAME_BLACKLIST for w in words):
                return text.title()

    return None


# ==========================================================
# EXTRACT DATE
# ==========================================================


def extract_date(text: str) -> str | None:
    parsed = dateparser.parse(
        text,
        settings={
            "PREFER_DATES_FROM": "future",
            "RETURN_AS_TIMEZONE_AWARE": False,
        },
    )
    if parsed:
        return parsed.strftime("%Y-%m-%d")

    match = re.search(r"\b(\d{4})\s+(\d{1,2})\s+(\d{1,2})\b", text)
    if match:
        y, m, d = match.groups()
        return f"{y}-{m.zfill(2)}-{d.zfill(2)}"

    return None


# ==========================================================
# EXTRACT PEOPLE — strips date numbers before scanning
# ==========================================================


def extract_people(text: str) -> int | None:
    # Remove year numbers (2024, 2025, 2026...)
    cleaned = re.sub(r"\b(19|20)\d{2}\b", "", text)

    # Remove day+month combos like "13th March", "March 13"
    cleaned = re.sub(
        r"\b(0?[1-9]|[12]\d|3[01])(st|nd|rd|th)?\b\s*"
        r"(january|february|march|april|may|june|july|august|"
        r"september|october|november|december)\b",
        "",
        cleaned,
        flags=re.IGNORECASE,
    )
    cleaned = re.sub(
        r"\b(january|february|march|april|may|june|july|august|"
        r"september|october|november|december)\b\s*\d{0,2}",
        "",
        cleaned,
        flags=re.IGNORECASE,
    )

    # Remove date-like standalone day numbers (13, 14, 25 etc > 20)
    # Only keep numbers 1–20 as valid guest counts
    match = re.search(r"\b([1-9]|1[0-9]|20)\b", cleaned)
    if match:
        return int(match.group(1))

    # Word numbers with fuzzy matching
    tokens = re.findall(r"\b\w+\b", cleaned.lower())
    for token in tokens:
        if token in NUMBER_WORDS:
            return NUMBER_WORDS[token]
        matches = get_close_matches(token, NUMBER_WORDS.keys(), n=1, cutoff=0.75)
        if matches:
            return NUMBER_WORDS[matches[0]]

    return None


# ==========================================================
# EXTRACT SECTION & MEAL SLOT
# ==========================================================


def extract_section(text: str) -> str | None:
    return fuzzy_match(text, SECTION_ALIASES)


def extract_meal_slot(text: str) -> str | None:
    return fuzzy_match(text, MEAL_SLOT_ALIASES)


# ==========================================================
# COMBINED EXTRACTOR
# ==========================================================


def extract_slots(query: str) -> dict:
    return {
        "name": extract_name(query),
        "date": extract_date(query),
        "people": extract_people(query),
        "section": extract_section(query),
        "meal_slot": extract_meal_slot(query),
    }
