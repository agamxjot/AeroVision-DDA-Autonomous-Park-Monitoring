# 5. Drone Mission Planning

## 5.1 Introduction

The drone mission-planning module converts optimized inspection waypoints into executable or simulated drone missions.

The primary objective is to organize inspection routes while considering operational parameters such as drone speed, battery endurance, altitude, and camera field of view.

## 5.2 Mission Parameters

The current planner uses the following configured parameters:

| Parameter | Configured Value |
|---|---:|
| Drone speed | 6 m/s |
| Battery endurance | 15 minutes |
| Flight altitude | 30 m |
| Camera field of view | 80° |
| Dwell time | 4 seconds |
| Coordinate system | UTM Zone 43N |

These values represent configured simulation and planning assumptions, not necessarily measured real-world performance.

## 5.3 Waypoint Generation

The optimized inspection route is converted into a sequence of geographical waypoints.

Each waypoint contains relevant information such as:
- Waypoint identifier.
- Latitude and longitude.
- Assigned drone identifier.
- Route segment information.

## 5.4 Battery-Aware Mission Allocation

The planner considers the available battery endurance when assigning inspection routes.

When a route exceeds the configured endurance threshold, it is divided into multiple mission segments.

This allows the inspection task to be distributed across separate drone missions rather than assuming that one drone can complete the entire route in a single flight.

## 5.5 Multi-Drone Assignment

Inspection waypoints are distributed among drone missions based on the implemented partitioning and allocation logic.

The system generates a mission table containing waypoint sequences and drone assignments.

## 5.6 Mission Simulation and Verification

A separate verification module simulates drone movement along the generated waypoint sequence.

The simulation provides visual and tabular information such as:
- Current drone position.
- Altitude.
- Traversed distance.
- Waypoint progression.
- Mission trajectory.

## 5.7 Mission Outputs

The mission-planning workflow generates:
- Drone-wise waypoint tables.
- Mission segmentation information.
- Deployment visualizations.
- Simulated trajectory outputs.
- Mission verification reports.

## 5.8 Limitations

The current planning and verification workflow is simulation-oriented. Actual deployment requires hardware-level validation, communication testing, obstacle avoidance, GPS accuracy assessment, regulatory permissions, and flight-safety procedures.