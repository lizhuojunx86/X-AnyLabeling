#!/usr/bin/env python3
"""
Auto-annotation script using X-AnyLabeling for cat keypoint detection
Continues from existing 447 annotations
"""

import json
import sys
import os
from pathlib import Path
import subprocess
import time

# Add X-AnyLabeling to path
sys.path.insert(0, '/Users/lizhuojun/Desktop/APP/kittycat/X-AnyLabeling')

# Configuration
DATASET_DIR = Path("/Users/lizhuojun/Desktop/APP/kittycat/ai_model_workspace/datasets")
IMAGE_DIR = DATASET_DIR / "images"
ANNOTATION_DIR = DATASET_DIR / "annotations"
XANYLABELING_DIR = Path("/Users/lizhuojun/Desktop/APP/kittycat/X-AnyLabeling")

# Keypoint names from the existing annotations
KEYPOINT_NAMES = [
    "nose", "left_eye", "right_eye", "left_ear_base", "left_ear_tip",
    "right_ear_base", "right_ear_tip", "neck", "left_shoulder",
    "right_shoulder", "left_elbow", "right_elbow", "left_paw_front",
    "right_paw_front", "tail_base", "tail_mid", "tail_tip"
]

def get_annotated_images():
    """Get list of already annotated images."""
    annotated = set()
    for json_file in ANNOTATION_DIR.glob("*_keypoints.json"):
        # Extract image name from annotation filename
        image_name = json_file.stem.replace("_keypoints", "") + ".jpg"
        annotated.add(image_name)
    return annotated

def get_remaining_images():
    """Get list of images that need annotation."""
    all_images = set(p.name for p in IMAGE_DIR.glob("*.jpg"))
    annotated = get_annotated_images()
    remaining = all_images - annotated
    return sorted(list(remaining))

def create_annotation_config():
    """Create configuration for X-AnyLabeling auto-annotation."""
    config = {
        "image_dir": str(IMAGE_DIR),
        "output_dir": str(ANNOTATION_DIR),
        "model_type": "yolov8n-pose",
        "model_path": "/Users/lizhuojun/Desktop/APP/kittycat/yolov8n-pose.onnx",
        "keypoint_names": KEYPOINT_NAMES,
        "auto_save": True,
        "batch_size": 10
    }
    
    config_path = XANYLABELING_DIR / "auto_config.json"
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)
    
    return config_path

def show_progress():
    """Display current annotation progress."""
    total_images = len(list(IMAGE_DIR.glob("*.jpg")))
    annotated_images = len(get_annotated_images())
    remaining_images = total_images - annotated_images
    
    print("\n" + "="*60)
    print("ANNOTATION PROGRESS REPORT")
    print("="*60)
    print(f"Total cat images:        {total_images}")
    print(f"Already annotated:       {annotated_images} ({annotated_images/total_images*100:.1f}%)")
    print(f"Remaining to annotate:   {remaining_images}")
    print("="*60)
    
    # Show sample of remaining images
    remaining = get_remaining_images()
    if remaining:
        print("\nNext images to annotate:")
        for img in remaining[:10]:
            print(f"  - {img}")
        if len(remaining) > 10:
            print(f"  ... and {len(remaining)-10} more")
    else:
        print("\n✓ All images have been annotated!")
    
    return annotated_images, remaining_images

def launch_xanylabeling_gui():
    """Launch X-AnyLabeling GUI for manual annotation."""
    print("\nLaunching X-AnyLabeling GUI...")
    print("Instructions:")
    print("1. Use the GUI to continue annotating cat keypoints")
    print("2. Load the pose estimation model from: /Users/lizhuojun/Desktop/APP/kittycat/yolov8n-pose.onnx")
    print("3. Use batch inference for faster annotation")
    print("4. Save annotations in JSON format")
    
    # Activate virtual environment and launch
    activate_cmd = f"source {XANYLABELING_DIR}/venv/bin/activate"
    launch_cmd = "python -m anylabeling.app"
    
    full_command = f"cd {XANYLABELING_DIR} && {activate_cmd} && {launch_cmd}"
    
    try:
        subprocess.run(full_command, shell=True, check=True, executable="/bin/bash")
    except KeyboardInterrupt:
        print("\n\nX-AnyLabeling closed.")
    except Exception as e:
        print(f"Error launching X-AnyLabeling: {e}")

def main():
    print("CAT IMAGE ANNOTATION SYSTEM")
    print("Using X-AnyLabeling for keypoint annotation")
    print("-" * 60)
    
    # Show current progress
    annotated, remaining = show_progress()
    
    if remaining == 0:
        print("\nAll images have been annotated! No further work needed.")
        return
    
    print("\n" + "="*60)
    print("ANNOTATION OPTIONS")
    print("="*60)
    print("1. Launch X-AnyLabeling GUI for manual annotation")
    print("2. View detailed progress report")
    print("3. Export annotation summary")
    print("4. Exit")
    
    choice = input("\nSelect option (1-4): ").strip()
    
    if choice == "1":
        launch_xanylabeling_gui()
        # Show updated progress after GUI closes
        print("\nUpdated progress:")
        show_progress()
    
    elif choice == "2":
        # Detailed progress report
        annotated_list = sorted(list(get_annotated_images()))
        print(f"\nAnnotated images ({len(annotated_list)}):")
        for i, img in enumerate(annotated_list, 1):
            print(f"{i:4d}. {img}")
    
    elif choice == "3":
        # Export summary
        summary = {
            "total_images": len(list(IMAGE_DIR.glob("*.jpg"))),
            "annotated": annotated,
            "remaining": remaining,
            "annotated_files": sorted(list(get_annotated_images())),
            "remaining_files": get_remaining_images()
        }
        
        summary_path = DATASET_DIR / "annotation_summary.json"
        with open(summary_path, 'w') as f:
            json.dump(summary, f, indent=2)
        
        print(f"\n✓ Summary exported to: {summary_path}")
    
    elif choice == "4":
        print("\nExiting...")
    
    else:
        print("\nInvalid option.")

if __name__ == "__main__":
    main()