# Dataset Survey & Strategy
**Document:** `/docs/dataset_survey.md`
**Role:** Vision & AI Developer | **Milestone 1** | ITAI 4376 – Spring 2026

---

## 1. Target Classes

The system must reliably detect four waste categories at inference time:

| Label (final) | Real-world objects included |
|---|---|
| `plastic` | PET water bottles, soda bottles, plastic film/bags |
| `metal_can` | Aluminum beverage cans, steel food cans |
| `paper_cardboard` | Flat paper sheets, crumpled paper, cardboard boxes, cereal boxes |
| `other` *(optional)* | Mixed/unclassified items routed to the default bin |

---

## 2. Public Dataset Sources

### 2.1 TACO — Trash Annotations in Context
- **URL:** https://github.com/pedropro/TACO
- **Size:** ~1,500 images, 4,784 annotations across 60 fine-grained categories
- **Format:** COCO JSON; requires remapping to our 3–4 coarse labels
- **Strengths:** Photographed in real-world outdoor environments (parks, streets); high visual diversity in background and lighting. Strong for generalization.
- **Weaknesses:** Fine-grained label taxonomy (e.g., "Unlabeled litter", "Cigarette") requires manual remapping; relatively small at base size. Plastic bottle and aluminum can coverage is good; paper/cardboard coverage is moderate.
- **Recommended use:** Primary foundation dataset. Remap labels: `{Plastic bottle → plastic, Beverage can → metal_can, Carton → paper_cardboard, Paper → paper_cardboard}`.

### 2.2 Trash Type / Garbage Classification — Roboflow Universe
- **URL:** https://universe.roboflow.com (search "waste detection" or "garbage classification")
- **Notable datasets:** "Garbage Detection" by various contributors; some exceed 5,000 images
- **Format:** YOLOv8-compatible export available directly from Roboflow (saves label conversion effort)
- **Strengths:** Pre-split into train/val/test; Roboflow's free tier supports in-browser augmentation and one-click YOLOv8 export. Several community datasets already use our exact four-class taxonomy.
- **Weaknesses:** Quality varies by contributor; some datasets contain blurry or mislabeled images — always do a manual spot-check of 50–100 samples before training.
- **Recommended use:** Secondary source. Download 2–3 complementary Roboflow datasets and merge with TACO. Target combined size of **2,000–4,000 images** before workspace fine-tuning.

### 2.3 Open Images v7 (Google)
- **URL:** https://storage.googleapis.com/openimages/web/index.html
- **Size:** 9 M images total; subsets downloadable by class
- **Relevant classes:** `Bottle`, `Tin can`, `Cardboard`
- **Format:** Bounding box annotations in CSV; requires conversion to YOLO format
- **Strengths:** Extremely large and diverse; excellent for boosting underrepresented classes. High photographic quality.
- **Weaknesses:** No `paper` class specifically; downloading and converting subsets requires the `fiftyone` library or the official downloader script — adds setup overhead.
- **Recommended use:** Supplementary source for `metal_can` and `plastic` if those classes are underrepresented after merging TACO + Roboflow. Download 300–500 images per relevant class using the OIDv4 toolkit: `pip install openimages`.

---

## 3. Recommended Dataset Assembly Strategy

### Phase 1 — Baseline Dataset (Milestone 2, Weeks 3–4)

1. Download TACO from GitHub. Run the provided label-remapping script (or write a short Python script using the COCO JSON) to map fine-grained labels to our four classes.
2. Download 2–3 Roboflow datasets with YOLOv8 export. Merge with TACO.
3. Inspect class balance. If any class has fewer than 400 training images, supplement with Open Images v7.
4. Final target before fine-tuning: **~2,500–4,000 images, ≥ 400 images per class**.

### Phase 2 — Workspace Fine-Tuning (Milestone 2, after Oren provides environment images)

Oren will provide **15–20 photos per object** captured under actual demo lighting on the real workspace surface. These in-domain images are critical — models trained purely on internet photos often fail under specific lighting conditions or unusual backgrounds.

Steps:
1. Label Oren's images using **LabelImg** (desktop) or **Roboflow** (browser-based, recommended for speed).
2. Add labeled workspace images to the training set.
3. Run a short fine-tuning pass of **30–50 epochs** from the baseline checkpoint.
4. Re-evaluate on the held-out test set; expect 5–15% improvement in real-world accuracy.

---

## 4. Label Remapping Reference

| Source Label | Our Label |
|---|---|
| Plastic bottle, PET bottle, Drink container | `plastic` |
| Beverage can, Tin can, Aluminum can | `metal_can` |
| Paper, Newspaper, Magazine, Cardboard, Carton | `paper_cardboard` |
| Everything else | `other` (or discard if confusing) |

---

## 5. Data Augmentation Plan

Apply the following augmentations during training (configurable in the YOLOv8 YAML):

| Augmentation | Setting | Rationale |
|---|---|---|
| Horizontal flip | 50% probability | Bottles and cans look the same from both sides |
| Brightness jitter | ±30% | Compensate for demo lighting variation |
| HSV hue shift | ±10° | Handle different colored plastic bottles |
| Random rotation | ±10° | Objects placed at slight angles in workspace |
| Mosaic | Enabled (YOLOv8 default) | Improves small-object detection |
| Random crop | 10% | Handles partially visible objects at frame edge |

Avoid aggressive augmentations (large rotations > 45°, heavy blur) — waste items in a real bin have a limited range of natural orientations.

---

## 6. Tools

| Task | Tool | Notes |
|---|---|---|
| Label conversion (COCO → YOLO) | Custom Python script or `roboflow` Python SDK | |
| Manual annotation | LabelImg or Roboflow (free tier) | Roboflow is faster for browser-based annotation |
| Dataset merging and splitting | `roboflow` Python SDK or custom script | |
| Class balance visualization | `matplotlib` histogram on label `.txt` files | |
| Open Images download | `fiftyone` or OIDv4 toolkit | |

---

*Author: Vision & AI Developer | Date: Week 1 | Status: Draft — to be updated in Milestone 2*
