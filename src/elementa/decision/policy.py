from elementa.core.models import Action
from .field_map import best_profile_match


SUBMIT_WORDS = ["submit", "apply", "finish", "pay"]
NEXT_WORDS = ["next", "continue"]


def next_action(screen, task_spec):

    # 1. Fill empty inputs
    for el in screen.elements:
        if el.role == "input" and el.enabled:
            if not el.value_text:
                if el.label_text:
                    key, value, score = best_profile_match(el.label_text, task_spec.profile)
                    if key and score > 70:
                        return Action(
                            type="TYPE",
                            element_id=el.element_id,
                            text=value,
                            reason=f"Filling {key}"
                        )

    # 2. Click Next if exists
    for el in screen.elements:
        if el.role == "button" and el.label_text:
            text = el.label_text.lower()
            if any(w in text for w in NEXT_WORDS):
                return Action(
                    type="CLICK",
                    element_id=el.element_id,
                    reason="Clicking Next"
                )

    # 3. Submit (guarded)
    for el in screen.elements:
        if el.role == "button" and el.label_text:
            text = el.label_text.lower()
            if any(w in text for w in SUBMIT_WORDS):
                return Action(
                    type="CLICK",
                    element_id=el.element_id,
                    reason="Submit detected",
                    risk="HIGH"
                )

    return Action(type="WAIT", reason="Nothing to do")