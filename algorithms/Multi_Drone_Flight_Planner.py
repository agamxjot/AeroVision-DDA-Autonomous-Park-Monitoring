# =========================================================
# MULTI-DRONE FLIGHT PLANNER & SIMULATOR
# TWO-FILE VERSION: BOUNDARY PLOT + PRE-SORTED TSP
# =========================================================

import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from matplotlib.patches import Circle
from pyproj import Transformer
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from math import sqrt, tan, radians

# =========================================================
# GEOGRAPHIC PARAMETERS (For Lat/Lon Export)
# =========================================================
utm_zone = 43
is_northern_hemisphere = True

# =========================================================
# REAL-WORLD MISSION PARAMS (CRITICAL THRESHOLDS)
# =========================================================
scale_factor = 1.0            # Set to 1.0 assuming files are in true meters
drone_height = 30             # Altitude in meters
fov = 80                      # Camera Field of View (degrees)

drone_speed = 6.0             # Average drone flight speed in m/s
dwell_time_per_node = 4.0     # Time (seconds) paused at each node for model detection
battery_threshold_mins = 15.0 # Maximum operational flight duration per drone battery/unit

# Convert battery window to absolute operational seconds
max_battery_seconds = battery_threshold_mins * 60.0

# Compute Camera Coverage Radius: r = h * tan(FOV/2)
r = (drone_height * tan(radians(fov / 2))) * scale_factor

# =========================================================
# VISUAL GRAPHICS SETTINGS
# =========================================================
fig_width = 16
fig_height = 14
boundary_width = 3.5
route_width = 2.5
circle_width = 1.5
node_size = 60
start_node_size = 220
title_size = 20

# =========================================================
# FIXED FILE SELECTION ENGINE (TWO FILES)
# =========================================================
root = Tk()
root.withdraw()  # Hide the main root window safely

print("Waiting for Boundary file selection...")
boundary_file = askopenfilename(
    title="1. Select Boundary Spreadsheet (Park Area)",
    filetypes=[("Excel Files", "*.xlsx *.xls")]
)

if not boundary_file:
    print("No boundary file selected. Exiting...")
    root.destroy()
    sys.exit()

print("Waiting for TSP file selection...")
tsp_file = askopenfilename(
    title="2. Select Pre-Calculated TSP Spreadsheet",
    filetypes=[("Excel Files", "*.xlsx *.xls")]
)

root.destroy()  # Utterly destroy the Tk instance so it cannot loop!

if not tsp_file:
    print("No TSP file selected. Exiting...")
    sys.exit()

print(f"\nProcessing Boundary: {boundary_file}")
print(f"Processing TSP: {tsp_file}")

# Load Boundary Data
df_bound = pd.read_excel(boundary_file)
bx_col = 'X_meters' if 'X_meters' in df_bound.columns else 'X_m'
by_col = 'Y_meters' if 'Y_meters' in df_bound.columns else 'Y_m'
bound_x = df_bound[bx_col].values * scale_factor
bound_y = df_bound[by_col].values * scale_factor

# Load TSP Data
df_tsp = pd.read_excel(tsp_file)
tx_col = 'X_meters' if 'X_meters' in df_tsp.columns else 'X_m'
ty_col = 'Y_meters' if 'Y_meters' in df_tsp.columns else 'Y_m'
ordered_x = df_tsp[tx_col].values * scale_factor
ordered_y = df_tsp[ty_col].values * scale_factor
tsp_route_length = len(ordered_x)

if tsp_route_length == 0:
    print("Error: No waypoints found in the TSP file.")
    sys.exit()

# =========================================================
# REAL-WORLD TIME & DRONE QUANTITY CALCULATIONS
# =========================================================
drone_assignments = []  
drone_id_counter = 1
current_drone_time_elapsed = 0.0
total_mission_time_seconds = 0.0
total_distance = 0.0

current_drone_time_elapsed += dwell_time_per_node
total_mission_time_seconds += dwell_time_per_node
drone_assignments.append(drone_id_counter)

for i in range(1, tsp_route_length):
    # Calculate Euclidean distance between current and previous node
    leg_distance = sqrt((ordered_x[i] - ordered_x[i-1])**2 + (ordered_y[i] - ordered_y[i-1])**2)
    total_distance += leg_distance
    
    transit_time = leg_distance / drone_speed
    step_cost_seconds = transit_time + dwell_time_per_node
    
    if current_drone_time_elapsed + step_cost_seconds > max_battery_seconds:
        drone_id_counter += 1
        current_drone_time_elapsed = dwell_time_per_node
        total_mission_time_seconds += step_cost_seconds
    else:
        current_drone_time_elapsed += step_cost_seconds
        total_mission_time_seconds += step_cost_seconds
        
    drone_assignments.append(drone_id_counter)

total_drones_needed = drone_id_counter

# =========================================================
# EXPORT COMPREHENSIVE FLIGHT TABLE
# =========================================================
epsg_code = 32600 + utm_zone if is_northern_hemisphere else 32700 + utm_zone
transformer = Transformer.from_crs(f"epsg:{epsg_code}", "epsg:4326", always_xy=True)
ordered_lon, ordered_lat = transformer.transform(ordered_x, ordered_y)

waypoints_df = pd.DataFrame({
    'Waypoint_ID': range(1, tsp_route_length + 1),
    'Assigned_Drone_ID': drone_assignments,  
    'Latitude': ordered_lat,
    'Longitude': ordered_lon,
    'X_meters': ordered_x,
    'Y_meters': ordered_y,
    'Altitude': [drone_height] * tsp_route_length,
    'Dwell_Time_Sec': [dwell_time_per_node] * tsp_route_length
})
waypoints_df.to_excel('Multi_Drone_Mission_Table.xlsx', index=False)

# =========================================================
# RENDER VISUAL FLIGHT SCHEDULE MAP
# =========================================================
fig, ax = plt.subplots(figsize=(fig_width, fig_height))

# Plot the Boundary File Data
ax.plot(bound_x, bound_y, linewidth=boundary_width, color='black', alpha=0.6, label='Park Boundary', zorder=1)
ax.fill(bound_x, bound_y, color='aliceblue', alpha=0.2, zorder=0)

# Draw the coverage circles around each node
for nx, ny in zip(ordered_x, ordered_y):
    circle = Circle(
        (nx, ny), r, edgecolor='darkgreen', facecolor='limegreen',
        alpha=0.10, linewidth=circle_width, zorder=2
    )
    ax.add_patch(circle)

# Distinct color pool for dividing paths between drone teams
colors_pool = ['#FF1493', '#00EEEE', '#FFD700', '#00FF00', '#FF4500', '#9ACD32', '#0000FF']
drone_colors = {d_id: colors_pool[(d_id - 1) % len(colors_pool)] for d_id in range(1, total_drones_needed + 1)}

# Plot paths connecting segments, color-coded by the assigned drone unit
for i in range(1, tsp_route_length):
    d_id = drone_assignments[i]
    ax.plot([ordered_x[i-1], ordered_x[i]], [ordered_y[i-1], ordered_y[i]],
            color=drone_colors[d_id], linestyle='--', linewidth=route_width, zorder=3)

# Scatter nodes on map colored by drone ownership
for d_id in range(1, total_drones_needed + 1):
    mask = np.array(drone_assignments) == d_id
    ax.scatter(ordered_x[mask], ordered_y[mask], s=node_size, 
               color=drone_colors[d_id], edgecolors='black', label=f'Drone / Battery Pack #{d_id}', zorder=4)

# Highlight swap locations where a new drone sequence takes over
for i in range(1, tsp_route_length):
    if drone_assignments[i] != drone_assignments[i-1]:
        ax.scatter(ordered_x[i], ordered_y[i], s=start_node_size, facecolors='none', 
                   edgecolors='red', linewidths=3, linestyle=':', label='Battery Swap Hub' if i == 1 or 'Battery Swap Hub' not in ax.get_legend_handles_labels()[1] else "", zorder=5)

# Annotate waypoint IDs sequential numbers
for i, (ox, oy) in enumerate(zip(ordered_x, ordered_y)):
    ax.annotate(str(i+1), (ox, oy), textcoords="offset points", xytext=(5,5), ha='left', fontsize=10, fontweight='bold', color='navy', zorder=6)

# Setup Information Dashboard Box
info_text = (
    f"=== FLEET DATA ANALYSIS ===\n"
    f"Total Waypoints: {tsp_route_length}\n"
    f"Coverage Radius: {r:.2f} m\n"
    f"Drone Avg Speed: {drone_speed} m/s\n"
    f"Model Dwell Time: {dwell_time_per_node}s / node\n"
    f"Battery Limit: {battery_threshold_mins} mins\n"
    f"-----------------------\n"
    f"DRONES REQUIRED: {total_drones_needed}\n"
    f"TOTAL TIME: {total_mission_time_seconds / 60.0:.2f} mins"
)
ax.text(0.02, 0.05, info_text, transform=ax.transAxes, fontsize=12, fontweight='bold',
        bbox=dict(facecolor='white', edgecolor='darkmagenta', alpha=0.9, boxstyle='round,pad=0.6'), zorder=10)

ax.set_title('Strategic Multi-Drone Fleet Deployment & Traversal Map', fontsize=title_size, fontweight='bold')
ax.set_xlabel('X Metrics Plane (meters)', fontsize=12)
ax.set_ylabel('Y Metrics Plane (meters)', fontsize=12)
ax.grid(True, linestyle=':', alpha=0.6, color='gray')

# CHANGED: Aspect set to 'auto' to allow the graph to visually stretch into narrow bounds
ax.set_aspect('auto') 

ax.legend(loc='upper right', fontsize=11)

# Save high-res chart
fig.savefig('Graph_Multi_Drone_Flight_Plan.png', dpi=300, bbox_inches='tight')

# =========================================================
# PRINT SUMMARY INSIGHTS
# =========================================================
print("\n=======================================================")
print("            FLEET MISSION OPERATIONS REPORT             ")
print("=======================================================")
print(f"Total Coverage Path Distance     : {total_distance:.2f} meters")
print(f"Calculated Camera Radius (r)     : {r:.2f} meters")
print(f"Configured Processing Dwell Time : {dwell_time_per_node} seconds per stop")
print(f"Operational Battery Endurance    : {battery_threshold_mins} minutes per unit")
print("-------------------------------------------------------")
print(f"TOTAL DRONE UNITS / BATTERIES REQUIRED : {total_drones_needed}")
print(f"TOTAL ESTIMATED DEPLOYMENT TIME        : {total_mission_time_seconds / 60.0:.2f} minutes")
print("=======================================================\n")

plt.show()