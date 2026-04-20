# Model Selection Rationale
**Document:** `/docs/model_selection.md`
**Role:** Vision & AI Developer | **Milestone 1** | ITAI 4376 – Spring 2026

---

## 1. Objective

Select an object detection model that (a) accurately identifies at least four waste categories — plastic bottle, aluminum can, cardboard, and paper — and (b) runs at **≥ 5 fps in real-time on an NVIDIA Jetson Nano** without requiring an auxiliary GPU. This document records the evaluation, ruling-out rationale, and final selection.

---

## 2. Hardware Constraint: The Jetson Nano Ceiling

The NVIDIA Jetson Nano (4 GB variant) provides **472 GFLOPS** of compute via its 128-core Maxwell GPU. Real-time inference at ≥ 5 fps on a 640 × 640 input frame leaves a hard budget of roughly **200 ms per frame**, including image pre-processing, inference, and post-processing (NMS).

Empirical benchmarks and the Ultralytics deployment guide consistently show that models exceeding approximately **5 million parameters** exceed this budget at full resolution under TensorRT FP16 optimisation. Models above this threshold either:
- Drop below 5 fps even with TensorRT acceleration, or
- Require resolution reduction severe enough (< 320 × 320) to degrade detection accuracy on small objects such as crumpled paper balls.

**Therefore, any model with > 5 M parameters is ruled out for this project.**

This explicitly excludes: YOLOv5s (7.2 M), YOLOv5m (21.2 M), YOLOv8s (11.2 M), YOLOv8m (25.9 M), all YOLOv8l/x variants, EfficientDet-D1 and above, and any two-stage detector (Faster R-CNN, Mask R-CNN).

---

## 3. Candidate Models

| Model | Parameters | Jetson Nano fps (FP16, est.) | mAP@0.5 (COCO) | ONNX Export | Notes |
|---|---|---|---|---|---|
| **YOLOv5n** | 1.9 M | ~10–14 fps | 28.0 | ✅ | Smallest YOLO; faster but less accurate |
| **YOLOv8n** | 3.2 M | ~8–12 fps | 37.3 | ✅ | Higher accuracy at similar speed; recommended |
| YOLOv5s | 7.2 M | ~4–6 fps | 37.4 | ✅ | **Ruled out** — exceeds 5 M parameter budget |
| YOLOv8s | 11.2 M | ~3–5 fps | 44.9 | ✅ | **Ruled out** — exceeds 5 M parameter budget |
| MobileNet-SSD v2 | 4.3 M | ~8 fps | ~22 | ✅ | Lower accuracy; lacks strong community waste-class support |
| EfficientDet-D0 | 3.9 M | ~5–6 fps | 34.6 | ⚠️ | Borderline fps; complex anchor config; not recommended |

*fps estimates are for 640×640 input, Jetson Nano 4 GB, TensorRT FP16 engine. Sources: Ultralytics benchmarks, JetsonHacks community tests.*

---

## 4. Head-to-Head: YOLOv5n vs YOLOv8n

### Accuracy
YOLOv8n achieves a COCO mAP@0.5 of **37.3** vs YOLOv5n's **28.0** — a 9.3-point improvement in baseline accuracy before any fine-tuning. For a waste-sorting application with visually similar categories (e.g., white plastic vs. white paper), this margin is meaningful and reduces the risk of falling below the project's 80% accuracy target.

### Speed on Jetson Nano
Both models comfortably meet the ≥ 5 fps threshold. YOLOv8n is slightly slower than YOLOv5n due to its additional parameters, but the gap narrows under TensorRT optimisation and is not a practical concern at our operating resolution.

### Training Ecosystem
YOLOv8 is actively maintained by Ultralytics and offers a clean Python API (`from ultralytics import YOLO`), native Roboflow integration, and first-class ONNX/TensorRT export — all required for our deployment pipeline. YOLOv5 remains stable but is in maintenance mode; new features and bug fixes are directed at YOLOv8.

### Deployment Path
Both models export to ONNX via a single command. YOLOv8's export pipeline has been validated against `trtexec` for TensorRT engine generation on JetPack 4.6.x, which matches our Jetson Nano environment.

---

## 5. Decision

**Selected model: YOLOv8n (nano variant)**

Rationale summary: YOLOv8n delivers significantly higher baseline mAP than YOLOv5n, comfortably clears the Jetson Nano real-time threshold, fits within the 5 M parameter hard limit (3.2 M params), and has the most actively maintained training/export toolchain. It is the lowest-risk choice for meeting the project's 80% classification accuracy target.

YOLOv5n is retained as a **fallback option** in case Jetson performance is lower than estimated in practice; a YOLOv5n checkpoint can be trained in parallel during Milestone 2 with minimal additional effort.

---

## 6. Ruled-Out Models Summary

| Model | Reason for Exclusion |
|---|---|
| YOLOv5s (7.2 M) | Exceeds 5 M parameter budget; fps borderline on Nano |
| YOLOv8s (11.2 M) | Exceeds 5 M parameter budget; insufficient fps at 640×640 |
| YOLOv8m/l/x | Far exceed parameter and compute budget |
| EfficientDet-D1+ | Exceeds parameter budget |
| Faster R-CNN | Two-stage detector; too slow for real-time on Nano |
| DETR / RT-DETR | Transformer architectures; memory and compute far exceed Nano budget |

---

*Author: Vision & AI Developer | Date: Week 1 | Review: NLP & Integration Developer*
