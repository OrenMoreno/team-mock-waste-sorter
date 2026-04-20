# ML Environment Setup Guide
**Role:** Vision & AI Developer | **Milestone 1** | ITAI 4376 – Spring 2026

---

## Prerequisites

- OS: Ubuntu 20.04 / 22.04 (or Windows 10/11 with WSL2)
- GPU: NVIDIA GPU recommended (CUDA 11.8+); CPU-only path is included
- RAM: 8 GB minimum, 16 GB recommended for training

---

## Step 1 — Verify / Install Python 3.8+

```bash
python3 --version        # Confirm ≥ 3.8
# If not installed:
sudo apt update && sudo apt install -y python3 python3-pip python3-venv
```

Create and activate an isolated virtual environment (recommended to avoid package conflicts):

```bash
python3 -m venv ~/yolo-env
source ~/yolo-env/bin/activate
# To deactivate later: deactivate
```

---

## Step 2 — Install PyTorch

### Option A — With CUDA (NVIDIA GPU, recommended for training speed)

First confirm your CUDA version:
```bash
nvidia-smi          # Note the "CUDA Version" in the top-right corner
```

Install the matching PyTorch build (example for CUDA 11.8):
```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```
> For CUDA 12.1 replace `cu118` with `cu121`. Visit https://pytorch.org/get-started/locally/ to generate the exact command for your version.

### Option B — CPU only (no NVIDIA GPU available)

```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
```

### Verify PyTorch installation

```bash
python3 - <<'EOF'
import torch
print(f"PyTorch version : {torch.__version__}")
print(f"CUDA available  : {torch.cuda.is_available()}")
if torch.cuda.is_available():
    print(f"GPU             : {torch.cuda.get_device_name(0)}")
EOF
```

Expected output (GPU path):
```
PyTorch version : 2.x.x+cu118
CUDA available  : True
GPU             : NVIDIA GeForce RTX xxxx
```

---

## Step 3 — Install OpenCV

```bash
pip install opencv-python        # Headless OK for server; full build for GUI windows
# Optional but useful for annotation previews:
pip install opencv-contrib-python
```

Verify:
```bash
python3 -c "import cv2; print(f'OpenCV version: {cv2.__version__}')"
```

---

## Step 4 — Install Common ML Utilities

```bash
pip install numpy matplotlib pillow seaborn scikit-learn tqdm
pip install onnx onnxruntime          # For ONNX export & inference on Jetson Nano
```

---

## Step 5 — Clone the Ultralytics YOLOv8 Repository

YOLOv8 is the recommended model for this project (see `/docs/model_selection.md`).

```bash
# Install via pip (simplest for training & inference)
pip install ultralytics

# Verify installation
python3 -c "from ultralytics import YOLO; print('Ultralytics YOLOv8 ready')"
```

Clone the full source repo if you need to inspect internals or customize the training loop:
```bash
git clone https://github.com/ultralytics/ultralytics.git
cd ultralytics
pip install -e .       # Editable install — edits to source take effect immediately
```

---

## Step 6 — (Optional) Clone YOLOv5 as Fallback Reference

```bash
cd ~
git clone https://github.com/ultralytics/yolov5.git
cd yolov5
pip install -r requirements.txt
```

---

## Step 7 — Quick Smoke Test (Webcam + Pre-trained Weights)

### YOLOv8 (recommended)

```bash
# Run inference on your webcam (source=0) using the nano model
yolo predict model=yolov8n.pt source=0 show=True
```

Or via Python:

```python
from ultralytics import YOLO

model = YOLO("yolov8n.pt")          # Downloads ~6 MB on first run
results = model.predict(source=0, show=True, conf=0.4)
```

Press `q` to quit the webcam window.

### YOLOv5 (fallback)

```bash
cd ~/yolov5
python detect.py --weights yolov5n.pt --source 0
```

---

## Step 8 — Confirm Full Environment

Run this block to print a complete environment summary:

```bash
python3 - <<'EOF'
import sys, torch, cv2
from ultralytics import YOLO
print("=" * 45)
print(f"Python      : {sys.version.split()[0]}")
print(f"PyTorch     : {torch.__version__}")
print(f"CUDA        : {torch.cuda.is_available()} ({torch.version.cuda})")
print(f"OpenCV      : {cv2.__version__}")
model = YOLO("yolov8n.pt")
print(f"YOLOv8n     : loaded ({sum(p.numel() for p in model.model.parameters())/1e6:.1f}M params)")
print("=" * 45)
print("Environment OK — ready for Milestone 2 training.")
EOF
```

---

## Troubleshooting

| Symptom | Likely Cause | Fix |
|---|---|---|
| `CUDA available: False` | Driver mismatch | Re-install matching CUDA toolkit; reboot |
| Webcam index error (`-1`) | Wrong device ID | Try `source=1` or `source=2` |
| `ModuleNotFoundError: cv2` | OpenCV not in venv | Re-activate venv, then `pip install opencv-python` |
| Low fps on webcam test | CPU-only mode | Expected; training GPU is separate from Jetson deployment |

---

*Last updated: Week 1 — Environment & Infrastructure Setup phase*
