from elementa.core.models import UIElement, ScreenModel, TaskSpec
from elementa.decision.engine import DecisionEngine

screen = ScreenModel(
    screen_id="1",
    elements=[
        UIElement("1", "input", "Email Address", None),
        UIElement("2", "button", "Next", None),
        UIElement("3", "button", "Submit Application", None),
    ]
)

task = TaskSpec(
    goal="Apply to job",
    profile={"email": "nick@email.com"}
)

engine = DecisionEngine()
print(engine.tick(task, screen))