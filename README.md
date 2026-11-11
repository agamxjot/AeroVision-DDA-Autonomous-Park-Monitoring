# AeroVision: DDA Autonomous Park Monitoring System

A drone-based autonomous park monitoring system combining computer vision, geospatial coverage planning, route optimization, and multi-drone mission simulation.

The project explores how autonomous drones can assist in monitoring urban parks through aerial image analysis, vegetation and infrastructure detection, and optimized mission planning.

## Project Overview

The system consists of three major components:

1. **Computer Vision:** YOLOv8-based instance segmentation for identifying park features and potential anomalies.
2. **Geospatial Coverage Planning:** Hexagonal Coverage Planning (HCP), waypoint generation, and route optimization for systematic aerial coverage.
3. **Drone Mission Planning:** Battery-constrained multi-drone mission allocation and simulated drone navigation.

The project was developed and evaluated using seven park locations associated with the Delhi Development Authority (DDA).

## Key Features

- YOLOv8 instance segmentation for park feature detection.
- Detection classes including vegetation, pathways, rooftops, water bodies, dry areas, broken trees, and water clogging.
- Hexagonal Coverage Planning for waypoint generation.
- Nearest Neighbour route initialization and 2-opt route optimization.
- Multi-drone mission planning with battery endurance constraints.
- Parallel swarm simulation and waypoint traversal visualization.
- Coverage analysis, mission tables, graphs, and Excel-based reporting.

## Repository Structure

```text
DDA-Autonomous-Park-Monitoring/
│
├── algorithms/
│   ├── HCP_Node_Generation.py
│   ├── Multi_Drone_Flight_Planner.py
│   ├── Parallel_Swarm_Simulator.py
│   ├── Simulation.py
│   └── README.md
│
├── documentations/
│   ├── 01_Project_Overview.md
│   ├── 02_System_Architecture.md
│   ├── 03_Geospatial_Coverage_Planning.md
│   ├── 04_Algorithm_Design.md
│   ├── 05_Drone_Mission_Planning.md
│   ├── 06_Computer_Vision_Model.md
│   ├── 07_Model_Performance.md
│   ├── 08_Simulation_and_Validation.md
│   ├── 09_Hardware_Integration.md
│   ├── 10_Installation_and_Execution.md
│   └── 11_Limitations_and_Future_Work.md
│
├── model_detection/
│   ├── Video_Instance_Segmentation_Analyzer.py
│   ├── results.csv
│   ├── results.png
│   ├── confusion_matrix.png
│   └── training and validation visualizations
│
├── results/
│   ├── Asaf_Ali/
│   ├── Lala_Hardyal/
│   ├── Rohini_Park/
│   ├── Sanjay_Lake/
│   ├── Smriti_Van/
│   ├── Vasant_Udyan/
│   └── Vasant_Vatika/
│
├── requirements.txt
├── .gitignore
└── README.md
```

## Computer Vision Model

The project uses a YOLOv8 instance segmentation model trained to identify park-related features and anomalies.

**Detection classes:**
- BROKEN_TREES
- DRY_AREA
- PATHWAYS
- ROOFTOPS
- VEGETATION
- WATERBODY
- WATER_CLOGGING

### Model Performance

Reported metrics from the final 150-epoch training run:

| Metric | Bounding Boxes | Segmentation Masks |
|---|---:|---:|
| mAP@50 | 66.35% | 39.26% |
| mAP@50–95 | 50.89% | 24.19% |

Additional bounding-box metrics:

- Precision: 74.26%
- Recall: 61.26%

These are validation results and should not be interpreted as guaranteed real-world detection performance.

## Geospatial Coverage Planning

The coverage-planning module generates spatial waypoints across park boundaries using a hexagonal node arrangement.

The planning workflow includes:

1. Park boundary processing.
2. Coordinate conversion into a projected coordinate system.
3. Hexagonal waypoint generation.
4. Coverage-node selection.
5. Initial route generation using the Nearest Neighbour heuristic.
6. Route refinement using 2-opt optimization.
7. Mission table and coverage visualization generation.

## Multi-Drone Mission Planning

The multi-drone planning module explores dividing a mission into smaller battery-constrained flight segments.

The simulation incorporates:
- Drone endurance constraints.
- Flight speed and waypoint dwell time.
- Mission allocation.
- Route visualization.
- Mission time estimation.

The parallel swarm simulator visualizes drone movement and mission execution through simulated trajectories and telemetry.

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/agamxjot/DDA-Autonomous-Park-Monitoring.git
cd DDA-Autonomous-Park-Monitoring
```

### 2. Create a virtual environment

Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

Linux/macOS:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Model weights

The trained YOLO model weights are not included in this repository.

Obtain the appropriate trained `.pt` weights separately and configure the model-weight path in `Video_Instance_Segmentation_Analyzer.py` before running video inference.

## Running the Project

Run the individual algorithm modules from the project root or follow their respective execution instructions.

Examples:

```bash
python algorithms/HCP_Node_Generation.py
```

```bash
python algorithms/Multi_Drone_Flight_Planner.py
```

```bash
python algorithms/Parallel_Swarm_Simulator.py
```

```bash
python algorithms/Simulation.py
```

For video-based instance segmentation:

```bash
python model_detection/Video_Instance_Segmentation_Analyzer.py
```

**Note:** The scripts may require input park boundary files, videos, model weights, or other configuration paths. Configure these inputs according to the source code before execution.

## Experimental Results

The repository contains selected outputs from seven park locations:

- Asaf Ali
- Lala Hardyal
- Rohini Park
- Sanjay Lake
- Smriti Van
- Vasant Udyan
- Vasant Vatika

Available outputs include:
- Drone mission tables.
- Coverage reports.
- Route and node visualizations.
- Multi-drone flight planning graphs.
- Detection analysis spreadsheets.

## Documentation

Detailed technical documentation is available in the [`documentations/`](documentations/) directory.

| Document | Description |
|---|---|
| [Project Overview](documentations/01_Project_Overview.md) | Objectives and project scope |
| [System Architecture](documentations/02_System_Architecture.md) | Overall system design |
| [Geospatial Coverage Planning](documentations/03_Geospatial_Coverage_Planning.md) | Spatial waypoint generation |
| [Algorithm Design](documentations/04_Algorithm_Design.md) | Planning and optimization methods |
| [Drone Mission Planning](documentations/05_Drone_Mission_Planning.md) | Mission allocation and execution |
| [Computer Vision Model](documentations/06_Computer_Vision_Model.md) | YOLOv8 model and detection classes |
| [Model Performance](documentations/07_Model_Performance.md) | Training and validation metrics |
| [Simulation and Validation](documentations/08_Simulation_and_Validation.md) | Simulation methodology |
| [Hardware Integration](documentations/09_Hardware_Integration.md) | Hardware integration considerations |
| [Installation and Execution](documentations/10_Installation_and_Execution.md) | Setup and execution instructions |
| [Limitations and Future Work](documentations/11_Limitations_and_Future_Work.md) | Current limitations and improvements |

## Limitations

- Segmentation performance varies across detection classes.
- Some classes require additional training data and model refinement.
- Mission planning and swarm behavior are evaluated through software simulations.
- Real-world flight performance depends on hardware, GPS accuracy, battery characteristics, and environmental conditions.
- Accurate physical-area estimation from video requires appropriate camera calibration and ground-scale information.

## Future Work

Potential improvements include:

- Improving segmentation accuracy for underperforming classes.
- Integrating real-time drone telemetry.
- Implementing collision avoidance and dynamic mission reassignment.
- Testing mission planning with physical drone platforms.
- Improving camera calibration and physical-area estimation.
- Developing a centralized park-monitoring dashboard.

## Project Status

This repository contains the project's software modules, model evaluation outputs, selected experimental results, and technical documentation.

The distinction between software simulation, model evaluation, and physical drone deployment is maintained throughout the documentation.

---

**Project:** DDA Autonomous Park Monitoring System  
**Domain:** Embedded Systems | Computer Vision | UAVs | Geospatial Analysis | Autonomous Systems  
**Repository:** [GitHub](https://github.com/agamxjot/DDA-Autonomous-Park-Monitoring)
