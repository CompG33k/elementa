from elementa.core.models import Action, ScreenModel, TaskSpec
from .policy import next_action
from .safety import guard
from .history import History
from .retry import failure_action


class DecisionEngine:
    def __init__(self):
        self.history = History()

    def tick(self, task_spec, screen):
        action = next_action(screen, task_spec)
        return guard(action, task_spec)   
 
    def tick(self, task: TaskSpec, screen: ScreenModel) -> Action:
        action = next_action(screen, task)
        action = guard(action, task)

        # prevent infinite loops
        count = self.history.increment(action)
        if count > 2 and action.type in ("TYPE", "CLICK"):
            return failure_action(action)

        self.history.last_screen_id = screen.screen_id
        return action