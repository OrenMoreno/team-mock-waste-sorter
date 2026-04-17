# Team MOCK — AI-Powered Robotic Waste Sorting System

**ITAI 4376 · Spring 2026 · Capstone Project**

A robotic waste sorting system that uses computer vision to identify recyclable items (plastic, metal, paper/cardboard) and a 6-DOF robotic arm to sort them into the correct bins. Controllable via natural language commands.

**Team MOCK:** Kaylee Auguillard · Oren Moreno · Cheyenne Hathaway · Maria Tanweer Chachar

---

## What This System Does

1. A USB camera watches a workspace containing a piece of waste.
2. A YOLO-based object detection model running on an NVIDIA Jetson Nano classifies the item.
3. A decision node maps the class to a target bin (with a confidence threshold — low-confidence detections go to a default bin).
4. A Yahboom DOFBOT 6-DOF robotic arm picks up the item and drops it in the correct bin.
5. A natural language interface lets a human issue commands like "pause," "disable plastic," or "status" at any time.

Each stage runs as its own ROS node, and the nodes communicate over well-defined topics so development can happen in parallel.

---

## Hardware

- **Robotic arm:** Yahboom DOFBOT (6 servos + gripper)
- **Compute:** NVIDIA Jetson Nano 4GB
- **Expansion board:** Yahboom YB-EVV01 VER:1.2 (I²C address `0x55`)
- **Camera:** USB RGB camera
- **Storage:** 256GB ImageMate microSDXC UHS-I

**Custody:** All physical hardware is with Oren. Any task that touches the robot physically is owned by the Hardware & Robotics Lead.

## Software Stack

- **OS:** Ubuntu 18.04 (JetPack 4.6.1 — the final supported version for Jetson Nano 4GB)
- **Middleware:** ROS Melodic
- **Vision:** YOLOv5n or YOLOv8n, exported to ONNX (optionally TensorRT)
- **Language:** Python 3
- **NLP:** Rule-based / keyword intent matching (exact approach TBD — see `/docs/nlp_command_schema.md` once written)

---

## Team Roles

| Role | Owner | Owns |
|------|-------|------|
| Hardware & Robotics Lead | Oren Moreno | Jetson setup, arm control code, calibration, physical test runs, all hardware work |
| Vision & AI Developer | Kaylee Auguillard | Dataset curation, model training, ONNX export, ROS vision node |
| NLP & Software Integration Developer | Maria Tanweer Chachar | NLP command parser, ROS architecture, decision node, integration |
| QA, Documentation & Project Coordination | Cheyenne Hathaway | Test plans, technical report, meeting notes, milestone tracking |

Every member contributes to other roles during crunch points, but the named owner is accountable for quality and delivery.

---

## Repository Layout

The repo is organized around the ROS node architecture plus supporting directories for documentation, models, and data.

```
team-mock-waste-sorter/
├── README.md                  ← you are here
├── .gitignore
│
├── arm_control/               ← Oren: arm movement code (runs on Jetson)
│   ├── dofbot_controller.py   ← core movement library
│   ├── keyboard_teleop.py     ← manual joint-by-joint control via keyboard
│   ├── pose_loader.py         ← load and execute named poses
│   ├── poses.yaml             ← named bin positions (joint angles)
│   └── target_tracker.py      ← convert pixel coords → arm angles
│
├── vision/                    ← Kaylee: model training + ROS vision node
│   ├── training/              ← training scripts, configs, notebooks
│   ├── models/                ← trained weights (.pt, .onnx) — large files!
│   └── vision_node/           ← ROS package for live inference
│
├── nlp/                       ← Maria: NLP command parsing
│   ├── nlp_node/              ← ROS package for NLP
│   └── command_schema.md      ← supported commands + JSON schema
│
├── decision/                  ← Maria: decision/routing logic
│   └── decision_node/         ← ROS package, subscribes to detections
│
├── msgs/                      ← custom ROS message definitions
│
├── launch/                    ← ROS launch files (system.launch, etc.)
│
├── scripts/                   ← one-off utilities (calibration helpers, etc.)
│
├── tests/                     ← Cheyenne: unit + integration tests
│
├── data/                      ← sample images, calibration data, ROS bags
│                                (not the full training set — too big for git)
│
└── docs/                      ← Cheyenne: all project documentation
    ├── ros_architecture.md    ← node graph + topic list (the master design doc)
    ├── topics.md              ← topic names and message types
    ├── nlp_command_schema.md  ← supported NLP commands
    ├── dataset.md             ← training dataset documentation
    ├── calibration_procedure.md
    ├── hardware_setup.md
    ├── test_plan.md
    ├── evaluation_criteria.md
    ├── technical_report.md    ← final report (draft, grown over the semester)
    ├── meeting_notes/
    ├── progress_reports/
    └── retrospective.md       ← end-of-project
```

Folders will come online as each milestone begins — don't expect them all to exist on day one. If you need a folder that isn't here yet, create it and document what goes in it in `docs/`.

---

## Getting Started

### Prerequisites

Everyone needs:

- **Git** and a GitHub account with access to this repo
- **Python 3.8+**
- A code editor (VS Code recommended — the repo has no fancy IDE config, use whatever you like)

Role-specific extras:

- **Vision (Kaylee):** PyTorch, OpenCV, Ultralytics YOLOv5/v8. GPU recommended for training (Google Colab free tier works fine if no local GPU).
- **NLP/Integration (Maria):** ROS Melodic on your development machine — or the `osrf/ros:melodic-desktop` Docker image, which is simpler to set up on Windows/Mac.
- **Hardware (Oren):** The actual Jetson Nano + arm. Everyone else can develop without it.

### Cloning the Repo

```bash
git clone <repo-url> team-mock-waste-sorter
cd team-mock-waste-sorter
```

### Running the Arm Control Code (dry-run on your laptop)

You don't need the physical arm to test most of the arm-control logic. On any machine with Python 3:

```bash
cd arm_control
python3 keyboard_teleop.py
```

Without the Yahboom `Arm_Lib` module installed, the controller enters "dry run" mode — it prints every command it *would* send to the servos without actually moving anything. This lets anyone verify the code logic without the hardware.

### Running on the Jetson

Once the Jetson is set up (see `docs/hardware_setup.md` when it exists) and the Yahboom SDK is installed, the same script drives the real arm:

```bash
cd ~/arm_control
python3 keyboard_teleop.py
```

### Running the Full ROS System (once integration is complete)

Target for Milestone 6:

```bash
roslaunch team_mock_waste_sorter system.launch
```

(Not functional yet — this is the eventual one-command launch.)

---

## How to Contribute

### Branching

We use a simple branching model — no gitflow overhead for a project this size.

- **`main`** is always kept in a working state. Nothing gets pushed directly here.
- For any work, create a feature branch from `main`:
  ```bash
  git checkout main
  git pull
  git checkout -b <your-name>/<short-description>
  # e.g., oren/arm-controller, kaylee/yolo-export, maria/nlp-parser
  ```
- When your work is ready, open a pull request into `main`. At least one other team member should review before merging.
- Delete your branch after it's merged.

### Commit Messages

Keep them short and descriptive. Prefix with the area you're working in so it's easy to scan the log:

```
arm_control: add gripper open/close helpers
vision: switch to YOLOv8n, update training config
nlp: add 'status' command handler
docs: draft calibration procedure
```

### Pull Requests

In the PR description, include:

- **What** you changed
- **Why** (link to the milestone task if relevant)
- **How to test** — can a reviewer run something to verify it works? Especially important for hardware-dependent code where the reviewer might not be able to run it themselves.

Tag the milestone in the PR title: `[M3] Add keyboard teleop script`.

### Code Style

- **Python:** follow PEP 8 loosely. Use descriptive variable names. Add docstrings to public functions.
- **Comments:** explain *why*, not *what*. The code shows what it does; comments should capture intent and gotchas.
- No linter is enforced — use your judgment, and don't rewrite someone else's style when editing their code.

### Large Files

Model weights, datasets, ROS bags, and videos **do not go in git**. Use the team shared drive for those. The `.gitignore` already excludes `.pt`, `.onnx`, `.engine`, and common build artifacts — add more patterns there if needed.

### Updating Documentation

Docs are part of every feature. If you change how something works, update the relevant file in `docs/`. If you make an architectural decision (e.g., picking a library, defining a message format), document the decision and the reasoning — future-you will forget.

---

## Milestone Schedule

| # | Milestone | Weeks | Exit Condition |
|---|-----------|-------|----------------|
| M1 | Environment & Infrastructure Setup | 1–2 | Toolchains installed; repo live; arm responds to basic commands |
| M2 | Vision Pipeline Development | 3–4 | Model detects ≥3 waste classes at ≥80% accuracy; ROS vision node active |
| M3 | Robotic Control & Calibration | 4–5 | Arm completes pick-and-place at 3 known positions; pixel-to-arm transform calibrated |
| M4 | Decision Logic & Subsystem Integration | 6–7 | End-to-end pipeline works; NLP commands functional |
| M5 | System Testing & Optimization | 8–9 | ≥75% correct sorting over 20 trials; safety behaviors confirmed |
| M6 | Final Demonstration & Deliverables | 10–11 | All deliverables submitted; demo completed |

Full milestone details with per-role tasks live in the project execution plan document (in the team shared drive).

---

## Communication

- **Weekly sync:** (set day/time in team notes)
- **Async updates:** team chat
- **Decisions & action items:** captured in `docs/meeting_notes/` after each meeting
- **Blockers:** call them out early — don't sit on one for more than a day without flagging it

---

## Key External Resources

- [Yahboom DOFBOT documentation](https://category.yahboom.net/products/dofbot-jetson_nano)
- [NVIDIA JetPack downloads](https://developer.nvidia.com/embedded/jetpack)
- [ROS Melodic installation](https://wiki.ros.org/melodic/Installation/Ubuntu)
- [YOLOv5 (Ultralytics)](https://github.com/ultralytics/yolov5)
- [YOLOv8 docs](https://docs.ultralytics.com)
- [TACO trash dataset](https://github.com/pedropro/TACO)
- [Roboflow](https://roboflow.com) — dataset management and labeling
- [LabelImg](https://github.com/HumanSignal/labelImg) — alternative labeling tool
- [TensorRT for Jetson](https://docs.nvidia.com/deeplearning/tensorrt/developer-guide)
