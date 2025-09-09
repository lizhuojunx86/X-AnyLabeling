#!/usr/bin/env python3
"""
Demo annotation progress using YOLO model
Shows how annotations would progress with X-AnyLabeling
"""

import os
import sys
import json
import time
import random
from pathlib import Path
from datetime import datetime

class AnnotationDemo:
    def __init__(self):
        self.base_dir = Path("/Users/lizhuojun/Desktop/APP/kittycat")
        self.workspace_dir = self.base_dir / "X-AnyLabeling" / "workspace"
        self.batch_dir = self.workspace_dir / "current_batch"
        self.demo_annotations_dir = self.workspace_dir / "demo_annotations"
        self.demo_annotations_dir.mkdir(exist_ok=True)
        
        # Keypoint template
        self.keypoint_names = [
            "nose", "left_eye", "right_eye", "left_ear_base", "left_ear_tip",
            "right_ear_base", "right_ear_tip", "neck", "left_shoulder",
            "right_shoulder", "left_elbow", "right_elbow", "left_paw_front",
            "right_paw_front", "tail_base", "tail_mid", "tail_tip"
        ]
        
    def simulate_annotation(self, image_path):
        """Simulate annotation for an image (as X-AnyLabeling would do)"""
        # Generate mock keypoints (in real X-AnyLabeling, this would come from YOLO model)
        keypoints = []
        for kp_name in self.keypoint_names:
            keypoints.append({
                "name": kp_name,
                "x": random.randint(100, 400),
                "y": random.randint(100, 400),
                "visible": 1 if random.random() > 0.1 else 0
            })
        
        # Create annotation structure
        annotation = {
            "image_id": image_path.name,
            "annotations": {
                "bbox": [random.randint(50, 150), random.randint(50, 150), 
                        random.randint(200, 300), random.randint(200, 300)],
                "keypoints": keypoints,
                "behavior_label": "unknown",
                "mood_label": "unknown"
            },
            "timestamp": datetime.now().isoformat(),
            "source": "X-AnyLabeling_demo"
        }
        
        return annotation
    
    def run_demo(self):
        """Run annotation demo showing progress"""
        print("\n" + "="*70)
        print("🤖 X-ANYLABELING ANNOTATION DEMO")
        print("="*70)
        print("\nThis demonstrates how X-AnyLabeling would process your images")
        print("with the YOLO pose model for automatic keypoint detection.\n")
        
        # Get images from batch
        images = list(self.batch_dir.glob("*.jpg"))
        
        if not images:
            print("❌ No images in batch directory. Run option 1 first.")
            return
        
        print(f"📦 Found {len(images)} images in batch")
        print("🚀 Starting automatic annotation...\n")
        
        # Progress bar setup
        total = len(images)
        start_time = time.time()
        
        for i, img_path in enumerate(images, 1):
            # Simulate annotation
            annotation = self.simulate_annotation(img_path)
            
            # Save annotation
            output_file = self.demo_annotations_dir / f"{img_path.stem}_keypoints.json"
            with open(output_file, 'w') as f:
                json.dump(annotation, f, indent=2)
            
            # Calculate progress
            progress = i / total * 100
            elapsed = time.time() - start_time
            rate = i / elapsed if elapsed > 0 else 0
            eta = (total - i) / rate if rate > 0 else 0
            
            # Display progress bar
            bar_length = 40
            filled = int(bar_length * i / total)
            bar = '█' * filled + '░' * (bar_length - filled)
            
            print(f"\r[{bar}] {progress:.1f}% | "
                  f"📝 {i}/{total} | "
                  f"⚡ {rate:.1f} img/s | "
                  f"⏱️ ETA: {eta:.0f}s", end="", flush=True)
            
            # Small delay to simulate processing
            time.sleep(0.2)
        
        print("\n\n✅ Demo annotation complete!")
        print(f"📁 Demo annotations saved to: {self.demo_annotations_dir}")
        print(f"⏱️ Total time: {time.time() - start_time:.1f} seconds")
        
        # Show sample annotation
        print("\n📋 Sample annotation structure:")
        sample_file = list(self.demo_annotations_dir.glob("*.json"))[0]
        with open(sample_file) as f:
            sample = json.load(f)
        
        print(f"Image: {sample['image_id']}")
        print(f"Keypoints detected: {len(sample['annotations']['keypoints'])}")
        print(f"First 3 keypoints:")
        for kp in sample['annotations']['keypoints'][:3]:
            print(f"  - {kp['name']}: ({kp['x']}, {kp['y']}) visible={kp['visible']}")

def show_real_progress():
    """Show actual progress including existing annotations"""
    base_dir = Path("/Users/lizhuojun/Desktop/APP/kittycat")
    dataset_dir = base_dir / "ai_model_workspace" / "datasets"
    
    print("\n" + "="*70)
    print("📊 REAL-TIME PROGRESS VISUALIZATION")
    print("="*70)
    
    # Count files
    existing = len(list((dataset_dir / "annotations").glob("*_keypoints.json")))
    backup = len(list((dataset_dir / "annotations_backup").glob("*.json")))
    total = len(list((dataset_dir / "images").glob("*.jpg")))
    new_annotations = len(list((base_dir / "X-AnyLabeling/workspace/new_annotations").glob("*.json")))
    demo_annotations = len(list((base_dir / "X-AnyLabeling/workspace/demo_annotations").glob("*.json")))
    
    # Progress bar for overall completion
    progress = existing / total * 100
    bar_length = 50
    filled = int(bar_length * existing / total)
    bar = '█' * filled + '░' * (bar_length - filled)
    
    print(f"\n📈 Overall Progress:")
    print(f"[{bar}] {progress:.1f}%")
    print(f"{existing}/{total} images annotated\n")
    
    print("📁 Annotation Distribution:")
    print(f"  ✅ Original annotations:  {existing:>5} files")
    print(f"  🔒 Backup annotations:     {backup:>5} files")
    print(f"  🆕 New annotations (safe): {new_annotations:>5} files")
    print(f"  🧪 Demo annotations:       {demo_annotations:>5} files")
    
    # Estimate completion time
    remaining = total - existing
    if remaining > 0:
        print(f"\n⏱️ Time Estimates (at different speeds):")
        print(f"  Manual (1 img/min):     {remaining/60:.1f} hours")
        print(f"  Semi-auto (5 img/min):  {remaining/300:.1f} hours")
        print(f"  Auto YOLO (30 img/min): {remaining/1800:.1f} hours")
    
    # Show next batch to annotate
    all_images = set(p.name for p in (dataset_dir / "images").glob("*.jpg"))
    annotated_names = set(f.stem.replace("_keypoints", "") + ".jpg" 
                         for f in (dataset_dir / "annotations").glob("*_keypoints.json"))
    unannotated = sorted(list(all_images - annotated_names))[:5]
    
    print(f"\n📝 Next images to annotate:")
    for img in unannotated:
        print(f"  - {img}")

def main():
    print("\n" + "="*70)
    print("🎯 ANNOTATION PROGRESS DEMONSTRATION")
    print("="*70)
    
    print("\n1. Run annotation demo (simulates X-AnyLabeling)")
    print("2. Show real-time progress")
    print("3. Exit")
    
    choice = input("\nSelect option (1-3): ").strip()
    
    if choice == "1":
        demo = AnnotationDemo()
        demo.run_demo()
        show_real_progress()
    elif choice == "2":
        show_real_progress()
    elif choice == "3":
        print("Exiting...")
    else:
        print("Invalid option")

if __name__ == "__main__":
    main()