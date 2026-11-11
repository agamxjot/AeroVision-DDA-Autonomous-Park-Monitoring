# 7. Model Performance

## 7.1 Overview

The computer vision model was evaluated using standard object detection and instance segmentation metrics. The evaluation focused on measuring the accuracy of predicted bounding boxes and segmentation masks across the seven park-monitoring categories.

The documented results correspond to the final 150-epoch training run.

## 7.2 Evaluation Metrics

The following metrics were used:

- **Precision:** Measures the proportion of predicted detections that are correct.
- **Recall:** Measures the proportion of actual objects successfully detected.
- **mAP@50:** Mean Average Precision at an Intersection over Union threshold of 0.50.
- **mAP@50–95:** Mean Average Precision averaged across IoU thresholds from 0.50 to 0.95.

Bounding-box and segmentation performance are evaluated separately.

## 7.3 Overall Model Performance

| Metric | Bounding Box | Segmentation Mask |
|---|---:|---:|
| Precision | 74.26% | Not reported |
| Recall | 61.26% | Not reported |
| mAP@50 | 66.35% | 39.26% |
| mAP@50–95 | 50.89% | 24.19% |

The model demonstrates stronger performance in bounding-box detection compared with segmentation-mask prediction.

## 7.4 Class-wise Segmentation Performance

The following values represent class-wise AP@50 from the segmentation evaluation:

| Class | AP@50 |
|---|---:|
| BROKEN_TREES | 62.3% |
| DRY_AREA | 12.2% |
| PATHWAYS | 17.1% |
| ROOFTOPS | 58.8% |
| VEGETATION | 37.1% |
| WATERBODY | 44.5% |
| WATER_CLOGGING | 42.8% |

## 7.5 Performance Analysis

The results indicate variations in performance across different categories.

BROKEN_TREES and ROOFTOPS achieved comparatively stronger segmentation performance, while DRY_AREA and PATHWAYS require further improvement.

The difference between bounding-box and mask performance indicates that accurately locating an object does not necessarily guarantee precise segmentation of its complete region.

## 7.6 Confidence Threshold Analysis

The F1-confidence curve was used to examine the relationship between prediction confidence and the balance between precision and recall.

The observed peak F1 score was approximately 0.50 at a confidence threshold of 0.340.

This provides a reference point for selecting an inference confidence threshold.

## 7.7 Future Performance Improvements

Potential improvements include:
- Increasing the number of annotated examples for underperforming classes.
- Improving annotation consistency.
- Applying class-specific data augmentation.
- Evaluating different model architectures.
- Fine-tuning segmentation parameters.
- Testing generalization across different parks and environmental conditions.

## 7.8 Conclusion

The evaluation establishes a baseline for automated park-condition detection. Although bounding-box detection shows promising results, segmentation performance and class-wise consistency remain important areas for further improvement.