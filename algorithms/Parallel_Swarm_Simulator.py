# =========================================================
# ACCELERATED PARALLEL SWARM SIMULATOR WITH LIVE TABLE
# =========================================================
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Circle
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from math import sqrt, tan, radians

# =========================================================
# 1. PARAMETERS
# =========================================================
scale_factor = 0.5   
drone_height = 30    
fov = 90             

drone_speed = 6.0             # Transit speed (m/s)
dwell_time = 3.0              # 3.0 seconds scanning/detection time per node
battery_threshold_mins = 15.0 # Max operation limit per drone
max_battery_seconds = battery_threshold_mins * 60.0

fig_width = 16
fig_height = 11
r = (drone_height * tan(radians(fov / 2))) * scale_factor

# =========================================================
# 2. FILE LOADING
# =========================================================
root = Tk()
root.withdraw()

print("1. Select your Boundary Spreadsheet...")
boundary_path = askopenfilename(title="1. Select Boundary", filetypes=[("Excel Files", "*.xlsx *.xls")])
if not boundary_path: sys.exit()

print("2. Select your Generated Waypoints/Mission Table...")
waypoints_path = askopenfilename(title="2. Select Waypoints", filetypes=[("Excel Files", "*.xlsx *.xls")])
root.destroy()
if not waypoints_path: sys.exit()

# Parse files
df_bound = pd.read_excel(boundary_path)
bound_x = df_bound['X_meters' if 'X_meters' in df_bound.columns else 'X_m'].values * scale_factor
bound_y = df_bound['Y_meters' if 'Y_meters' in df_bound.columns else 'Y_m'].values * scale_factor

if (bound_x[0], bound_y[0]) != (bound_x[-1], bound_y[-1]):
    bound_x = np.append(bound_x, bound_x[0])
    bound_y = np.append(bound_y, bound_y[0])

df_wp = pd.read_excel(waypoints_path)
wp_id = df_wp['Waypoint_ID'].values
wp_x = df_wp['X_meters'].values
wp_y = df_wp['Y_meters'].values

# =========================================================
# 3. SWARM PARTITIONING MATH
# =========================================================
drone_paths = []
current_path = [0]
current_time = dwell_time 

for i in range(1, len(wp_x)):
    dist = sqrt((wp_x[i] - wp_x[i-1])**2 + (wp_y[i] - wp_y[i-1])**2)
    step_cost = (dist / drone_speed) + dwell_time
    
    if current_time + step_cost > max_battery_seconds:
        drone_paths.append(current_path)
        current_path = [i-1, i] 
        current_time = (dist / drone_speed) + dwell_time
    else:
        current_path.append(i)
        current_time += step_cost

drone_paths.append(current_path)
num_drones = len(drone_paths)

# =========================================================
# 4. PRE-BUILD TIMELINES (OPTIMIZED FOR SPEEDUP)
# =========================================================
fps = 2# ACCELERATION: Dropping steps per second to move faster through legs
timelines = []
colors_pool = ['#FF1493', '#00EEEE', '#FFD700', '#00FF00', '#FF4500', '#9ACD32', '#0000FF']
drone_colors = [colors_pool[i % len(colors_pool)] for i in range(num_drones)]

max_frames = 0

for d_idx, path in enumerate(drone_paths):
    tl_x, tl_y, tl_active = [], [], []
    tl_status, tl_bat = [], []
    rem_bat_seconds = max_battery_seconds
    
    for p_idx, w_idx in enumerate(path):
        is_first_node_of_drone = (p_idx == 0)
        is_very_first_mission_node = (w_idx == 0)
        
        # A. Dwell Phase
        if not is_first_node_of_drone or is_very_first_mission_node:
            dwell_frames = int(dwell_time * fps)
            for _ in range(dwell_frames):
                tl_x.append(wp_x[w_idx])
                tl_y.append(wp_y[w_idx])
                tl_active.append(True)
                tl_status.append(f"SCAN WP {wp_id[w_idx]}")
                tl_bat.append(max(0.0, rem_bat_seconds / 60.0))
                rem_bat_seconds -= (1.0 / fps)
                
        # B. Transit Phase
        if p_idx < len(path) - 1:
            next_w = path[p_idx+1]
            dist = sqrt((wp_x[next_w] - wp_x[w_idx])**2 + (wp_y[next_w] - wp_y[w_idx])**2)
            transit_frames = max(1, int((dist / drone_speed) * fps))
            
            for f in range(transit_frames):
                frac = f / float(transit_frames)
                tl_x.append(wp_x[w_idx] + frac * (wp_x[next_w] - wp_x[w_idx]))
                tl_y.append(wp_y[w_idx] + frac * (wp_y[next_w] - wp_y[w_idx]))
                tl_active.append(True)
                tl_status.append(f"TO WP {wp_id[next_w]}")
                tl_bat.append(max(0.0, rem_bat_seconds / 60.0))
                rem_bat_seconds -= (1.0 / fps)
                
    timelines.append({'x': tl_x, 'y': tl_y, 'active': tl_active, 'status': tl_status, 'bat': tl_bat})
    if len(tl_x) > max_frames:
        max_frames = len(tl_x)

# Pad tracking lists
for tl in timelines:
    shortfall = max_frames - len(tl['x'])
    if shortfall > 0:
        tl['x'].extend([tl['x'][-1]] * shortfall)
        tl['y'].extend([tl['y'][-1]] * shortfall)
        tl['active'].extend([False] * shortfall)
        tl['status'].extend(["LANDED/DONE"] * shortfall)
        last_bat = tl['bat'][-1] if tl['bat'] else battery_threshold_mins
        tl['bat'].extend([last_bat] * shortfall)

# =========================================================
# 5. GRAPHICS & DASHBOARD SETUP
# =========================================================
fig, ax = plt.subplots(figsize=(fig_width, fig_height))
ax.set_aspect('auto')
ax.grid(True, linestyle='--', alpha=0.5, color='gray')

ax.plot(bound_x, bound_y, color='black', linewidth=3, zorder=1)
ax.fill(bound_x, bound_y, color='dimgray', alpha=0.12)

rendered_nodes = set()
for i, path in enumerate(drone_paths):
    d_color = drone_colors[i]
    for w_idx in path:
        nx, ny = wp_x[w_idx], wp_y[w_idx]
        ax.add_patch(Circle((nx, ny), r, edgecolor=d_color, facecolor=d_color, alpha=0.14, linewidth=1.2, zorder=2))
        ax.scatter(nx, ny, color='darkorange', s=20, edgecolors='black', zorder=4)
        
        if w_idx not in rendered_nodes:
            ax.annotate(str(wp_id[w_idx]), (nx, ny), textcoords="offset points", xytext=(3,3), 
                        ha='left', va='bottom', fontsize=8, color='black', alpha=0.7, fontweight='bold', zorder=8)
            rendered_nodes.add(w_idx)

ax.plot(wp_x, wp_y, color='purple', linestyle=':', linewidth=1.0, alpha=0.4, zorder=3)

trails = []
markers = []
for i in range(num_drones):
    t, = ax.plot([], [], color=drone_colors[i], linewidth=2.5, zorder=5)
    m, = ax.plot([], [], marker='o', markersize=12, markeredgecolor='black', color=drone_colors[i], zorder=6)
    trails.append(t)
    markers.append(m)

telemetry_box = ax.text(
    0.01, 0.98, '', transform=ax.transAxes, fontsize=10, fontfamily='monospace', fontweight='bold',
    va='top', ha='left',
    bbox=dict(facecolor='white', alpha=0.92, edgecolor='navy', boxstyle='round,pad=0.6'), zorder=10
)

for path, color in zip(drone_paths, drone_colors):
    ax.scatter(wp_x[path[0]], wp_y[path[0]], s=200, facecolors='none', edgecolors=color, linewidths=3, zorder=7)

ax.set_title("Simultaneous Swarm Verification & Live Telemetry Table", fontsize=16, fontweight='bold', pad=15)
ax.set_xlim(min(min(bound_x), min(wp_x)) - 30, max(max(bound_x), max(wp_x)) + 30)
ax.set_ylim(min(min(bound_y), min(wp_y)) - 30, max(max(bound_y), max(wp_y)) + 30)

# =========================================================
# 6. ANIMATION ENGINE (FAST BLIT)
# =========================================================
def update_sim(frame):
    active_count = 0
    
    for i in range(num_drones):
        tl = timelines[i]
        trails[i].set_data(tl['x'][:frame+1], tl['y'][:frame+1])
        markers[i].set_data([tl['x'][frame]], [tl['y'][frame]])
        
        if tl['active'][frame] and tl['status'][frame] != "LANDED/DONE":
            active_count += 1
            markers[i].set_alpha(1.0)
        else:
            markers[i].set_alpha(0.35) 
            
    global_time_mins = (frame / fps) / 60.0
    
    table_header = (
        f"=== GLOBAL LIVE SWARM TELEMETRY ===\n"
        f"Global Clock: {global_time_mins:.2f} mins | Active: {active_count}/{num_drones} Drones\n"
        f"-----------------------------------------------------\n"
        f"DRONE UNIT  | CURRENT STATUS   | BATTERY REMAINING   \n"
        f"-----------------------------------------------------"
    )
    
    table_rows = []
    for i in range(num_drones):
        status_str = timelines[i]['status'][frame].ljust(16)
        bat_str = f"{timelines[i]['bat'][frame]:.2f} mins left".ljust(18)
        table_rows.append(f"Drone #{i+1:<5} | {status_str} | {bat_str}")
        
    complete_table = table_header + "\n" + "\n".join(table_rows) + "\n-----------------------------------------------------"
    telemetry_box.set_text(complete_table)
    
    return trails + markers + [telemetry_box]

# ACCELERATION: interval lowered to 20ms for rapid screen updates
ani = FuncAnimation(fig, update_sim, frames=max_frames, interval=20, blit=True, repeat=False)
plt.show()