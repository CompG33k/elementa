from elementa.core.models import UIElement, ScreenModel, TaskSpec
from elementa.decision.engine import DecisionEngine

screen = ScreenModel(
    screen_id="1",
    elements=[
        UIElement("cb1", "checkbox", "I agree to the Terms", None, enabled=True, checked=False),
        UIElement("in1", "input", "Email Address", None),
        UIElement("btn1", "button", "Next", None),
        UIElement("btn2", "button", "Submit Application", None),
    ]
)

task = TaskSpec(
    goal="Apply to job",
    profile={"email": "nick@email.com"},
    require_submit_confirm=True,
)

engine = DecisionEngine()
print(engine.tick(task, screen))

