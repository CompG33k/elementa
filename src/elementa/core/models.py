from dataclasses import dataclass, field
from typing import List, Optional, Dict


@dataclass
class UIElement:
    element_id: str
    role: str  # input, button, checkbox, dropdown, text
    label_text: Optional[str]
    value_text: Optional[str]
    enabled: bool = True
    checked: Optional[bool] = None
    required: Optional[bool] = None
    confidence: float = 1.0


@dataclass
class ScreenModel:
    screen_id: str
    elements: List[UIElement]


@dataclass
class TaskSpec:
    goal: str
    profile: Dict[str, str]
    require_submit_confirm: bool = True


@dataclass
class Action:
    type: str  # TYPE, CLICK, WAIT, ASK_USER, STOP
    element_id: Optional[str] = None
    text: Optional[str] = None
    reason: Optional[str] = None
    risk: str = "LOW"