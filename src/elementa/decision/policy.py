from elementa.core.models import Action
from .field_map import best_profile_match, normalize

NEXT_WORDS = ["next", "continue", "save and continue", "proceed"]
SUBMIT_WORDS = ["submit", "apply", "finish", "pay", "send", "confirm"]
TERMS_WORDS = ["i agree", "agree", "terms", "conditions", "privacy", "consent"]

def contains_any(text: str, words: list[str]) -> bool:
    t = normalize(text)
    return any(w in t for w in words)

def value_matches(expected: str, observed: str | None) -> bool:
    if not observed:
        return False
    e = normalize(expected)
    o = normalize(observed)
    if "@" in e:  # email heuristic
        return "@" in o and e.replace(" ", "") in o.replace(" ", "")
    return e in o

def next_action(screen, task_spec):

    # 1) Accept terms checkbox if allowed
    for el in screen.elements:
        if el.role == "checkbox" and el.enabled and el.label_text and contains_any(el.label_text, TERMS_WORDS):
            if getattr(task_spec, "allow_accept_terms", True) and el.checked is False:
                return Action(type="CLICK", element_id=el.element_id, reason="Accepting terms checkbox")

    # 2) Fill inputs (skip if already correct)
    for el in screen.elements:
        if el.role not in ("input", "textarea") or not el.enabled:
            continue
        if not el.value_text or not el.label_text:
            continue

        key, value, score = best_profile_match(el.label_text, task_spec.profile)
        if not key or score <= 70:
            continue

        if value_matches(value, el.value_text):
            continue

        return Action(type="TYPE", element_id=el.element_id, text=value, reason=f"Filling {key} (score {score})")

    # 3) Click Next/Continue
    for el in screen.elements:
        if el.role == "button" and el.enabled and el.label_text and contains_any(el.label_text, NEXT_WORDS):
            return Action(type="CLICK", element_id=el.element_id, reason="Clicking Next/Continue", risk="MEDIUM")

    # 4) Detect Submit/Apply (gated later)
    for el in screen.elements:
        if el.role == "button" and el.enabled and el.label_text and contains_any(el.label_text, SUBMIT_WORDS):
            return Action(type="CLICK", element_id=el.element_id, reason="Submit/Apply detected", risk="HIGH")

    return Action(type="WAIT", reason="Nothing to do")