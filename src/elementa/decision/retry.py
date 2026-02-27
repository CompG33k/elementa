from elementa.core.models import Action

MAX_ATTEMPTS_PER_ACTION = 2

def should_retry(attempt_count: int) -> bool:
    return attempt_count <= MAX_ATTEMPTS_PER_ACTION

def failure_action(action: Action) -> Action:
    return Action(
        type="ASK_USER",
        element_id=action.element_id,
        reason=f"Action failed repeatedly: {action.reason}",
        risk=action.risk,
    )