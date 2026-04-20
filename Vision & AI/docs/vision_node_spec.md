# Vision Node Interface Specification
**Document:** `/docs/vision_node_spec.md`
**Role:** Vision & AI Developer | **Milestone 1** | ITAI 4376 – Spring 2026
**Audience:** NLP & Software Integration Developer, Hardware Lead

---

## 1. Purpose

This document defines the ROS interface contract for the `vision_node`. It specifies the topics the node subscribes to, the topic it publishes on, the message format, and the behavioral guarantees the rest of the system can rely on. Any developer building nodes downstream of `vision_node` (particularly `decision_node`) should treat this document as the authoritative interface reference.

---

## 2. Node Identity

| Field | Value |
|---|---|
| ROS package name | `vision_node` |
| Node name | `/vision_node` |
| Language | Python 3 |
| Location | `~/catkin_ws/src/vision_node/` |

---

## 3. Subscribed Topics

| Topic | Message Type | Description |
|---|---|---|
| `/usb_cam/image_raw` | `sensor_msgs/Image` | Raw camera frames from the USB camera. The actual topic name may differ depending on the driver; the final confirmed name will be documented by the Hardware Lead and updated here. |

The node processes every incoming frame. If inference cannot keep up with the camera publishing rate, it drops older frames rather than queuing them (non-blocking callback pattern).

---

## 4. Published Topics

### 4.1 Primary Output — `/detections`

**Message type:** `vision_node/DetectionResult` *(custom message — see Section 5)*

Published **once per inference pass** when at least one object is detected with confidence ≥ the configured threshold.

**Behavior when no object is detected:** The node publishes a message with `object_class = "none"` and `confidence = 0.0` every 1 second while the camera feed is active but no object is visible. This prevents the `decision_node` from hanging waiting for a message.

**Behavior when multiple objects are visible:** The node publishes the **highest-confidence detection only** per frame. Multi-object queuing is out of scope for v1 and will be revisited in Milestone 5 if time allows.

---

### 4.2 Diagnostic Topic — `/vision_node/status`

**Message type:** `std_msgs/String`

Published at **1 Hz**. Payload is a human-readable JSON string:

```json
{
  "state": "running",
  "fps": 8.3,
  "last_class": "plastic",
  "last_confidence": 0.91,
  "frames_processed": 1042
}
```

`state` values: `"running"`, `"idle"` (no camera feed), `"error"`.

---

## 5. Custom Message Definition — `DetectionResult`

**File location:** `~/catkin_ws/src/vision_node/msg/DetectionResult.msg`

```
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
```

### Field Definitions

| Field | Type | Unit | Notes |
|---|---|---|---|
| `header` | `std_msgs/Header` | — | Contains ROS timestamp (`stamp`) and `frame_id = "camera"` |
| `object_class` | `string` | — | One of: `"plastic"`, `"metal_can"`, `"paper_cardboard"`, `"other"`, `"none"` |
| `confidence` | `float32` | [0.0 – 1.0] | Raw model confidence. 0.0 if `object_class == "none"` |
| `bbox_center_x_px` | `float32` | pixels | Horizontal center of bounding box from left edge |
| `bbox_center_y_px` | `float32` | pixels | Vertical center of bounding box from top edge |
| `bbox_width_px` | `float32` | pixels | Width of bounding box |
| `bbox_height_px` | `float32` | pixels | Height of bounding box |

---

## 6. Configuration Parameters (ROS Params)

These values can be set in a launch file or YAML config. Defaults shown below.

| Parameter | Default | Description |
|---|---|---|
| `~confidence_threshold` | `0.65` | Detections below this score are treated as "none" |
| `~model_path` | `$(find vision_node)/models/yolov8n_waste.onnx` | Path to the ONNX model weights |
| `~input_width` | `640` | Model input resolution (width) |
| `~input_height` | `640` | Model input resolution (height) |
| `~camera_topic` | `/usb_cam/image_raw` | Camera topic to subscribe to |
| `~publish_rate_max` | `10` | Max detections published per second (caps GPU load) |

---

## 7. Example Message (rostopic echo)

```
header:
  seq: 1042
  stamp:
    secs: 1713200456
    nsecs: 382100000
  frame_id: "camera"
object_class: "plastic"
confidence: 0.912
bbox_center_x_px: 317.4
bbox_center_y_px: 228.1
bbox_width_px: 84.2
bbox_height_px: 210.5
```

---

## 8. Integration Notes for `decision_node`

The `decision_node` (owned by the NLP & Integration Developer) should:

1. Subscribe to `/detections` using a `rospy.Subscriber` with a queue size of 1 (always process the latest frame only).
2. Treat any message where `object_class == "none"` or `confidence < 0.65` as a no-detection event. The 0.65 threshold is enforced in `vision_node`, but `decision_node` should defensively re-check the confidence field.
3. Use `bbox_center_x_px` and `bbox_center_y_px` as the pixel-space pick coordinates to pass to the calibration transform and then to `arm_control_node`.
4. Implement a timeout: if no non-"none" message is received within **3 seconds**, publish `idle` to `/arm_status`.

---

## 9. Assumptions & Out of Scope for v1

- **Single-object detection only.** The node publishes the highest-confidence object per frame.
- **No tracking.** Object identity is not tracked across frames (no SORT/DeepSORT).
- **Fixed camera.** The calibration transform assumes the camera does not move between sessions.
- **No depth.** Only 2D pixel coordinates are published; Z-axis position is handled by fixed pick height in `arm_control_node`.

---

## 10. Version History

| Version | Date | Author | Notes |
|---|---|---|---|
| v0.1 | Week 1 | Vision & AI Developer | Initial draft for team review |

---

*For questions about this spec, contact the Vision & AI Developer. For questions about how `decision_node` consumes this interface, contact the NLP & Integration Developer.*
