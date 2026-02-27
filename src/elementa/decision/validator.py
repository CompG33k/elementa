from elementa.core.models import Action, ScreenModel

def _find(screen: ScreenModel, element_id: str):
    for e in screen.elements:
        if e.element_id == element_id:
            return e
    return None

def verify(action: Action, before: ScreenModel, after: ScreenModel) -> bool:
    if action.type == "TYPE" and action.element_id:
        b = _find(before, action.element_id)
        a = _find(after, action.element_id)
        if not a:
            return False
        # simplest: value text changed OR contains some of the typed text
        typed = (action.text or "").strip().lower()
        after_val = (a.value_text or "").strip().lower()
        if typed and after_val:
            return typed[: max(3, len(typed)//3)] in after_val or after_val != ((b.value_text or "").strip().lower())
        return False

    if action.type == "CLICK" and action.element_id:
        # simplest: screen changed
        return before.screen_id != after.screen_id

    if action.type in ("WAIT", "ASK_USER", "STOP"):
        return True

    return False