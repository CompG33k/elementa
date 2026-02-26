# Elementa (WIP)

Elementa is a **fully offline UI automation agent** that can:
- **Fill forms** (job applications, signups, onboarding flows)
- **Run UI testing flows** (click paths, assertions, regressions)
- **Navigate multi-step pages** safely (with submit confirmation gates)

The system uses an on-device pipeline:

**Screen → Detect UI elements → Understand state → Decide next action → Execute → Verify**

No cloud dependency. No GPT subscription required.

---

## Architecture (high level)

Elementa is split into two major subsystems:

### 1) Perception (Eyes)
Transforms screenshots into a structured `ScreenModel`:
- UI element bounding boxes
- Element roles (input/button/checkbox/dropdown/link)
- OCR text for labels and values
- Basic state estimation (enabled/checked/focused/required)
- Stable element IDs across frames (tracking)

**Typical stack:** YOLOv8 + OCR (EasyOCR) + element association/tracking

### 2) Decision (Brain)
Consumes `ScreenModel` + `TaskSpec` and produces a single safe next action:
- Rule-based policy (deterministic MVP)
- Safety guardrails (submit/pay/delete confirmation)
- Validation + retry logic (verify actions worked, avoid loops)
- Optional LLM planner for ambiguous cases (offline Llama)

**Typical stack:** Python decision engine + policy + safety + validator + history

---

## Goals

### MVP 1 — Offline Smart Form Filler
- Fill common fields (name, email, phone, city, LinkedIn, website)
- Click "Next/Continue"
- Never click "Submit/Apply" without explicit confirmation
- Log every decision and verification result

### MVP 2 — UI Test Runner
- Execute known flows robustly using perception-based targeting
- Add simple assertions (element exists, text visible, checkbox state)

---

## Repository Layout (planned)
