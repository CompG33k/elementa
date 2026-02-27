from elementa.core.models import UIElement, ScreenModel, TaskSpec
from elementa.decision.engine import DecisionEngine

def make_task():
    return TaskSpec(
        goal="Apply to job",
        profile={"email": "nick@email.com"},
        require_submit_confirm=True,
    )

def scenario_1():
    # Unchecked terms + empty email -> should CLICK checkbox first (or TYPE email depending on policy order)
    return ScreenModel(
        screen_id="1",
        elements=[
            UIElement("cb1", "checkbox", "I agree to the Terms", None, enabled=True, checked=False),
            UIElement("in1", "input", "Email Address", None),
            UIElement("btn1", "button", "Next", None),
            UIElement("btn2", "button", "Submit Application", None),
        ],
    )

def scenario_2():
    # Terms checked + empty email -> should TYPE email
    return ScreenModel(
        screen_id="2",
        elements=[
            UIElement("cb1", "checkbox", "I agree to the Terms", None, enabled=True, checked=True),
            UIElement("in1", "input", "Email Address", None),
            UIElement("btn1", "button", "Next", None),
            UIElement("btn2", "button", "Submit Application", None),
        ],
    )

def scenario_3():
    # Terms checked + email filled -> should CLICK Next
    return ScreenModel(
        screen_id="3",
        elements=[
            UIElement("cb1", "checkbox", "I agree to the Terms", None, enabled=True, checked=True),
            UIElement("in1", "input", "Email Address", "nick@email.com"),
            UIElement("btn1", "button", "Next", None),
            UIElement("btn2", "button", "Submit Application", None),
        ],
    )

def scenario_4_submit_only():
    # Only submit remains -> should ASK_USER (gated) not CLICK
    return ScreenModel(
        screen_id="4",
        elements=[
            UIElement("btn2", "button", "Submit Application", None),
        ],
    )

if __name__ == "__main__":
    task = make_task()
    engine = DecisionEngine()

    # Keep your original behavior (single call)
    print("Single tick (original):")
    print(engine.tick(task, scenario_1()))
    print()

    # Added: flow verification
    print("Flow test:")
    for s in [scenario_1(), scenario_2(), scenario_3(), scenario_4_submit_only()]:
        action = engine.tick(task, s)
        print(f"screen_id={s.screen_id} -> {action}")