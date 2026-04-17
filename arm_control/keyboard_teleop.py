#!/usr/bin/env python3
"""
Keyboard teleoperation for DOFBOT.
Run this over SSH on the Jetson to manually control each joint.
Also runs on Windows for dry-run testing (without Arm_Lib).

Controls:
  q/a  - Base rotate left/right
  w/s  - Shoulder up/down
  e/d  - Elbow up/down
  r/f  - Wrist tilt up/down
  t/g  - Wrist rotate left/right
  o    - Open gripper
  c    - Close gripper
  h    - Go to home position
  p    - Print current angles
  x    - Exit
"""
import sys
from dofbot_controller import DofbotController


# Cross-platform single-keypress reader
try:
    # Windows
    import msvcrt
    def get_key():
        ch = msvcrt.getch()
        try:
            return ch.decode('utf-8', errors='ignore')
        except Exception:
            return ''
except ImportError:
    # Unix (Jetson / Linux / macOS)
    import tty
    import termios
    def get_key():
        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)
        return ch


STEP = 5  # Degrees per keypress


def main():
    ctrl = DofbotController()

    # Track current angles (start at home)
    angles = dict(ctrl.HOME_POSE)
    ctrl.go_home()

    print("\n=== DOFBOT Keyboard Teleop ===")
    print("q/a=base  w/s=shoulder  e/d=elbow  r/f=wrist tilt  t/g=wrist rotate")
    print("o=open gripper  c=close gripper  h=home  p=print angles  x=exit\n")

    key_map = {
        'q': (ctrl.BASE,         +STEP),
        'a': (ctrl.BASE,         -STEP),
        'w': (ctrl.SHOULDER,     +STEP),
        's': (ctrl.SHOULDER,     -STEP),
        'e': (ctrl.ELBOW,        +STEP),
        'd': (ctrl.ELBOW,        -STEP),
        'r': (ctrl.WRIST_TILT,   +STEP),
        'f': (ctrl.WRIST_TILT,   -STEP),
        't': (ctrl.WRIST_ROTATE, +STEP),
        'g': (ctrl.WRIST_ROTATE, -STEP),
    }

    while True:
        key = get_key()

        # Handle Ctrl+C cleanly on Windows (msvcrt returns '\x03')
        if key == '\x03':
            print("\nCtrl+C detected. Sending arm home...")
            ctrl.go_home()
            break

        if key == 'x':
            print("\nExiting. Sending arm home...")
            ctrl.go_home()
            break
        elif key == 'h':
            angles = dict(ctrl.HOME_POSE)
            ctrl.go_home()
        elif key == 'o':
            ctrl.open_gripper()
            angles[ctrl.GRIPPER] = ctrl.GRIPPER_OPEN
        elif key == 'c':
            ctrl.close_gripper()
            angles[ctrl.GRIPPER] = ctrl.GRIPPER_CLOSED
        elif key == 'p':
            print(f"\nCurrent angles: {angles}\n")
        elif key in key_map:
            servo_id, delta = key_map[key]
            angles[servo_id] = max(0, min(180, angles[servo_id] + delta))
            ctrl.move_servo(servo_id, angles[servo_id], speed_ms=200)
        else:
            # Unknown key - ignore silently
            pass


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nInterrupted. Sending arm home...")
        try:
            DofbotController().go_home()
        except Exception:
            pass