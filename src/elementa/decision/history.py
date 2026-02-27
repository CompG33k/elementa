from dataclasses import dataclass, field
from typing import Dict, Tuple, Optional
from elementa.core.models import Action

@dataclass
class History:
    last_screen_id: Optional[str] = None
    # (action_type, element_id, text) -> count
    attempts: Dict[Tuple[str, str, str], int] = field(default_factory=dict)

    def key(self, action: Action) -> Tuple[str, str, str]:
        return (action.type, action.element_id or "", action.text or "")

    def increment(self, action: Action) -> int:
        k = self.key(action)
        self.attempts[k] = self.attempts.get(k, 0) + 1
        return self.attempts[k]

    def attempts_for(self, action: Action) -> int:
        return self.attempts.get(self.key(action), 0)