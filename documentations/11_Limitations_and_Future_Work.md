# 11. Limitations and Future Work

## 11.1 Current Limitations

Although the proposed framework integrates geospatial planning, computer vision, and drone mission simulation, several limitations remain.

### 1. Computer Vision Performance

The segmentation model demonstrates varying performance across the seven monitoring categories.

DRY_AREA and PATHWAYS have comparatively lower segmentation AP@50 values, indicating the need for improved training data and model refinement.

### 2. Dataset Diversity

Model generalization depends on the diversity and quality of the annotated dataset.

Differences in lighting, weather, camera altitude, image resolution, and park conditions may affect detection performance.

### 3. Pixel-Based Area Estimation

The current area-analysis pipeline calculates the pixel area of predicted segmentation masks.

Without camera calibration, ground sampling distance, and suitable geometric correction, these values cannot be directly interpreted as physical ground area in square metres.

### 4. Geospatial Coverage Assumptions

Coverage planning uses configured drone altitude and camera field-of-view parameters.

Actual coverage may differ due to terrain, obstacles, camera orientation, and environmental conditions.

### 5. Route Optimization

Heuristic route optimization methods such as nearest neighbour and 2-opt do not guarantee a globally optimal TSP solution.

Additional constraints such as obstacles, no-fly zones, and real-time flight conditions are not necessarily represented in the current route model.

### 6. Simulation-to-Reality Gap

The drone mission and swarm simulators evaluate software-level mission logic.

Real-world flight performance may differ due to wind, GPS errors, communication delays, battery degradation, and hardware limitations.

### 7. Hardware Deployment

The deployment workflow requires further validation on the final embedded hardware configuration.

Real-time inference, flight-controller communication, and power requirements must be evaluated under actual operating conditions.

## 11.2 Future Work

### 1. Computer Vision Improvements

- Expand the annotated dataset.
- Improve segmentation performance for underperforming classes.
- Evaluate additional YOLO architectures.
- Apply advanced augmentation strategies.
- Optimize inference for embedded deployment.

### 2. Physical Area Estimation

- Integrate camera calibration.
- Estimate ground sampling distance.
- Apply perspective and geometric corrections.
- Convert segmentation pixel measurements into estimated physical areas.

### 3. Advanced Coverage Planning

- Improve boundary-aware node generation.
- Introduce obstacle-aware coverage planning.
- Evaluate adaptive inspection-point density.
- Incorporate overlapping image coverage requirements.

### 4. Advanced Route Optimization

- Compare additional TSP heuristics.
- Incorporate no-fly zones and obstacles.
- Optimize route assignment across multiple drones.
- Consider energy consumption and mission duration jointly.

### 5. Multi-Drone Coordination

- Develop more advanced swarm coordination.
- Introduce communication-aware task allocation.
- Evaluate dynamic mission reassignment.
- Incorporate collision avoidance and real-time position updates.

### 6. Embedded Deployment

- Benchmark inference on Jetson hardware.
- Optimize model size and inference latency.
- Integrate the perception pipeline with the flight controller.
- Validate telemetry and communication reliability.

### 7. Real-World Validation

- Conduct controlled outdoor flight tests.
- Compare predicted coverage with actual drone imagery.
- Evaluate detection performance across different parks.
- Measure mission completion time and inspection efficiency.

## 11.3 Conclusion

The project establishes a modular foundation for autonomous park monitoring by combining computer vision, geospatial coverage planning, route optimization, and multi-drone simulation.

Future development will focus on improving segmentation accuracy, introducing more realistic operational constraints, validating embedded deployment, and bridging the gap between software simulation and real-world autonomous inspection.