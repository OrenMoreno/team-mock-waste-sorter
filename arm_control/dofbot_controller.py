"""
DOFBOT arm controller - wraps Yahboom servo library into 
high-level movement functions.

Designed to run on the Jetson Nano with I2C connected.
"""
import time
import sys

# When running on the Jetson, the Arm_Lib module will be available.
# On your laptop, this import will fail - that's expected.
try:
    from Arm_Lib import Arm_Device
    ARM_AVAILABLE = True
except ImportError:
    ARM_AVAILABLE = False
    print("[WARN] Arm_Lib not found - running in DRY RUN mode")


class DofbotController:
    """High-level controller for the Yahboom DOFBOT arm."""

    # Servo IDs
    BASE = 1
    SHOULDER = 2
    ELBOW = 3
    WRIST_TILT = 4
    WRIST_ROTATE = 5
    GRIPPER = 6

    # Safe default positions (home pose - arm upright and centered)
    HOME_POSE = {1: 90, 2: 90, 3: 90, 4: 90, 5: 90, 6: 90}

    # Gripper constants (tune these on the real hardware)
    GRIPPER_OPEN = 60
    GRIPPER_CLOSED = 150

    # Default movement speed (milliseconds for servo travel)
    DEFAULT_SPEED = 500

    def __init__(self):
        if ARM_AVAILABLE:
            self.arm = Arm_Device()
            time.sleep(0.5)  # Let I2C settle
        else:
            self.arm = None

    def move_servo(self, servo_id, angle, speed_ms=None):
        """Move a single servo to the given angle."""
        if speed_ms is None:
            speed_ms = self.DEFAULT_SPEED
        angle = max(0, min(180, int(angle)))  # Clamp to safe range
        print(f"  Servo {servo_id} -> {angle}° ({speed_ms}ms)")
        if self.arm:
            self.arm.Arm_serial_servo_write(servo_id, angle, speed_ms)
            time.sleep(speed_ms / 1000.0 + 0.1)  # Wait for motion

    def move_all(self, angles_dict, speed_ms=None):
        """Move multiple servos simultaneously.
        angles_dict: {servo_id: angle, ...}
        """
        if speed_ms is None:
            speed_ms = self.DEFAULT_SPEED
        for sid, angle in angles_dict.items():
            angle = max(0, min(180, int(angle)))
            print(f"  Servo {sid} -> {angle}°")
            if self.arm:
                self.arm.Arm_serial_servo_write(sid, angle, speed_ms)
        time.sleep(speed_ms / 1000.0 + 0.2)

    def go_home(self):
        """Return all servos to the home position."""
        print("[HOME] Moving to home position...")
        self.move_all(self.HOME_POSE, speed_ms=800)

    def open_gripper(self):
        """Open the gripper."""
        print("[GRIP] Opening gripper")
        self.move_servo(self.GRIPPER, self.GRIPPER_OPEN, 400)

    def close_gripper(self):
        """Close the gripper."""
        print("[GRIP] Closing gripper")
        self.move_servo(self.GRIPPER, self.GRIPPER_CLOSED, 400)

    def rotate_base_to(self, angle):
        """Rotate the base to face a direction (0-180)."""
        print(f"[BASE] Rotating to {angle}°")
        self.move_servo(self.BASE, angle)

    def extend_arm_to(self, shoulder_angle, elbow_angle):
        """Extend the arm outward by adjusting shoulder and elbow."""
        print(f"[EXTEND] Shoulder={shoulder_angle}°, Elbow={elbow_angle}°")
        self.move_servo(self.SHOULDER, shoulder_angle)
        self.move_servo(self.ELBOW, elbow_angle)

    def reach_position(self, base_angle, shoulder_angle, 
                       elbow_angle, wrist_angle=90):
        """Move the arm to reach a specific workspace position.
        This is a simple joint-space approach - you give it the 
        angles directly. Later, you can add inverse kinematics.
        """
        print(f"[REACH] base={base_angle}, shoulder={shoulder_angle}, "
              f"elbow={elbow_angle}, wrist={wrist_angle}")
        pose = {
            self.BASE: base_angle,
            self.SHOULDER: shoulder_angle,
            self.ELBOW: elbow_angle,
            self.WRIST_TILT: wrist_angle,
            self.WRIST_ROTATE: 90,  # Keep wrist rotation neutral
        }
        self.move_all(pose)

    def pick_and_place(self, pick_pose, drop_pose):
        """Full pick-and-place sequence.
        pick_pose: dict of {servo_id: angle} for the pick location
        drop_pose: dict of {servo_id: angle} for the drop location
        """
        print("=== PICK AND PLACE ===")
        
        # 1. Go home first
        self.go_home()
        time.sleep(0.5)
        
        # 2. Open gripper
        self.open_gripper()
        
        # 3. Move to hover above pick position (raise shoulder a bit)
        hover = dict(pick_pose)
        hover[self.SHOULDER] = pick_pose.get(self.SHOULDER, 90) - 15
        self.move_all(hover)
        time.sleep(0.3)
        
        # 4. Lower to pick position
        self.move_all(pick_pose)
        time.sleep(0.3)
        
        # 5. Close gripper
        self.close_gripper()
        time.sleep(0.3)
        
        # 6. Lift (back to hover)
        self.move_all(hover)
        time.sleep(0.3)
        
        # 7. Move to drop position
        self.move_all(drop_pose)
        time.sleep(0.3)
        
        # 8. Open gripper
        self.open_gripper()
        time.sleep(0.3)
        
        # 9. Return home
        self.go_home()
        print("=== DONE ===")


if __name__ == "__main__":
    ctrl = DofbotController()
    ctrl.go_home()
    print("Controller initialized. Run keyboard_teleop.py to drive.")