"""
=============================================================
  YOLOv8 Instance Segmentation - Video Area Analyzer
  Trained on: BROKEN_TREES, DRY_AREA, PATHWAYS, ROOFTOPS,
              VEGETATION, WATERBODY, WATER_CLOGGING
=============================================================
  HOW TO USE:
  1. Run this script
  2. A file picker will open — select your video
  3. Wait for processing to finish
  4. An Excel file AND an Analyzed Video will be saved!
=============================================================
"""

import cv2
import numpy as np
import pandas as pd
from ultralytics import YOLO
from tkinter import Tk, filedialog, messagebox
import os
import time

# ─── CONFIG ────────────────────────────────────────────────
MODEL_PATH = r"C:\Users\agamj\Downloads\bas.v3i.yolov8 (2)\bas.v3i.yolov8\runs\segment\runs\yolov8s_seg_training\weights\best.pt"
CONFIDENCE = 0.35       # Minimum confidence threshold (0.0 - 1.0)
PROCESS_EVERY_N_FRAMES = 1  # Process every Nth frame to speed things up (1 = every frame)
# ───────────────────────────────────────────────────────────

CLASS_NAMES = [
    'BROKEN_TREES', 'DRY_AREA', 'PATHWAYS',
    'ROOFTOPS', 'VEGETATION', 'WATERBODY', 'WATER_CLOGGING'
]

def pick_video():
    """Open a file dialog to select a video file."""
    root = Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    video_path = filedialog.askopenfilename(
        title="Select a Video File",
        filetypes=[
            ("Video files", "*.mp4 *.avi *.mov *.mkv *.wmv *.flv *.webm"),
            ("All files", "*.*")
        ]
    )
    root.destroy()
    return video_path


def mask_to_area(mask, frame_h, frame_w):
    """Calculate pixel area from a binary mask."""
    if mask is None:
        return 0
    # Resize mask to frame size and count non-zero pixels
    mask_resized = cv2.resize(mask.astype(np.uint8), (frame_w, frame_h))
    return int(np.sum(mask_resized > 0))


def process_video(video_path, model):
    """Run inference on video, collect per-frame results, and save annotated video."""
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"ERROR: Cannot open video: {video_path}")
        return None, None

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    frame_area = frame_w * frame_h

    print(f"\n📹 Video: {os.path.basename(video_path)}")
    print(f"   Resolution : {frame_w} x {frame_h}")
    print(f"   FPS        : {fps:.1f}")
    print(f"   Total Frames: {total_frames}")
    print(f"   Processing every {PROCESS_EVERY_N_FRAMES} frame(s)")
    print(f"   Estimated frames to process: {total_frames // PROCESS_EVERY_N_FRAMES}\n")

    # ─── VIDEO WRITER SETUP ───
    video_dir = os.path.dirname(video_path)
    video_name = os.path.splitext(os.path.basename(video_path))[0]
    out_video_path = os.path.join(video_dir, f"{video_name}_analyzed.mp4")
    
    # Adjust output FPS so the skipped frames don't result in a fast-forward video
    out_fps = fps / PROCESS_EVERY_N_FRAMES
    fourcc = cv2.VideoWriter_fourcc(*'mp4v') # Codec for .mp4
    out_video = cv2.VideoWriter(out_video_path, fourcc, out_fps, (frame_w, frame_h))
    # ──────────────────────────

    rows = []
    frame_idx = 0
    processed = 0
    start_time = time.time()

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_idx += 1

        # Only process every Nth frame
        if frame_idx % PROCESS_EVERY_N_FRAMES != 0:
            continue

        processed += 1
        timestamp_sec = frame_idx / fps
        timestamp_str = time.strftime('%H:%M:%S', time.gmtime(timestamp_sec))

        # Run YOLOv8 inference
        results = model(frame, conf=CONFIDENCE, verbose=False)[0]

        # ─── DRAW AND SAVE FRAME ───
        # .plot() draws the segmentation masks and bounding boxes onto the frame
        annotated_frame = results.plot()
        out_video.write(annotated_frame)
        # ───────────────────────────

        # Build a base row with all classes at 0
        base = {
            'Frame': frame_idx,
            'Timestamp': timestamp_str,
            'Timestamp_sec': round(timestamp_sec, 2),
            'Frame_Width_px': frame_w,
            'Frame_Height_px': frame_h,
            'Frame_Total_Area_px2': frame_area,
        }
        for cls in CLASS_NAMES:
            base[f'{cls}_instances'] = 0
            base[f'{cls}_area_px2'] = 0
            base[f'{cls}_area_pct'] = 0.0

        # Fill in detections if any masks exist
        if results.masks is not None:
            masks = results.masks.data.cpu().numpy()  # (N, H, W)
            classes = results.boxes.cls.cpu().numpy().astype(int)
            confs = results.boxes.conf.cpu().numpy()

            for mask, cls_id, conf in zip(masks, classes, confs):
                cls_name = CLASS_NAMES[cls_id]
                area = mask_to_area(mask, frame_h, frame_w)
                base[f'{cls_name}_instances'] += 1
                base[f'{cls_name}_area_px2'] += area

        # Calculate percentages
        for cls in CLASS_NAMES:
            area = base[f'{cls}_area_px2']
            base[f'{cls}_area_pct'] = round((area / frame_area) * 100, 3)

        rows.append(base)

        # Progress print
        elapsed = time.time() - start_time
        frames_left = (total_frames // PROCESS_EVERY_N_FRAMES) - processed
        eta = (elapsed / processed * frames_left) if processed > 0 else 0
        print(f"   ✅ Frame {frame_idx:>5}/{total_frames}  |  "
              f"Time: {timestamp_str}  |  "
              f"ETA: {int(eta)}s remaining", end='\r')

    cap.release()
    out_video.release() # Close the video writer
    print(f"\n\n✅ Done! Processed {processed} frames in {int(time.time()-start_time)}s.\n")
    return rows, out_video_path


def save_to_excel(rows, video_path):
    """Save results to a nicely formatted Excel file."""
    df = pd.DataFrame(rows)

    # ── Summary sheet: total area per class across entire video ──
    summary_data = []
    for cls in CLASS_NAMES:
        total_area = df[f'{cls}_area_px2'].sum()
        avg_pct = df[f'{cls}_area_pct'].mean()
        max_pct = df[f'{cls}_area_pct'].max()
        total_instances = df[f'{cls}_instances'].sum()
        summary_data.append({
            'Class': cls,
            'Total Instances Detected': int(total_instances),
            'Total Area (px²)': int(total_area),
            'Average Coverage (%)': round(avg_pct, 3),
            'Peak Coverage (%)': round(max_pct, 3),
        })
    summary_df = pd.DataFrame(summary_data).sort_values('Total Area (px²)', ascending=False)

    # ── Output path: same folder as video ──
    video_dir = os.path.dirname(video_path)
    video_name = os.path.splitext(os.path.basename(video_path))[0]
    excel_path = os.path.join(video_dir, f"{video_name}_area_analysis.xlsx")

    with pd.ExcelWriter(excel_path, engine='openpyxl') as writer:
        # Sheet 1: Summary
        summary_df.to_excel(writer, sheet_name='Summary', index=False)

        # Sheet 2: Full per-frame data
        df.to_excel(writer, sheet_name='Per-Frame Data', index=False)

        # Sheet 3: Compact view (just area % per class per frame)
        compact_cols = ['Frame', 'Timestamp'] + [f'{cls}_area_pct' for cls in CLASS_NAMES]
        compact_df = df[compact_cols].copy()
        compact_df.columns = ['Frame', 'Timestamp'] + CLASS_NAMES
        compact_df.to_excel(writer, sheet_name='Coverage % per Frame', index=False)

        # Auto-fit column widths
        for sheet_name in writer.sheets:
            ws = writer.sheets[sheet_name]
            for col in ws.columns:
                max_len = max(len(str(cell.value or '')) for cell in col)
                ws.column_dimensions[col[0].column_letter].width = min(max_len + 4, 40)

    return excel_path


def main():
    print("=" * 60)
    print("  YOLOv8 Segmentation - Video Area Analyzer")
    print("=" * 60)

    # 1. Pick video
    print("\n📂 Opening file picker... (select your video)")
    video_path = pick_video()
    if not video_path:
        print("❌ No video selected. Exiting.")
        return

    # 2. Load model
    print(f"\n🤖 Loading trained model from:\n   {MODEL_PATH}\n")
    if not os.path.exists(MODEL_PATH):
        print(f"❌ ERROR: Model not found at {MODEL_PATH}")
        print("   Make sure training has completed and best.pt exists!")
        return
    model = YOLO(MODEL_PATH)
    print("✅ Model loaded successfully!\n")

    # 3. Process video
    rows, out_video_path = process_video(video_path, model)
    if not rows:
        print("❌ No frames processed. Check your video file.")
        return

    # 4. Save Excel
    print("💾 Saving Excel file...")
    excel_path = save_to_excel(rows, video_path)
    
    print(f"✅ Excel saved to:\n   {excel_path}")
    print(f"✅ Video saved to:\n   {out_video_path}\n")

    # 5. Done popup
    root = Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    messagebox.showinfo(
        "Done! ✅",
        f"Analysis complete!\n\n"
        f"📊 Excel file saved to:\n{excel_path}\n\n"
        f"🎬 Analyzed video saved to:\n{out_video_path}\n\n"
        f"Sheets inside Excel:\n"
        f"  1. Summary - Total area per class\n"
        f"  2. Per-Frame Data - Full raw data\n"
        f"  3. Coverage % per Frame - Clean compact view"
    )
    root.destroy()

    print("=" * 60)
    print("  All done! Open the Excel file and Video to view your results.")
    print("=" * 60)


if __name__ == '__main__':
    main()
