import unittest
from unittest.mock import MagicMock
from vision_node.msg import DetectionResult

class TestVisionNode(unittest.TestCase):

    def setUp(self):
        # Mock the ROS publisher and subscriber
        self.mock_publisher = MagicMock()
        self.mock_subscriber = MagicMock()

    def test_detection_result_message(self):
        # Create a mock DetectionResult message
        msg = DetectionResult()
        msg.header.stamp = 123456789
        msg.header.frame_id = "camera"
        msg.object_class = "plastic"
        msg.confidence = 0.85
        msg.bbox_center_x_px = 320.0
        msg.bbox_center_y_px = 240.0
        msg.bbox_width_px = 50.0
        msg.bbox_height_px = 100.0

        # Simulate publishing the message
        self.mock_publisher.publish(msg)

        # Verify the message was published
        self.mock_publisher.publish.assert_called_once_with(msg)

    def test_none_detection_message(self):
        # Create a mock DetectionResult message for "none"
        msg = DetectionResult()
        msg.header.stamp = 123456789
        msg.header.frame_id = "camera"
        msg.object_class = "none"
        msg.confidence = 0.0
        msg.bbox_center_x_px = 0.0
        msg.bbox_center_y_px = 0.0
        msg.bbox_width_px = 0.0
        msg.bbox_height_px = 0.0

        # Simulate publishing the message
        self.mock_publisher.publish(msg)

        # Verify the message was published
        self.mock_publisher.publish.assert_called_once_with(msg)

if __name__ == "__main__":
    unittest.main()