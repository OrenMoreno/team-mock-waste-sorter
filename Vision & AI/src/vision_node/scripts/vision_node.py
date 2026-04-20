#!/usr/bin/env python3

import rospy
import json
import onnxruntime as ort
from sensor_msgs.msg import Image
from std_msgs.msg import String
from vision_node.msg import DetectionResult
import numpy as np
import cv2

class VisionNode:
    def __init__(self):
        # ROS Parameters
        self.confidence_threshold = rospy.get_param('~confidence_threshold', 0.65)
        self.model_path = rospy.get_param('~model_path', 'model.onnx')
        self.input_width = rospy.get_param('~input_width', 640)
        self.input_height = rospy.get_param('~input_height', 640)

        # ONNX Runtime session
        self.session = ort.InferenceSession(self.model_path)

        # ROS Publishers
        self.detection_pub = rospy.Publisher('/detections', DetectionResult, queue_size=10)
        self.status_pub = rospy.Publisher('/vision_node/status', String, queue_size=1)

        # ROS Subscriber
        self.image_sub = rospy.Subscriber('/usb_cam/image_raw', Image, self.image_callback, queue_size=1, buff_size=2**24)

        # Status variables
        self.frames_processed = 0
        self.last_class = "none"
        self.last_confidence = 0.0

        # Timer for status publishing
        rospy.Timer(rospy.Duration(1), self.publish_status)

    def preprocess_image(self, ros_image):
        # Convert ROS Image to OpenCV format
        np_arr = np.frombuffer(ros_image.data, dtype=np.uint8)
        image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        
        # Resize and normalize
        resized = cv2.resize(image, (self.input_width, self.input_height))
        normalized = resized / 255.0
        transposed = np.transpose(normalized, (2, 0, 1))  # HWC to CHW
        return np.expand_dims(transposed, axis=0).astype(np.float32)

    def image_callback(self, ros_image):
        try:
            input_tensor = self.preprocess_image(ros_image)
            outputs = self.session.run(None, {self.session.get_inputs()[0].name: input_tensor})

            # Parse outputs (assuming YOLOv8n format)
            detections = outputs[0]
            best_detection = None

            for detection in detections:
                _, x, y, w, h, conf, cls = detection
                if conf > self.confidence_threshold:
                    if best_detection is None or conf > best_detection['confidence']:
                        best_detection = {
                            'object_class': str(int(cls)),
                            'confidence': conf,
                            'bbox_center_x_px': x,
                            'bbox_center_y_px': y,
                            'bbox_width_px': w,
                            'bbox_height_px': h
                        }

            if best_detection:
                self.publish_detection(best_detection)
            else:
                self.publish_none_detection()

            self.frames_processed += 1

        except Exception as e:
            rospy.logerr(f"Error processing image: {e}")

    def publish_detection(self, detection):
        msg = DetectionResult()
        msg.header.stamp = rospy.Time.now()
        msg.header.frame_id = "camera"
        msg.object_class = detection['object_class']
        msg.confidence = detection['confidence']
        msg.bbox_center_x_px = detection['bbox_center_x_px']
        msg.bbox_center_y_px = detection['bbox_center_y_px']
        msg.bbox_width_px = detection['bbox_width_px']
        msg.bbox_height_px = detection['bbox_height_px']
        self.detection_pub.publish(msg)

        self.last_class = detection['object_class']
        self.last_confidence = detection['confidence']

    def publish_none_detection(self):
        msg = DetectionResult()
        msg.header.stamp = rospy.Time.now()
        msg.header.frame_id = "camera"
        msg.object_class = "none"
        msg.confidence = 0.0
        msg.bbox_center_x_px = 0.0
        msg.bbox_center_y_px = 0.0
        msg.bbox_width_px = 0.0
        msg.bbox_height_px = 0.0
        self.detection_pub.publish(msg)

        self.last_class = "none"
        self.last_confidence = 0.0

    def publish_status(self, event):
        status = {
            "state": "running",
            "fps": self.frames_processed,
            "last_class": self.last_class,
            "last_confidence": self.last_confidence,
            "frames_processed": self.frames_processed
        }
        self.status_pub.publish(json.dumps(status))

if __name__ == '__main__':
    rospy.init_node('vision_node', anonymous=False)
    node = VisionNode()
    rospy.spin()