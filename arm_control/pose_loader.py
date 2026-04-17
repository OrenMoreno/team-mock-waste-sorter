#!/usr/bin/env python3
"""Load and execute named poses from poses.yaml."""
import yaml
import sys
from dofbot_controller import DofbotController


def load_poses(yaml_path="poses.yaml"):
    with open(yaml_path, 'r') as f:
        return yaml.safe_load(f)


def main():
    if len(sys.argv) < 2:
        poses = load_poses()
        print("Available poses:", list(poses.keys()))
        print("Usage: python3 pose_loader.py <pose_name>")
        return

    pose_name = sys.argv[1]
    poses = load_poses()
    
    if pose_name not in poses:
        print(f"Unknown pose: {pose_name}")
        print("Available:", list(poses.keys()))
        return

    ctrl = DofbotController()
    print(f"Moving to pose: {pose_name}")
    ctrl.move_all(poses[pose_name], speed_ms=800)


if __name__ == "__main__":
    main()