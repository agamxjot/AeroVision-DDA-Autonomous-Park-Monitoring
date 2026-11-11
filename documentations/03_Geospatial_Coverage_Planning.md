# 3. Geospatial Coverage Planning

## 3.1 Introduction

Geospatial coverage planning is responsible for dividing a park's geographical area into systematic inspection points. The objective is to generate a set of waypoints that enables drones to inspect the park while minimizing unnecessary travel and maintaining geographical coverage.

## 3.2 Boundary Extraction

Park boundaries are obtained from KML geographical data containing latitude and longitude coordinates.

Since latitude and longitude are angular measurements, they are converted into projected coordinates before performing distance-based calculations.

The project uses UTM Zone 43N for its geographical processing workflow.

## 3.3 Coordinate Transformation

Geographical coordinates are transformed into metric coordinates to support distance calculations.

The resulting coordinates are used for:
- Boundary representation.
- Distance calculations.
- Inspection node generation.
- Route optimization.
- Coverage visualization.

## 3.4 Hexagonal Coverage Planning

A Hexagonal Coverage Planning (HCP) approach is used to distribute inspection nodes across the park.

Hexagonal arrangements provide a structured way to distribute inspection locations while reducing irregular gaps between neighboring coverage regions.

The coverage radius is calculated using the drone altitude and camera field of view.

\[
r=h\tan\left(\frac{\theta}{2}\right)
\]

Where:

- \(r\) = Ground coverage radius.
- \(h\) = Drone altitude.
- \(\theta\) = Camera field of view.

The horizontal spacing between neighboring nodes is based on the coverage geometry:

\[
d_x=2r
\]

\[
d_y=\sqrt{3}r
\]

The generated nodes are checked against the park boundary to retain relevant inspection locations.

## 3.5 Coverage Visualization

The generated inspection nodes are plotted over the park boundary to visually evaluate their distribution.

The resulting maps help identify:
- Areas covered by inspection nodes.
- Potential gaps in node distribution.
- Boundary-related coverage issues.
- Overall inspection-point density.

## 3.6 Coverage Output

The geospatial planning module generates:
- Park boundary visualizations.
- HCP node maps.
- Geographical waypoint coordinates.
- Coverage-related reports.
- Input data for subsequent route optimization and mission planning.

## 3.7 Limitations

The calculated coverage represents the geometric ground footprint based on the selected altitude and field-of-view assumptions. Actual coverage may vary due to terrain, camera orientation, obstacles, image overlap, and flight conditions.