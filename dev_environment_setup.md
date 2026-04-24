# Development Environment Setup

**Team MOCK · ITAI 4376 · Spring 2026**

This guide walks you through setting up your development environment for the AI-Powered Robotic Waste Sorting System project. It covers both **Visual Studio** (the full IDE from Microsoft) and **Visual Studio Code** (the lightweight code editor) — pick whichever you prefer. You only need one.

If you've never used a Python virtual environment before, or never been on a team that shares code through GitHub, this guide is written for you. Read §1 and §2 before jumping to the install steps — the *why* makes the *how* much easier to follow.

---

## Table of Contents

1. [Why use a virtual environment?](#1-why-use-a-virtual-environment)
2. [What you'll end up with](#2-what-youll-end-up-with)
3. [Prerequisites](#3-prerequisites)
4. [Get the code](#4-get-the-code)
5. [Path A — Setup with VS Code (recommended for this project)](#5-path-a--setup-with-vs-code)
6. [Path B — Setup with Visual Studio](#6-path-b--setup-with-visual-studio)
7. [Installing the project dependencies](#7-installing-the-project-dependencies)
8. [Verify everything works](#8-verify-everything-works)
9. [Day-to-day workflow](#9-day-to-day-workflow)
10. [Git & GitHub basics for first-time team projects](#10-git--github-basics-for-first-time-team-projects)
11. [Troubleshooting](#11-troubleshooting)

---

## 1. Why use a virtual environment?

A **virtual environment** (or *venv* for short) is a self-contained folder that holds a specific version of Python and a specific set of installed packages, separate from everything else on your computer.

Here's the problem it solves. Say you install `ultralytics` globally for this class. Next semester you take a different class that needs an older, incompatible version of `ultralytics`. You install it — and now *this* project breaks, because you only have one Python installation and it can only hold one version of each package at a time.

With a venv, each project gets its own sandbox:

- **No conflicts.** Project A's packages never interfere with Project B's.
- **Reproducible setups.** Every teammate installs from the same `requirements.txt` into their own venv, so you're all running the same versions. Bugs you hit, they can reproduce. Code that works for them works for you.
- **No administrator/sudo needed.** Packages install into the venv folder, not into system Python.
- **Easy cleanup.** Done with a project? Delete the venv folder. Nothing lingers on your system.
- **Pinned Python version.** You can set the venv to Python 3.10 even if the rest of your system uses 3.13.

**Rule of thumb for this class and beyond:** one venv per project, always. Never `pip install` into system Python.

---

## 2. What you'll end up with

After following this guide, your machine will have:

- Python 3.10 or 3.11 installed (system-wide)
- Git installed and connected to your GitHub account
- The `team-mock-waste-sorter` repo cloned locally
- A folder called `.venv` inside the repo — this is your isolated Python environment
- All project dependencies (from `requirements.txt`) installed inside `.venv`
- Your IDE (VS Code or Visual Studio) configured to use the venv's Python

You'll be able to run the dry-run arm teleop script (`python arm_control/keyboard_teleop.py`) and have it print servo commands without touching any hardware.

---

## 3. Prerequisites

### Python 3.10 or 3.11

Python 3.10 or 3.11 are recommended for this project. 3.12 is fine too. 3.13 works but some packages (notably older PyTorch builds) can lag behind on support.

**Check what you have:**

```powershell
# Windows PowerShell
python --version
# or
py --version
```

```bash
# macOS / Linux
python3 --version
```

**If you don't have it, or have an unsupported version:**

- **Windows:** Download the installer from [python.org](https://www.python.org/downloads/). During install, **check the box "Add python.exe to PATH"** — this is important.
- **macOS:** Install via [python.org](https://www.python.org/downloads/) or Homebrew (`brew install python@3.11`).
- **Linux (Ubuntu/Debian):** `sudo apt install python3.11 python3.11-venv`

### Git

```powershell
git --version
```

If not installed: download from [git-scm.com](https://git-scm.com/downloads).

Then configure it with your identity (only needed once per machine):

```powershell
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
```

The email should match the one on your GitHub account.

### Your IDE

Install one of these:

- **Visual Studio Code** (free, lightweight, cross-platform): [code.visualstudio.com](https://code.visualstudio.com/)
- **Visual Studio** (heavier IDE, Windows/Mac): [visualstudio.microsoft.com](https://visualstudio.microsoft.com/) — during install, select the **"Python development"** workload.

---

## 4. Get the code

Open a terminal (PowerShell on Windows, Terminal on macOS/Linux) and navigate to where you keep code projects. For example:

```powershell
# Windows (PowerShell)
cd C:\Users\<your-username>\source\repos
```

```bash
# macOS / Linux
cd ~/projects
```

Then clone the repo:

```powershell
git clone https://github.com/OrenMoreno/team-mock-waste-sorter.git
cd team-mock-waste-sorter
```

You now have a local copy of the code. From here on, all commands are run from inside the `team-mock-waste-sorter` folder unless noted.

---

## 5. Path A — Setup with VS Code

This is the recommended path for this project — VS Code is lighter, faster to launch, and its Python extension handles venv activation automatically.

### Step 1 — Open the project

```powershell
code .
```

(The `.` means "open the current folder." If `code` isn't recognized, launch VS Code normally and use **File → Open Folder**.)

### Step 2 — Install the Python extension

If you haven't already, install the official **Python** extension by Microsoft. VS Code usually prompts you the first time you open a `.py` file.

### Step 3 — Create the virtual environment

In VS Code, open the command palette:

- Windows/Linux: `Ctrl+Shift+P`
- macOS: `Cmd+Shift+P`

Type **"Python: Create Environment"** and select it. Then choose:

1. **Venv** (not Conda)
2. Your Python 3.10 or 3.11 interpreter
3. Check the box next to `requirements.txt` so it installs dependencies automatically

VS Code creates a `.venv` folder in your project and installs everything from `requirements.txt` into it. You'll see a terminal open and packages download — this takes **5–15 minutes** because PyTorch and Ultralytics are large.

If the GUI option doesn't work, do it manually from the terminal:

```powershell
# Windows PowerShell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

```bash
# macOS / Linux
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

> **PowerShell note:** If you get an error about scripts being disabled when you try to activate, run this once to allow local scripts:
> ```powershell
> Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
> ```

### Step 4 — Tell VS Code to use the venv

Open the command palette again and run **"Python: Select Interpreter"**. Pick the one labeled `.venv` (it'll say something like `Python 3.11.x ('.venv': venv)`).

From now on, when you open a new terminal in VS Code (**Terminal → New Terminal**, or `` Ctrl+` ``), it automatically activates the venv. You'll see `(.venv)` at the start of your prompt.

**Skip to [§7 installing dependencies](#7-installing-the-project-dependencies) if you used manual terminal commands and haven't installed them yet. If you used the GUI wizard with the checkbox, they're already installed — go to [§8 verify](#8-verify-everything-works).**

---

## 6. Path B — Setup with Visual Studio

Use this path if you prefer the full Visual Studio IDE.

### Step 1 — Open the project

- Launch Visual Studio
- Select **File → Open → Folder** and pick your `team-mock-waste-sorter` folder.
  - Use "Open Folder," not "Open Project" — this repo doesn't have a `.sln` solution file.

### Step 2 — Open the Python Environments window

- **View → Other Windows → Python Environments**

You'll see a panel listing every Python installation Visual Studio has detected.

### Step 3 — Add a new virtual environment

- In the Python Environments panel, click **"Add Environment..."**
- In the dialog:
  - **Environment type:** Virtual environment (venv)
  - **Project:** your `team-mock-waste-sorter` folder
  - **Base interpreter:** Python 3.10 or 3.11
  - **Location:** leave as default (`<project>\.venv`)
  - **Install requirements.txt:** check this box (if visible)
- Click **Create**

Visual Studio creates the `.venv` folder, sets it as the active environment for this project, and begins installing dependencies. The output window shows progress. Give it **5–15 minutes**.

### Step 4 — Confirm it's the active environment

In the Python Environments panel, your new `.venv` should show in **bold** — that means it's the active one for this project. If it's not bold, right-click it and select **"Activate Environment"**.

Any Python file you run from inside Visual Studio will now use the venv.

### Step 5 — Open a terminal with the venv active

If you need the command line (you will, eventually — for git, running scripts with arguments, etc.):

- **View → Terminal** (or `` Ctrl+` ``)
- In the terminal, activate the venv manually:
  ```powershell
  .\.venv\Scripts\Activate.ps1
  ```

---

## 7. Installing the project dependencies

If your IDE setup above didn't install dependencies automatically, or if you want to do it manually, here's the procedure.

**First, confirm your venv is active.** You should see `(.venv)` at the start of your terminal prompt. If not, activate it:

```powershell
# Windows PowerShell
.\.venv\Scripts\Activate.ps1
```

```bash
# macOS / Linux
source .venv/bin/activate
```

**Then install:**

```powershell
pip install --upgrade pip
pip install -r requirements.txt
```

### GPU training setup (Vision & AI role only — Kaylee)

If you have an NVIDIA GPU and plan to **train** the model (as opposed to just running inference), install PyTorch with CUDA support *before* running `pip install -r requirements.txt`. The default PyTorch on PyPI is CPU-only.

```powershell
# With venv active — example for CUDA 11.8
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
pip install -r requirements.txt
```

Check your CUDA version first with `nvidia-smi`. For other CUDA versions, visit [pytorch.org/get-started/locally](https://pytorch.org/get-started/locally/) to get the exact command.

If you only need to run inference (test the trained model, not retrain it), the CPU-only PyTorch that comes from `requirements.txt` is enough.

### If you only need part of the project

Not everyone needs every dependency. PyTorch + Ultralytics alone are close to 2 GB. If you're only working on arm control, NLP, or documentation, you can skip them:

1. Open `requirements.txt` in an editor.
2. Comment out (`#` at the start of the line) the `ultralytics`, `torch`, and `torchvision` lines.
3. Run `pip install -r requirements.txt`.

Don't commit this change — it's just for your local install.

---

## 8. Verify everything works

With the venv active, run these checks:

```powershell
python --version
# Should print Python 3.10.x or 3.11.x (whichever you installed)

python -c "import yaml, numpy, cv2; print('Core deps OK')"
# Should print: Core deps OK
```

Then test the dry-run arm controller (this works on any machine — no Jetson needed):

```powershell
cd arm_control
python keyboard_teleop.py
```

You should see:

```
[WARN] Arm_Lib not found - running in DRY RUN mode
=== DOFBOT Keyboard Teleop ===
q/a=base  w/s=shoulder  e/d=elbow  ...
[HOME] Moving to home position...
  Servo 1 -> 90°
  Servo 2 -> 90°
  ...
```

Press a few keys (e.g., `q`, `w`, `o`) to see commands print, then `x` to exit. If this works, you're fully set up.

---

## 9. Day-to-day workflow

Once everything is installed, your daily cycle looks like this:

1. **Open the project** in your IDE. If you use VS Code's integrated terminal, the venv activates automatically. In other terminals, activate manually:

   ```powershell
   .\.venv\Scripts\Activate.ps1     # Windows
   ```

   ```bash
   source .venv/bin/activate        # macOS/Linux
   ```

2. **Pull the latest changes** from your teammates:

   ```powershell
   git checkout main
   git pull
   ```

3. **Check if `requirements.txt` changed** since you last pulled. If it did, re-install:

   ```powershell
   pip install -r requirements.txt
   ```

   (Some teams automate this with a `make dev` script; for a project this size, just remembering to do it after a pull is fine.)

4. **Create a branch for your work:**

   ```powershell
   git checkout -b <your-name>/<short-description>
   # e.g., oren/arm-calibration-poses
   ```

5. **Make changes, test, commit, push, open a pull request.** See §10 below.

6. **When you're done coding for the day,** you don't need to "deactivate" the venv — just close the terminal. If you want to leave the terminal open but exit the venv:

   ```powershell
   deactivate
   ```

---

## 10. Git & GitHub basics for first-time team projects

If you've used Git for solo projects this might feel like overkill, but working on a shared repo has a few conventions that matter.

### The golden rules

- **Never commit directly to `main`.** `main` is the team's source of truth — it should always work. Changes get in through pull requests.
- **Pull before you push.** Always `git pull` at the start of a session. If you push stale code, you'll create merge conflicts for everyone.
- **Commit often, in small logical chunks.** Better to have 5 small commits than 1 giant "did a bunch of stuff" commit. If a change breaks things, you can find and undo just that piece.
- **Never commit secrets.** API keys, passwords, personal config — never. Once it's in git history, it's basically public.
- **Never commit `.venv/`** or other large generated folders. The repo's `.gitignore` should already exclude them, but if in doubt, check `git status` before committing.

### Typical feature workflow

```powershell
# Start from an up-to-date main
git checkout main
git pull

# Branch off
git checkout -b oren/add-gripper-tuning

# ... make changes, save files ...

# See what changed
git status
git diff

# Stage and commit
git add arm_control/dofbot_controller.py
git commit -m "arm_control: tune gripper open/close angles"

# Push your branch to GitHub
git push -u origin oren/add-gripper-tuning
```

Then go to the GitHub repo in a browser — there'll be a **"Compare & pull request"** button. Click it, write a short description of what you changed and why, and request a teammate as reviewer. They'll review, maybe request changes, and eventually merge your branch into `main`.

### After your PR is merged

```powershell
git checkout main
git pull
git branch -d oren/add-gripper-tuning   # delete the local branch
```

Your branch is already deleted from GitHub (merge usually removes it automatically).

### Merge conflicts — don't panic

If two people edit the same file in different ways, Git can't always figure out how to combine them. You'll see a conflict when you try to merge or pull. The fix:

1. Open the affected file. You'll see Git's conflict markers (`<<<<<<<`, `=======`, `>>>>>>>`).
2. Decide what the final code should be. Keep the parts you want, delete the markers.
3. Save, `git add <file>`, `git commit`.

VS Code has a built-in merge conflict resolver that makes this much easier — it shows both versions with "Accept current," "Accept incoming," and "Accept both" buttons.

If you're stuck, ask before experimenting — it's easy to make a conflict worse.

### Commit message conventions for this project

Per the root `README.md`:

```
arm_control: add gripper open/close helpers
vision: switch to YOLOv8n, update training config
nlp: add 'status' command handler
docs: draft calibration procedure
```

Prefix with the area you touched, then a short imperative description ("add," "fix," "update" — not "added," "fixing").

---

## 11. Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| `python: command not found` (Windows) | Python not on PATH | Reinstall Python and check "Add to PATH" during install; or use `py` instead of `python` |
| PowerShell error when activating venv: *"running scripts is disabled"* | PowerShell execution policy too strict | `Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned`, then try again |
| `(.venv)` doesn't appear in VS Code terminal | Wrong interpreter selected | `Ctrl+Shift+P` → "Python: Select Interpreter" → pick the `.venv` one |
| `ModuleNotFoundError` for a package that's in `requirements.txt` | Installed into system Python, not the venv | Confirm venv is active (`(.venv)` in prompt), then `pip install -r requirements.txt` again |
| `pip install` is very slow or hangs on torch/ultralytics | Normal — those packages are hundreds of MB | Wait; use a wired connection if possible |
| `Arm_Lib not found` warning | Expected on any non-Jetson machine | No action needed — dry-run mode is intentional for laptops |
| Git push rejected: *"Updates were rejected"* | Remote has commits you don't have locally | `git pull --rebase`, resolve any conflicts, then `git push` |
| Accidentally committed a huge file (.pt, .onnx, video) | Missing `.gitignore` entry | Don't push yet. `git reset HEAD~1` to undo the commit, add the pattern to `.gitignore`, re-commit, then push |

---

## When to rebuild the venv from scratch

Sometimes things break in strange ways and starting clean is faster than debugging. It's safe — you can always recreate a venv from `requirements.txt`.

```powershell
# Make sure the venv isn't active
deactivate

# Delete it
Remove-Item -Recurse -Force .venv      # Windows PowerShell
# rm -rf .venv                          # macOS / Linux

# Recreate and reinstall
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r requirements.txt
```

The `.venv` folder is just a cache of installed packages — deleting it loses no work. Nothing in the venv should ever be committed to git anyway.

---

*Questions or corrections? Open an issue in the repo or post in the team chat.*
