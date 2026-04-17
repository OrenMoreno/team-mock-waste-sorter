#!/usr/bin/env python3
"""
Convert pixel coordinates from camera to arm joint angles.
Uses a simple proportional mapping instead of full calibration.

Assumptions (update these based on your actual setup):
- Camera is mounted on the arm or directly above the workspace
- Camera resolution is 640x480
- The workspace maps roughly to base angles 45-135 degrees
  (left edge of frame = 45°, right edge = 135°)
"""
from dofbot_controller import DofbotController

# Camera resolution (update to match your camera)
CAM_WIDTH = 640
CAM_HEIGHT = 480

# Mapping: pixel X -> base rotation angle
# Left edge of camera (x=0) maps to BASE_MIN
# Right edge (x=640) maps to BASE_MAX
# NOTE: you may need to flip these depending on camera orientation
BASE_MIN = 45
BASE_MAX = 135

# Mapping: pixel Y -> arm extension
# Objects near the top of the frame are far away -> extend more
# Objects near the bottom are close -> extend less
# These are (shoulder_angle, elbow_angle) pairs
EXTEND_NEAR = (70, 70)   # Object close (bottom of frame)
EXTEND_FAR = (45, 30)    # Object far (top of frame)


def pixel_to_base_angle(px_x):
    """Convert pixel X coordinate to base rotation angle."""
    ratio = px_x / CAM_WIDTH
    angle = BASE_MIN + ratio * (BASE_MAX - BASE_MIN)
    return max(BASE_MIN, min(BASE_MAX, angle))


def pixel_to_extension(px_y):
    """Convert pixel Y coordinate to shoulder and elbow angles.
    Lower Y (top of frame) = farther = more extension.
    """
    ratio = px_y / CAM_HEIGHT  # 0 = top (far), 1 = bottom (near)
    shoulder = EXTEND_FAR[0] + ratio * (EXTEND_NEAR[0] - EXTEND_FAR[0])
    elbow = EXTEND_FAR[1] + ratio * (EXTEND_NEAR[1] - EXTEND_FAR[1])
    return shoulder, elbow


def point_at_target(ctrl, px_x, px_y):
    """Rotate and extend the arm toward a target at pixel (x, y)."""
    base = pixel_to_base_angle(px_x)
    shoulder, elbow = pixel_to_extension(px_y)
    
    print(f"[TARGET] Pixel ({px_x}, {px_y}) -> "
          f"base={base:.0f}°, shoulder={shoulder:.0f}°, elbow={elbow:.0f}°")
    
    ctrl.reach_position(
        base_angle=base,
        shoulder_angle=shoulder,
        elbow_angle=elbow,
        wrist_angle=90
    )


def demo():
    """Test with hardcoded pixel positions."""
    ctrl = DofbotController()
    ctrl.go_home()
    
    test_points = [
        (320, 240, "Center of frame"),
        (100, 100, "Top-left (far left)"),
        (540, 400, "Bottom-right (near right)"),
        (320, 50,  "Top-center (far ahead)"),
    ]
    
    for px_x, px_y, desc in test_points:
        print(f"\n--- Pointing at: {desc} ---")
        point_at_target(ctrl, px_x, px_y)
        input("Press Enter to continue...")
    
    ctrl.go_home()


if __name__ == "__main__":
    demo()