"""The COD confirmation conversation, as data.

Each node says one line and maps the customer's intent to the next node.
`pipeline.py` walks this graph during a call; later the dashboard's script
editor will let each seller change the SCRIPT texts.
"""

# Default lines (Hinglish). Placeholders are filled per order by render().
SCRIPT = {
    "greet": "Namaste {name} ji, main {brand} se {agent} bol rahi hoon. Aapne {amount} ka "
             "{product} order kiya hai, cash on delivery. Kya hum ise ship kar dein?",
    "confirm_address": "Bahut badhiya! Aapka delivery address hai: {address}. Kya ye sahi hai?",
    "take_new_address": "Koi baat nahi, naya address bata dijiye.",
    "close_confirmed": "Dhanyavaad {name} ji! Aapka order 2-3 din mein pahunch jayega.",
    "ask_reason": "Koi baat nahi. Kya aap bata sakte hain ki cancel kyun karna hai?",
    "close_cancelled": "Samajh gayi. Aapka order cancel kar diya gaya hai. Dhanyavaad!",
    "ask_callback_time": "Bilkul, koi baat nahi. Aapko kab call karein?",
    "close_callback": "Theek hai, main {callback_time} call karungi. Dhanyavaad!",
}

# Outcomes written back to the order and the Shopify tag.
CONFIRMED, CANCELLED, CALLBACK, NO_ANSWER = "confirmed", "cancelled", "callback", "no_answer"
SHOPIFY_TAGS = {
    CONFIRMED: "cod-confirmed",
    CANCELLED: "cod-cancelled",
    CALLBACK: "cod-callback",
    NO_ANSWER: "cod-no-answer",
}

# node -> {"say": SCRIPT key, "next": {intent: node}} or {"say": ..., "end": outcome}
FLOW = {
    "greet": {"say": "greet", "next": {"yes": "confirm_address", "no": "ask_reason", "later": "ask_callback_time"}},
    "confirm_address": {"say": "confirm_address", "next": {"yes": "close_confirmed", "no": "take_new_address"}},
    "take_new_address": {"say": "take_new_address", "next": {"address_given": "close_confirmed"}},
    "close_confirmed": {"say": "close_confirmed", "end": CONFIRMED},
    "ask_reason": {"say": "ask_reason", "next": {"reason_given": "close_cancelled"}},
    "close_cancelled": {"say": "close_cancelled", "end": CANCELLED},
    "ask_callback_time": {"say": "ask_callback_time", "next": {"time_given": "close_callback"}},
    "close_callback": {"say": "close_callback", "end": CALLBACK},
}
START = "greet"

_MALE_FORMS = {"rahi hoon": "raha hoon", "karungi": "karunga", "Samajh gayi": "Samajh gaya"}


def render(text: str, values: dict, agent_is_male: bool = False) -> str:
    """Fill {placeholders} and switch verb gender for a male agent voice."""
    out = text.format_map(_Blank(values))
    if agent_is_male:
        for female, male in _MALE_FORMS.items():
            out = out.replace(female, male)
    return out


class _Blank(dict):
    """Leaves unknown placeholders visible instead of raising KeyError."""
    def __missing__(self, key):
        return "{" + key + "}"


def validate(flow: dict = FLOW, script: dict = SCRIPT) -> list[str]:
    """Problems in the flow graph (empty list means it is valid)."""
    problems = []
    if START not in flow:
        problems.append(f"start node '{START}' missing")
    for name, node in flow.items():
        if node["say"] not in script:
            problems.append(f"{name}: no script line '{node['say']}'")
        if ("next" in node) == ("end" in node):
            problems.append(f"{name}: needs exactly one of 'next' or 'end'")
        for intent, target in node.get("next", {}).items():
            if target not in flow:
                problems.append(f"{name}: '{intent}' points to unknown node '{target}'")
        if node.get("end") and node["end"] not in SHOPIFY_TAGS:
            problems.append(f"{name}: unknown outcome '{node['end']}'")
    return problems
