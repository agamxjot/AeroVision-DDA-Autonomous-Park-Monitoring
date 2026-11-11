# DDA Autonomous Park Monitoring Using AI & Drone Technology

An integrated drone-based park inspection framework combining geospatial coverage planning, route optimization, multi-drone mission planning, YOLOv8 instance segmentation and automated maintenance reporting.

## Project Overview

This project aims to automate urban park inspection through autonomous drone-based monitoring and AI-powered visual analysis.

The system combines computational geometry, optimization algorithms and deep learning to identify park features and potential maintenance anomalies across multiple DDA park locations.

## Key Features

- **Geospatial Processing:** Park boundary extraction, coordinate conversion and area calculation.
- **HCP Coverage Planning:** Hexagonal Close Packing-based inspection node generation.
- **Path Optimization:** Nearest Neighbour initialization and 2-opt TSP refinement.
- **Minimum Spanning Tree:** Kruskal-based graph optimization.
- **Multi-Drone Planning:** Battery-constrained waypoint allocation and mission scheduling.
- **AI-Based Inspection:** YOLOv8 instance segmentation across seven park-monitoring classes.
- **Automated Reporting:** Annotated videos, pixel-area analysis and Excel reports.
- **Mission Simulation:** Animated drone trajectories and live telemetry visualization.

## System Architecture

Park Boundary Data  
↓  
Geospatial Coordinate Processing  
↓  
HCP-Based Coverage Generation  
↓  
TSP / 2-Opt Route Optimization  
↓  
Multi-Drone Mission Allocation  
↓  
Drone Mission Simulation  
↓  
Aerial Image & Video Acquisition  
↓  
YOLOv8 Instance Segmentation  
↓  
Area Analysis & Maintenance Reporting

## Detection Categories

1. BROKEN_TREES
2. DRY_AREA
3. PATHWAYS
4. ROOFTOPS
5. VEGETATION
6. WATERBODY
7. WATER_CLOGGING

## Model Performance

Final epoch results from the uploaded 150-epoch training run:

| Metric | Bounding Box | Segmentation |
|---|---:|---:|
| mAP@50 | 66.35% | 39.26% |
| mAP@50–95 | 50.89% | 24.19% |

The model's performance varies across classes, with further improvement opportunities in DRY_AREA and PATHWAYS segmentation.

## Technology Stack

Python · PyTorch · YOLOv8 · OpenCV · NumPy · Pandas · SciPy · PyProj · Matplotlib · Excel

## Repository Structure

- `ALGORITHMS/` – Coverage generation, optimization and mission-planning algorithms.
- `COMPUTER_VISION/` – Model training, inference and video analysis.
- `PARK_RESULTS/` – Park-wise inspection outputs.
- `RESULTS/` – Training curves, evaluation plots and sample results.
- `DOCUMENTATION/` – Detailed technical documentation.

## Documentation

For detailed technical information, see:

- [Project Overview](DOCUMENTATION/01_Project_Overview.md)
- [System Architecture](DOCUMENTATION/02_System_Architecture.md)
- [Geospatial Coverage Planning](DOCUMENTATION/03_Geospatial_Coverage_Planning.md)
- [Algorithm Design](DOCUMENTATION/04_Algorithm_Design.md)
- [Drone Mission Planning](DOCUMENTATION/05_Drone_Mission_Planning.md)
- [Computer Vision Model](DOCUMENTATION/06_Computer_Vision_Model.md)
- [Model Performance](DOCUMENTATION/07_Model_Performance.md)
- [Simulation and Validation](DOCUMENTATION/08_Simulation_and_Validation.md)
- [Hardware Integration](DOCUMENTATION/09_Hardware_Integration.md)
- [Installation and Execution](DOCUMENTATION/10_Installation_and_Execution.md)
- [Limitations and Future Work](DOCUMENTATION/11_Limitations_and_Future_Work.md)

## Installation

```bash
git clone YOUR_REPOSITORY_URL
cd DDA-Autonomous-Park-Monitoring

python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt
```

Refer to the installation documentation for individual module execution and configuration.

## Project Scope

The repository contains algorithm implementations, computer vision pipelines, simulation scripts and representative inspection outputs. Simulation-based estimates are distinguished from independently verified real-world flight performance.

## Acknowledgements

Developed as part of research and engineering work involving autonomous drone-based park monitoring.