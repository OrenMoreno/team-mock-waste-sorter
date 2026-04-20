# vision_node/DetectionResult
# Published on: /detections
# Author: Vision & AI Developer
# Last updated: Week 1

# Header for timestamp and frame_id (for bag recording and debugging)
std_msgs/Header header

# Detected object class label.
# Valid values: "plastic", "metal_can", "paper_cardboard", "other", "none"
# "none" is published when no object is detected above the confidence threshold.
string object_class

# Detection confidence score in range [0.0, 1.0].
# Values below the threshold (default 0.65) are NOT published as normal detections;
# a "none" message is sent instead. This field is 0.0 when object_class is "none".
float32 confidence

# Bounding box center in pixel coordinates (u = horizontal, v = vertical).
# Origin is top-left corner of the image frame.
# Both values are 0.0 when object_class is "none".
float32 bbox_center_x_px
float32 bbox_center_y_px

# Bounding box dimensions in pixels (width and height).
# Provided for downstream use (e.g., size-based filtering). Both 0.0 when no detection.
float32 bbox_width_px
float32 bbox_height_px