# 10. Installation and Execution

## 10.1 Requirements

The project primarily uses Python-based computer vision, geospatial processing, optimization, and visualization libraries.

The environment may require:

- Python 3.10 or compatible version.
- Ultralytics YOLO.
- PyTorch.
- OpenCV.
- NumPy.
- Pandas.
- Matplotlib.
- Scikit-learn.
- OpenPyXL.
- Geospatial processing dependencies used by the selected scripts.

The exact package versions should be maintained in the repository's requirements.txt file.

## 10.2 Repository Setup

Clone the repository:

```bash
git clone YOUR_REPOSITORY_URL
cd DDA-Autonomous-Park-Monitoring
```

## 10.3 Virtual Environment

Create a Python virtual environment:

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

Activate it on Linux:

```bash
source venv/bin/activate
```

## 10.4 Install Dependencies

Install the required packages:

```bash
pip install -r requirements.txt
```

For GPU-based inference, install a PyTorch build compatible with the installed CUDA environment.

## 10.5 Geospatial Coverage Planning

Navigate to the relevant park directory and execute the HCP coverage-planning script.

Example:

```bash
python TSP_2OPT_GEOMETRIC_FINAL.py
```

The script generates coverage and route-related outputs based on its configured input files and parameters.

## 10.6 Multi-Drone Mission Planning

Execute the multi-drone flight planner:

```bash
python MULTI_DRONE_FLIGHT_PLANNER.py
```

The module generates mission waypoint information and drone-wise route segments.

## 10.7 Computer Vision Inference

Run the YOLO video-analysis script:

```bash
python DETECTION_MODEL_FINAL.py
```

Ensure that the input video and trained model weights are available at the paths configured in the script.

## 10.8 Mission Verification

Execute the mission verification module:

```bash
python DRONE_MISSION_VERIFICATION.py
```

The module visualizes the planned drone trajectory and provides mission-related telemetry.

## 10.9 Swarm Simulation

Execute the parallel swarm simulator:

```bash
python ACCELERATED_PARALLEL_SWARM_SIMULATOR.py
```

The simulator visualizes multiple drone agents and their mission progress.

## 10.10 Input and Output Requirements

Typical inputs include:
- Park boundary KML files.
- Drone video footage.
- Trained YOLO model weights.
- Waypoint and mission data files.
- Configuration parameters.

Typical outputs include:
- Annotated videos.
- Excel reports.
- Coverage maps.
- Route optimization graphs.
- Mission tables.
- Simulation visualizations.

## 10.11 Important Notes

File names, input paths, and dependencies may vary between park-specific folders.

Before executing a script, verify its configured input files and output directories.

Large datasets, raw videos, and trained model weights may be maintained separately from the public source repository when they exceed repository storage limits.