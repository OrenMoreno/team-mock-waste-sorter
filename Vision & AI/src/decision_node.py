#!/usr/bin/env python3

import rospy
from vision_node.msg import DetectionResult
from std_msgs.msg import String

class DecisionNode:
    def __init__(self):
        # ROS Subscriber
        self.detection_sub = rospy.Subscriber('/detections', DetectionResult, self.detection_callback, queue_size=1)

        # ROS Publisher
        self.arm_status_pub = rospy.Publisher('/arm_status', String, queue_size=10)

        # Timeout for no detection
        self.last_detection_time = rospy.Time.now()
        self.timeout_duration = rospy.Duration(3)  # 3 seconds

        # Timer to check for idle state
        rospy.Timer(rospy.Duration(0.5), self.check_idle_state)

    def detection_callback(self, msg):
        if msg.object_class == "none" or msg.confidence < 0.65:
            rospy.loginfo("No valid detection received.")
            return

        # Process valid detection
        rospy.loginfo(f"Processing detection: {msg.object_class} at ({msg.bbox_center_x_px}, {msg.bbox_center_y_px})")
        self.last_detection_time = rospy.Time.now()

        # Example: Publish pick coordinates to arm control (not implemented here)
        # self.arm_control_pub.publish(...)

    def check_idle_state(self, event):
        if rospy.Time.now() - self.last_detection_time > self.timeout_duration:
            rospy.loginfo("No detection within timeout. Publishing idle state.")
            self.arm_status_pub.publish("idle")

if __name__ == '__main__':
    rospy.init_node('decision_node', anonymous=False)
    node = DecisionNode()
    rospy.spin()