def guard(action, task_spec):
    if action.risk == "HIGH" and task_spec.require_submit_confirm:
        action.type = "ASK_USER"
        action.reason = "Submit requires confirmation"
    return action