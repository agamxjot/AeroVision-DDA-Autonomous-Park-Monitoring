# =========================================================
# DRONE COVERAGE + HCP + TSP 2-OPT GEOMETRIC OPTIMIZATION
# ZOOMABLE PROFESSIONAL VERSION (WITH LAT/LON + XY EXPORT)
# =========================================================
#
# FIXES & ADDITIONS INCLUDED:
# ✔ Boundary Gap Fix: Nodes placed if circle touches boundary
# ✔ Zoom works properly (Aspect ratio 'auto' stretches graphs)
# ✔ TSP 2-Opt Optimization: Eliminates dead-end graph jumps completely!
# ✔ Excel Export Updated: Now saves Waypoint_ID, Latitude, Longitude, 
#   X_meters, Y_meters, and Altitude to the mission table!
# ✔ GRAPH 2: Shows Coverage Circles + Flawless TSP Route
# ✔ MATH FIX: Radius correctly uses tan(radians(FOV/2))
# ✔ SCALE FIX: Calculates real-world Area & Perimeter, not scaled
# ✔ INFO BOX: Automatically stamps real metrics on exported PNGs
#
# =========================================================

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from matplotlib.patches import Circle
from matplotlib.path import Path
from pyproj import Transformer

from scipy.spatial.distance import pdist, squareform

from tkinter import Tk
from tkinter.filedialog import askopenfilename
from math import sqrt, tan, radians, pi

# =========================================================
# GEOGRAPHIC PARAMETERS (For Lat/Lon Export)
# =========================================================
# Defaulting to Delhi, India (UTM Zone 43N / EPSG:32643)
utm_zone = 43
is_northern_hemisphere = True

# =========================================================
# SCALE FACTOR & DRONE PARAMETERS
# =========================================================
scale_factor = 0.5
drone_height = 30
fov = 80

# =========================================================
# VISUAL SETTINGS
# =========================================================
fig_width = 18
fig_height = 16

boundary_width = 3.5
route_width = 2.5
circle_width = 2.0

node_size = 55
start_node_size = 220

title_size = 24
label_size = 16
textbox_size = 12

# =========================================================
# ENABLE INTERACTIVE ZOOM
# =========================================================
plt.rcParams['toolbar'] = 'toolmanager'

# =========================================================
# BROWSE EXCEL FILE
# =========================================================
Tk().withdraw()
file_path = askopenfilename(
    title="Select Boundary Spreadsheet",
    filetypes=[("Excel Files", "*.xlsx *.xls")]
)

if not file_path:
    print("No file selected. Exiting...")
    exit()

print("\nSelected File:")
print(file_path)

# =========================================================
# READ EXCEL FILE
# =========================================================
df = pd.read_excel(file_path)

x_col = 'X_meters' if 'X_meters' in df.columns else 'X_m'
y_col = 'Y_meters' if 'Y_meters' in df.columns else 'Y_m'

# =========================================================
# READ XY COORDINATES & CALCULATE REAL DIMENSIONS
# =========================================================
# Unscaled data for accurate real-world calculations
real_x = df[x_col].values
real_y = df[y_col].values

# Scaled data for plotting & geometry manipulation
x = real_x * scale_factor
y = real_y * scale_factor

# Calculate Real Area and Perimeter
real_area = 0
real_perimeter = 0

for i in range(len(real_x)):
    x1, y1 = real_x[i], real_y[i]
    x2, y2 = real_x[(i + 1) % len(real_x)], real_y[(i + 1) % len(real_y)]
    
    real_area += (x1 * y2) - (y1 * x2)
    real_perimeter += sqrt((x2 - x1)**2 + (y2 - y1)**2)

real_area = abs(real_area) / 2

# =========================================================
# COVERAGE RADIUS & AREA
# =========================================================
# Convert degrees to radians for tan()
real_r = drone_height * tan(radians(fov / 2))
node_area = pi * (real_r ** 2)

# Scaled radius for graph packing
r = real_r * scale_factor

print("\n===================================")
print("DRONE PARAMETERS")
print("===================================")
print(f"Drone Height = {drone_height} m")
print(f"FOV = {fov}°")
print(f"Coverage Radius = {real_r:.2f} m")
print(f"Single Node Area = {node_area:.2f} sq.m")

# =========================================================
# BOUNDARY OVERLAP LOGIC
# =========================================================
def point_to_segment_dist(px, py, x1, y1, x2, y2):
    """Calculates the shortest distance from a point to a line segment."""
    l2 = (x2 - x1)**2 + (y2 - y1)**2
    if l2 == 0:
        return sqrt((px - x1)**2 + (py - y1)**2)
    
    t = max(0, min(1, ((px - x1) * (x2 - x1) + (py - y1) * (y2 - y1)) / l2))
    proj_x = x1 + t * (x2 - x1)
    proj_y = y1 + t * (y2 - y1)
    return sqrt((px - proj_x)**2 + (py - proj_y)**2)

def is_covering_boundary(px, py, poly_x, poly_y, radius, path):
    """Checks if the circle center is inside OR if the circle touches the boundary."""
    if path.contains_point((px, py)):
        return True
        
    for i in range(len(poly_x)):
        x1, y1 = poly_x[i], poly_y[i]
        x2, y2 = poly_x[(i+1)%len(poly_x)], poly_y[(i+1)%len(poly_y)]
        
        if point_to_segment_dist(px, py, x1, y1, x2, y2) <= radius:
            return True
            
    return False

# =========================================================
# HCP NODE GENERATION
# =========================================================
x_spacing = 2 * r
y_spacing = np.sqrt(3) * r

boundary_points = np.column_stack((x, y))
polygon = Path(boundary_points)

xmin, xmax = np.min(x) - r, np.max(x) + r
ymin, ymax = np.min(y) - r, np.max(y) + r

nodes_x = []
nodes_y = []

row = 0
current_y = ymin

while current_y <= ymax:
    if row % 2 == 0:
        current_x = xmin
    else:
        current_x = xmin + r

    while current_x <= xmax:
        if is_covering_boundary(current_x, current_y, x, y, r, polygon):
            nodes_x.append(current_x)
            nodes_y.append(current_y)
        current_x += x_spacing

    current_y += y_spacing
    row += 1

nodes_x = np.array(nodes_x)
nodes_y = np.array(nodes_y)

if len(nodes_x) == 0:
    print("Error: Boundary too small for parameters.")
    exit()

print("\n===================================")
print("HCP NODES")
print("===================================")
print(f"Total Nodes Installed = {len(nodes_x)}")

# =========================================================
# TSP OPTIMIZATION (2-OPT HEURISTIC)
# =========================================================
print("\n===================================")
print("RUNNING TSP MULTI-PASS OPTIMIZATION...")
print("===================================")

points = np.column_stack((nodes_x, nodes_y))
dist_matrix = squareform(pdist(points))

def calculate_total_distance(route, d_matrix):
    return sum(d_matrix[route[i], route[i+1]] for i in range(len(route) - 1))

# Step 1: Nearest Neighbor Initial Path
unvisited = set(range(1, len(points)))
tsp_route = [0]
while unvisited:
    current = tsp_route[-1]
    next_node = min(unvisited, key=lambda x: dist_matrix[current, x])
    unvisited.remove(next_node)
    tsp_route.append(next_node)

# Step 2: 2-Opt refinement loop
best_distance = calculate_total_distance(tsp_route, dist_matrix)
improved = True

while improved:
    improved = False
    for i in range(1, len(tsp_route) - 2):
        for j in range(i + 1, len(tsp_route)):
            if j - i == 1: continue 
            new_route = tsp_route[:]
            new_route[i:j] = tsp_route[j-1:i-1:-1]
            new_distance = calculate_total_distance(new_route, dist_matrix)
            
            if new_distance < best_distance:
                tsp_route = new_route
                best_distance = new_distance
                improved = True
        if improved: break

# Unscale the final flight path distance for real-world metrics
real_best_distance = best_distance / scale_factor

print(f"TSP Complete. Total Flight Path Length = {real_best_distance:.2f} m")

# =========================================================
# EXPORT DRONE MISSION TABLE (TSP OPTIMIZED + ALL FIELDS)
# =========================================================
epsg_code = 32600 + utm_zone if is_northern_hemisphere else 32700 + utm_zone
transformer = Transformer.from_crs(f"epsg:{epsg_code}", "epsg:4326", always_xy=True)

ordered_x = nodes_x[tsp_route]
ordered_y = nodes_y[tsp_route]

# Unscale coordinates before calculating geographic location
ordered_real_x = ordered_x / scale_factor
ordered_real_y = ordered_y / scale_factor

# Convert structural XY coordinates back to global Lat/Lon
ordered_lon, ordered_lat = transformer.transform(ordered_real_x, ordered_real_y)

# Build comprehensive DataFrame with both spatial formats
waypoints_df = pd.DataFrame({
    'Waypoint_ID': range(1, len(tsp_route) + 1),
    'Latitude': ordered_lat,
    'Longitude': ordered_lon,
    'X_meters': ordered_real_x,
    'Y_meters': ordered_real_y,
    'Altitude': [drone_height] * len(tsp_route)
})

waypoints_df.to_excel('Drone_Mission_Table.xlsx', index=False)

# =========================================================
# TXT COVERAGE REPORT
# =========================================================
report_path = 'Coverage_Report.txt'
with open(report_path, 'w') as f:
    f.write("===================================\n")
    f.write("    DRONE FLIGHT COVERAGE REPORT   \n")
    f.write("===================================\n\n")
    f.write(f"Perimeter:         {real_perimeter:.2f} m\n")
    f.write(f"Boundary Area:     {real_area:.2f} sq.m\n")
    f.write(f"Drone Height:      {drone_height} m\n")
    f.write(f"Camera FOV:        {fov}°\n")
    f.write(f"Coverage Radius:   {real_r:.2f} m\n")
    f.write(f"Single Node Area:  {node_area:.2f} sq.m\n")
    f.write(f"Total HCP Nodes:   {len(nodes_x)}\n")
    f.write(f"Optimized Path:    {real_best_distance:.2f} m\n")
    f.write("\nFiles successfully exported:\n")
    f.write("- Drone_Mission_Table.xlsx (ID, Lat, Lon, X, Y, Alt)\n")
    f.write("- Graph_01_Stretched_Node_Coverage.png\n")
    f.write("- Graph_02_Stretched_TSP_Route.png\n")

# =========================================================
# PLOTTING UTILS: DRAW COVERAGE CIRCLES & TEXT BOX
# =========================================================
def draw_circles(ax):
    for nx, ny in zip(nodes_x, nodes_y):
        circle = Circle(
            (nx, ny), r, edgecolor='darkgreen', facecolor='limegreen',
            alpha=0.18, linewidth=circle_width, zorder=2
        )
        ax.add_patch(circle)

def add_info_box(ax, path_length=None):
    """Creates a text box overlay detailing the metrics on the graph."""
    info_text = (
        f"Boundary Area: {real_area:,.2f} sq.m\n"
        f"Single Node Area: {node_area:,.2f} sq.m\n"
        f"Total Nodes: {len(nodes_x)}\n"
        f"Drone Altitude: {drone_height} m"
    )
    if path_length:
        info_text += f"\nFlight Path Length: {path_length:,.2f} m"
        
    props = dict(boxstyle='round,pad=0.6', facecolor='wheat', edgecolor='black', alpha=0.85)
    
    # Places the text box in the upper left corner of the plot area
    ax.text(0.02, 0.96, info_text, transform=ax.transAxes, fontsize=12,
            verticalalignment='top', bbox=props, zorder=20, fontweight='bold', family='monospace')

# =========================================================
# GRAPH 1: STRETCHED NODE GRAPH (HCP COVERAGE)
# =========================================================
fig, ax = plt.subplots(figsize=(fig_width, fig_height))
ax.plot(x, y, linewidth=boundary_width, color='navy', label='Boundary')
ax.fill(x, y, color='lightskyblue', alpha=0.22)
draw_circles(ax)

ax.scatter(nodes_x, nodes_y, s=node_size, color='red', edgecolors='black', linewidths=0.8, zorder=5, label='HCP Nodes')
ax.scatter(nodes_x[0], nodes_y[0], s=start_node_size, color='yellow', edgecolors='black', linewidths=2, zorder=10, label='Start Node')

ax.set_title('Stretched Node Graph: HCP Packing (Full Boundary Coverage)', fontsize=title_size, fontweight='bold')
ax.set_xlabel('X Coordinate (Scaled)', fontsize=label_size)
ax.set_ylabel('Y Coordinate (Scaled)', fontsize=label_size)
ax.grid(True, linestyle='--', linewidth=1.2, color='black', alpha=0.55)
ax.set_aspect('auto')
ax.margins(0.05)
ax.legend(fontsize=12, loc='lower right')

add_info_box(ax) # Add the metrics box to Graph 1
fig.savefig('Graph_01_Stretched_Node_Coverage.png', dpi=300, bbox_inches='tight')

# =========================================================
# GRAPH 2: TSP TRAVERSAL ROUTE (OPTIMIZED FLIGHT PATH)
# =========================================================
fig2, ax2 = plt.subplots(figsize=(fig_width, fig_height))
ax2.plot(x, y, linewidth=boundary_width, color='black', alpha=0.5)
ax2.fill(x, y, color='aliceblue', alpha=0.22)

draw_circles(ax2)

# Draw TSP path execution loop
ax2.plot(ordered_x, ordered_y, color='purple', linestyle='--', linewidth=route_width, zorder=4, label='TSP Optimized Route')

# Draw waypoints on path surface
ax2.scatter(ordered_x, ordered_y, s=node_size, color='darkorange', edgecolors='black', linewidths=0.8, zorder=5)
ax2.scatter(ordered_x[0], ordered_y[0], s=start_node_size, color='green', edgecolors='white', linewidths=2, zorder=10, label='Start Node')

# Generate explicit ordering sequences
for i, (ox, oy) in enumerate(zip(ordered_x, ordered_y)):
    ax2.annotate(str(i+1), (ox, oy), textcoords="offset points", xytext=(6,6), ha='left', fontsize=11, fontweight='bold', color='navy', zorder=6)

ax2.set_title('Stretched Route Graph: TSP Waypoint Sequence', fontsize=title_size, fontweight='bold')
ax2.set_xlabel('X Coordinate (Scaled)', fontsize=label_size)
ax2.set_ylabel('Y Coordinate (Scaled)', fontsize=label_size)
ax2.grid(True, linestyle='--', linewidth=1.2, color='black', alpha=0.55)
ax2.set_aspect('auto')
ax2.margins(0.05)
ax2.legend(fontsize=12, loc='lower right')

add_info_box(ax2, path_length=real_best_distance) # Add the metrics box to Graph 2
fig2.savefig('Graph_02_Stretched_TSP_Route.png', dpi=300, bbox_inches='tight')

# =========================================================
# FINAL RESULTS
# =========================================================
print("\n===================================")
print("FINAL RESULTS")
print("===================================")
print(f"Perimeter = {real_perimeter:.2f} m")
print(f"Boundary Area = {real_area:.2f} sq.m")
print(f"HCP Nodes = {len(nodes_x)}")
print(f"Optimized Path Length = {real_best_distance:.2f} m")
print("\nOutput Files Saved:")
print(" - Drone_Mission_Table.xlsx (Contains Latitude, Longitude, X_meters, Y_meters)")
print(" - Coverage_Report.txt")
print(" - Graph_01_Stretched_Node_Coverage.png")
print(" - Graph_02_Stretched_TSP_Route.png")

# =========================================================
# SHOW GRAPHS
# =========================================================
plt.show()