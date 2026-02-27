from .policy import next_action
from .safety import guard


class DecisionEngine:

    def tick(self, task_spec, screen):
        action = next_action(screen, task_spec)
        action = guard(action, task_spec)
        return action