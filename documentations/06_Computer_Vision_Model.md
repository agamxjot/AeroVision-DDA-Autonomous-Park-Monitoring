# 6. Computer Vision Model

## 6.1 Introduction

The computer vision component is designed to automatically identify park-related conditions from aerial images and drone video footage.

A YOLO-based instance segmentation model is used to detect and segment relevant regions within the captured footage.

The model provides visual information that can support park inspection and maintenance analysis.

## 6.2 Dataset Preparation

A custom annotated dataset was prepared using Roboflow.

The dataset contains seven target categories:

1. BROKEN_TREES
2. DRY_AREA
3. PATHWAYS
4. ROOFTOPS
5. VEGETATION
6. WATERBODY
7. WATER_CLOGGING

The dataset was organized into training and validation subsets for model development and evaluation.

## 6.3 Model Architecture

The project uses YOLO-based instance segmentation architectures, including experiments with YOLOv8 and YOLO11.

The segmentation model predicts object locations and corresponding segmentation masks.

The masks provide region-level information beyond bounding-box detection, which is useful for analyzing irregular park features.

## 6.4 Model Training

The model was trained using the prepared custom dataset.

Training involved:
- Dataset loading and preprocessing.
- Model configuration.
- Training over multiple epochs.
- Validation during training.
- Monitoring precision, recall, and mean Average Precision.

The final documented training run used 150 epochs.

## 6.5 Model Performance

The final reported metrics from the 150-epoch training run are:

| Metric | Bounding Box | Segmentation Mask |
|---|---:|---:|
| Precision | 74.26% | — |
| Recall | 61.26% | — |
| mAP@50 | 66.35% | 39.26% |
| mAP@50–95 | 50.89% | 24.19% |

Bounding-box and segmentation metrics are reported separately because they evaluate different prediction outputs.

## 6.6 Video Inference Pipeline

A video-analysis pipeline processes drone footage frame by frame.

The pipeline:
1. Loads the input video.
2. Extracts individual frames.
3. Runs model inference.
4. Obtains predicted classes and segmentation masks.
5. Generates annotated frames.
6. Combines the processed frames into an output video.

## 6.7 Area Analysis and Reporting

The segmentation masks are used to calculate the pixel area occupied by detected regions.

The analysis pipeline generates:
- Annotated output videos.
- Detection summaries.
- Per-frame detection records.
- Class-wise coverage percentages.
- Excel reports containing summary and frame-level information.

**Important:** The current pixel-based area calculation should not be interpreted as physical ground area in square metres unless a suitable camera calibration and ground-scale conversion are applied.

## 6.8 Limitations and Future Improvements

Potential improvements include:
- Increasing the number and diversity of annotated training samples.
- Improving underperforming classes.
- Evaluating performance under different lighting and weather conditions.
- Applying camera calibration for physical area estimation.
- Testing inference performance on the target embedded hardware.