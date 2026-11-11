# 2. System Architecture

## 2.1 Architecture Overview

The proposed system follows a modular architecture consisting of five major stages:

1. Geospatial data processing.
2. Coverage generation and route optimization.
3. Drone mission planning.
4. Computer vision-based inspection.
5. Result verification and report generation.

Each module operates independently while contributing to the overall park-monitoring workflow.

## 2.2 System Workflow

### Stage 1: Geospatial Input

Park boundary information is obtained through geographical data such as KML files. The geographical coordinates are processed and converted into a suitable projected coordinate system for distance and area calculations.

### Stage 2: Coverage Planning

The park boundary is used to generate inspection nodes through a hexagonal coverage approach. These nodes represent the geographical locations that need to be inspected by the drones.

### Stage 3: Route Optimization

Generated nodes are converted into a graph or waypoint sequence. Route optimization techniques are applied to reduce unnecessary travel and improve inspection efficiency.

### Stage 4: Drone Mission Planning

The optimized inspection points are assigned to drone missions. Battery endurance, drone speed, altitude, field of view, and estimated mission duration are considered during planning.

### Stage 5: Computer Vision Inspection

Drone video footage is processed using a YOLO-based instance segmentation model. The model identifies relevant park categories and generates annotated visual outputs.

### Stage 6: Reporting and Verification

The system generates structured outputs such as:
- Annotated inspection videos.
- Detection summaries.
- Per-frame analytical data.
- Coverage reports.
- Mission waypoint tables.
- Drone simulation outputs.

## 2.3 Modular Architecture

| Module | Responsibility |
|---|---|
| Geospatial Processing | Boundary extraction and coordinate conversion |
| HCP Coverage Planner | Inspection node generation |
| Route Optimization | Inspection route calculation |
| Multi-Drone Planner | Battery-aware drone allocation |
| Computer Vision | Object and region detection |
| Mission Verification | Simulated trajectory and telemetry |
| Reporting | Excel files, graphs and annotated videos |

## 2.4 Data Flow

The overall data flow is:

Park Boundary → Coordinate Processing → Coverage Node Generation → Route Optimization → Drone Mission Allocation → Video Analysis → Inspection Reports.

The architecture is designed to allow individual modules to be modified or improved without requiring a complete redesign of the system.