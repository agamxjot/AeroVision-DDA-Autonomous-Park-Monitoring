# =========================================================
# DRONE MISSION VERIFICATION AND TRAVERSAL SIMULATOR (WITH CIRCLES)
# =========================================================
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Circle
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from math import sqrt, tan, radians

# =========================================================
# INITIAL SETS & PARAMETERS
# =========================================================
scale_factor = 0.5  # Must match the generation script scale
drone_height = 30   # Must match generation script to compute accurate radius
fov = 90            # Must match generation script
fig_width = 14
fig_height = 10

# Calculate exact coverage radius used during generation
r = (drone_height * tan(radians(fov / 2))) * scale_factor

# Hide root window for tkinter file picker
Tk().withdraw()

# 1. Browse and Load Boundary File
print("Select your Boundary Spreadsheet...")
boundary_path = askopenfilename(
    title="1. Select Boundary Spreadsheet",
    filetypes=[("Excel Files", "*.xlsx *.xls")]
)
if not boundary_path:
    print("Boundary file selection canceled. Exiting...")
    exit()

# 2. Browse and Load Waypoints File
print("Select your generated Drone_Mission_Table spreadsheet...")
waypoints_path = askopenfilename(
    title="2. Select Generated Drone_Mission_Table",
    filetypes=[("Excel Files", "*.xlsx *.xls")]
)
if not waypoints_path:
    print("Waypoint file selection canceled. Exiting...")
    exit()

# =========================================================
# PARSING FILE COORD DATA
# =========================================================
# Read Boundary
df_bound = pd.read_excel(boundary_path)
bx_col = 'X_meters' if 'X_meters' in df_bound.columns else 'X_m'
by_col = 'Y_meters' if 'Y_meters' in df_bound.columns else 'Y_m'
bound_x = df_bound[bx_col].values * scale_factor
bound_y = df_bound[by_col].values * scale_factor

# Ensure boundary loops completely back to start for plotting
if (bound_x[0], bound_y[0]) != (bound_x[-1], bound_y[-1]):
    bound_x = np.append(bound_x, bound_x[0])
    bound_y = np.append(bound_y, bound_y[0])

# Read Mission Waypoints
df_wp = pd.read_excel(waypoints_path)
wp_id = df_wp['Waypoint_ID'].values
wp_x = df_wp['X_meters'].values
wp_y = df_wp['Y_meters'].values
wp_alt = df_wp['Altitude'].values

print(f"\nSuccessfully loaded {len(wp_id)} waypoints for verification flight.")

# Calculate Cumulative Distances between waypoints
distances = [0.0]
total_dist = 0.0
for i in range(1, len(wp_x)):
    d = sqrt((wp_x[i] - wp_x[i-1])**2 + (wp_y[i] - wp_y[i-1])**2)
    total_dist += d
    distances.append(total_dist)

# =========================================================
# INITIALIZE INTERACTIVE SIMULATION PLOT
# =========================================================
fig, ax = plt.subplots(figsize=(fig_width, fig_height))
ax.set_aspect('auto')
ax.grid(True, linestyle='--', alpha=0.6, color='gray')

# Static Elements
ax.plot(bound_x, bound_y, color='black', linewidth=3, label='Zone Boundary', zorder=1)
ax.fill(bound_x, bound_y, color='dimgray', alpha=0.15)

# ---> ADDED: Draw the coverage circle for each waypoint node <---
for nx, ny in zip(wp_x, wp_y):
    circle = Circle(
        (nx, ny), r, edgecolor='darkgreen', facecolor='limegreen',
        alpha=0.12, linewidth=1.5, zorder=2
    )
    ax.add_patch(circle)

ax.plot(wp_x, wp_y, color='purple', linestyle=':', linewidth=1.5, alpha=0.7, label='Planned Path Blueprint')
ax.scatter(wp_x, wp_y, color='darkorange', s=30, edgecolors='black', zorder=3)

# Dynamic Simulation Elements
trail_line, = ax.plot([], [], color='mediumvioletred', linewidth=2.5, linestyle='-', label='Actual Flight Track', zorder=4)
drone_marker, = ax.plot([], [], color='lime', marker='o', markersize=14, markeredgecolor='black', markeredgewidth=2, zorder=5)

# Setup live telemetry dashboard textbox overlay
telemetry_text = ax.text(
    0.02, 0.95, '', transform=ax.transAxes, fontsize=12,
    fontfamily='monospace', fontweight='bold',
    bbox=dict(facecolor='white', alpha=0.85, edgecolor='navy', boxstyle='round,pad=0.5'),
    zorder=6
)

ax.set_title("Drone Simulation Verification Dashboard", fontsize=18, fontweight='bold', pad=15)
ax.set_xlabel("X Metric Plane (meters)", fontsize=12)
ax.set_ylabel("Y Metric Plane (meters)", fontsize=12)
ax.legend(loc='lower right', fontsize=10)

# Set dynamic coordinate viewing margins
ax.set_xlim(min(min(bound_x), min(wp_x)) - 30, max(max(bound_x), max(wp_x)) + 30)
ax.set_ylim(min(min(bound_y), min(wp_y)) - 30, max(max(bound_y), max(wp_y)) + 30)

# =========================================================
# ANIMATION STEP ENGINE
# =========================================================
frames_per_segment = 10  # Smooth transition resolution steps between waypoints
total_frames = (len(wp_x) - 1) * frames_per_segment

def update_sim(frame):
    # Determine which leg segment the drone is executing
    seg_idx = frame // frames_per_segment
    t = (frame % frames_per_segment) / frames_per_segment  # Normalized interpolation interval [0, 1)
    
    # Calculate linear position interpolation between current and target node
    x_curr, y_curr = wp_x[seg_idx], wp_y[seg_idx]
    x_next, y_next = wp_x[seg_idx + 1], wp_y[seg_idx + 1]
    
    drone_x = x_curr + t * (x_next - x_curr)
    drone_y = y_curr + t * (y_next - y_curr)
    
    # Render updated path trace history
    history_x = np.append(wp_x[:seg_idx + 1], drone_x)
    history_y = np.append(wp_y[:seg_idx + 1], drone_y)
    trail_line.set_data(history_x, history_y)
    
    # Move active marker
    drone_marker.set_data([drone_x], [drone_y])
    
    # Continuous telemetry output calculations
    current_leg_dist = t * sqrt((x_next - x_curr)**2 + (y_next - y_curr)**2)
    live_odometer = distances[seg_idx] + current_leg_dist
    
    telemetry_text.set_text(
        f"=== LIVE TELEMETRY ===\n"
        f"Last WP Passed : ID {wp_id[seg_idx]}\n"
        f"Heading To     : ID {wp_id[seg_idx + 1]}\n"
        f"Pos X (Meters) : {drone_x:.2f} m\n"
        f"Pos Y (Meters) : {drone_y:.2f} m\n"
        f"Altitude       : {wp_alt[seg_idx]:.1f} m\n"
        f"Odometer Track : {live_odometer:.2f} / {total_dist:.2f} m"
    )
    
    return trail_line, drone_marker, telemetry_text

# Run live playback loop
ani = FuncAnimation(
    fig, update_sim, frames=total_frames, 
    interval=60, blit=True, repeat=False
)

plt.show()