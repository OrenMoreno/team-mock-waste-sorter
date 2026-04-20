# AI-Powered Robotic Waste Sorting System
**ITAI 4376 · Spring 2026 · Team MOCK**
Kaylee Auguillard · Oren Moreno · Cheyenne Hathaway · Maria Tanweer Chachar

---

## Project Overview

This repository contains the full implementation for our AI-Powered Robotic Waste Sorting System capstone project. The system uses a YOLOv8n computer vision model to detect and classify waste items, which are then sorted by a DOFBOT robotic arm controlled via ROS on a Jetson Nano.

---



## Repository Structure

```
waste-sorting-robot/
├── dataset/                        # Training dataset (not pushed to Git — see below)
│   ├── train/
│   ├── valid/
│   ├── test/
│   └── data.yaml
├── models/
│   ├── yolov8n_waste_v3.pt         # Final trained PyTorch weights
│   └── yolov8n_waste_v3.onnx       # ONNX export for Jetson Nano deployment
├── runs/                           # YOLOv8 training outputs (auto-generated)
├── src/
│   └── vision_node/                # ROS package for object detection
│       ├── msg/
│       │   └── DetectionResult.msg # Custom ROS message definition
│       ├── scripts/
│       │   └── vision_node.py      # Main ROS vision node
│       ├── package.xml
│       └── CMakeLists.txt
├── docs/
│   ├── model_selection.md          # YOLOv8n vs YOLOv5n rationale
│   ├── dataset_survey.md           # Dataset sources and strategy
│   ├── vision_node_spec.md         # ROS interface specification
│   └── ml_environment_setup.md     # Environment setup guide
├── check_labels.py                 # Utility: verify label class distribution
├── remap_labels.py                 # Utility: remap dataset labels to 4 classes
└── test_webcam.py                  # Utility: test model on webcam
```

---

## Model Performance (Milestone 2 Results)

Trained on ~9,000 images from the Roboflow waste detection dataset. Labels remapped from 22 original classes to 4:

| Class | mAP50 | Precision | Recall |
|---|---|---|---|
| **Overall** | **94.1%** | 93.4% | 90.1% |
| plastic | 90.3% | 92.8% | 82.3% |
| metal_can | 95.0% | 90.5% | 94.0% |
| paper_cardboard | 92.1% | 93.2% | 85.9% |
| other | 99.1% | 97.1% | 98.2% |

> ✅ Exceeds the project's 80% mAP50 requirement.
> Inference speed: ~3.1ms per image on RTX 3060.

---

## Setup Instructions

### Prerequisites
- Python 3.10 or 3.11 recommended (3.13 works but has some limitations)
- NVIDIA GPU with CUDA 11.8+ recommended for training
- Windows 10/11 or Ubuntu 20.04/22.04

### 1 — Clone the Repository
```bash
git clone <your-repo-url>
cd waste-sorting-robot
```

### 2 — Install Dependencies
```bash
pip install ultralytics torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
pip install opencv-python onnx onnxruntime numpy
```

> For CPU only (no NVIDIA GPU), replace the PyTorch install URL with:
> `https://download.pytorch.org/whl/cpu`

### 3 — Verify GPU Is Detected
```bash
python -c "import torch; print('CUDA:', torch.cuda.is_available()); print('GPU:', torch.cuda.get_device_name(0))"
```

---

## Running the Webcam Test (Windows)

Test the trained model on your local webcam:
```bash
python -c "from ultralytics import YOLO; YOLO('models/yolov8n_waste_v3.pt').predict(source=0, show=True, conf=0.65)"
```
Press `Q` to quit.

---

## Dataset Setup (Oren / Maria)

The dataset is not pushed to Git due to its size (~1 GB). To recreate it:

1. Download the **Waste Detection** dataset from Roboflow in **YOLOv8 format**:
   - URL: https://universe.roboflow.com/ai-project-i3wje/waste-detection-vqkjo/dataset/10
2. Unzip it into the `dataset/` folder
3. Replace `dataset/data.yaml` with the following:
```yaml
path: <absolute path to your waste-sorting-robot/dataset folder>
train: train/images
val: valid/images
test: test/images

nc: 4
names: ['plastic', 'metal_can', 'paper_cardboard', 'other']
```
4. Run the label remapping script:
```bash
python remap_labels.py
```
5. Verify labels are correct:
```bash
python check_labels.py
```
You should see only classes 0–3.

---

## Retraining the Model

```bash
python -c "from ultralytics import YOLO; model = YOLO('yolov8n.pt'); model.train(data='dataset/data.yaml', epochs=100, imgsz=640, batch=16, name='waste_v3', patience=20, cache=True)"
```

Best weights will be saved to `runs/detect/waste_v3/weights/best.pt`. Copy to models folder:
```bash
# Windows
copy runs\detect\waste_v3\weights\best.pt models\yolov8n_waste_v3.pt

# Linux/Mac
cp runs/detect/waste_v3/weights/best.pt models/yolov8n_waste_v3.pt
```

---

## Exporting to ONNX (For Jetson Nano)

```bash
python -c "from ultralytics import YOLO; YOLO('models/yolov8n_waste_v3.pt').export(format='onnx', imgsz=640)"
```

Output: `models/yolov8n_waste_v3.onnx` — copy this file to the Jetson Nano via `scp`.

---

## ROS Vision Node (Jetson Nano)

### Topics

| Direction | Topic | Message Type | Description |
|---|---|---|---|
| Subscribes | `/usb_cam/image_raw` | `sensor_msgs/Image` | Raw camera frames |
| Publishes | `/detections` | `vision_node/DetectionResult` | Detection results |
| Publishes | `/vision_node/status` | `std_msgs/String` | Node status JSON |

### DetectionResult Message Fields

| Field | Type | Description |
|---|---|---|
| `object_class` | string | `plastic`, `metal_can`, `paper_cardboard`, `other`, or `none` |
| `confidence` | float32 | Detection confidence 0.0–1.0 |
| `bbox_center_x_px` | float32 | Bounding box center X in pixels |
| `bbox_center_y_px` | float32 | Bounding box center Y in pixels |
| `bbox_width_px` | float32 | Bounding box width in pixels |
| `bbox_height_px` | float32 | Bounding box height in pixels |

### ROS Parameters

| Parameter | Default | Description |
|---|---|---|
| `~confidence_threshold` | `0.65` | Minimum confidence to publish a detection |
| `~model_path` | `yolov8n_waste_v3.onnx` | Path to ONNX model |
| `~input_width` | `640` | Model input width |
| `~input_height` | `640` | Model input height |
| `~camera_topic` | `/usb_cam/image_raw` | Camera topic to subscribe to |

### Build and Run (on Jetson Nano)

```bash
cd ~/catkin_ws
catkin_make
source devel/setup.bash
rosrun vision_node vision_node.py
```

---

## Documentation

| File | Description |
|---|---|
| `docs/model_selection.md` | YOLOv8n vs YOLOv5n evaluation and selection rationale |
| `docs/dataset_survey.md` | Dataset sources, remapping strategy, augmentation plan |
| `docs/vision_node_spec.md` | Full ROS interface spec for Maria's integration work |
| `docs/ml_environment_setup.md` | Step-by-step environment setup guide |

---

## Team Role Contacts

| Role | Owner | Responsibilities |
|---|---|---|
| Vision & AI Developer | Kaylee Auguillard | Model training, vision node, ONNX export |
| Hardware & Robotics Lead | Oren Moreno | Jetson Nano, DOFBOT arm, calibration |
| NLP & Integration Developer | Maria Tanweer Chachar | ROS architecture, decision node, NLP |
| QA & Documentation Lead | Cheyenne Hathaway | Test plan, reports, presentation |