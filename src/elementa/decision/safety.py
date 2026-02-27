from elementa.core.models import Action

def guard(action: Action, task_spec) -> Action:
    if action.risk == "HIGH" and getattr(task_spec, "require_submit_confirm", True):
        return Action(
            type="ASK_USER",
            element_id=action.element_id,
            reason=f"{action.reason}. Confirmation required.",
            risk="HIGH"
        )
    return action