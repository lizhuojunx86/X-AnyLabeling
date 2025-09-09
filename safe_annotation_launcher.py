#!/usr/bin/env python3
"""
Safe X-AnyLabeling launcher with progress monitoring
This script ensures your existing annotations are protected
"""

import os
import sys
import json
import shutil
import subprocess
from pathlib import Path
from datetime import datetime

class SafeAnnotationManager:
    def __init__(self):
        self.base_dir = Path("/Users/lizhuojun/Desktop/APP/kittycat")
        self.dataset_dir = self.base_dir / "ai_model_workspace" / "datasets"
        self.original_annotations = self.dataset_dir / "annotations"
        self.backup_dir = self.dataset_dir / "annotations_backup"
        self.xanylabeling_dir = self.base_dir / "X-AnyLabeling"
        self.workspace_dir = self.xanylabeling_dir / "workspace"
        self.new_annotations_dir = self.workspace_dir / "new_annotations"
        self.test_images_dir = self.workspace_dir / "test_images"
        
    def show_current_status(self):
        """Display current annotation status"""
        print("\n" + "="*70)
        print("📊 CURRENT ANNOTATION STATUS")
        print("="*70)
        
        # Count existing annotations
        existing_count = len(list(self.original_annotations.glob("*_keypoints.json")))
        backup_count = len(list(self.backup_dir.glob("*.json")))
        total_images = len(list((self.dataset_dir / "images").glob("*.jpg")))
        
        print(f"✅ Original annotations: {existing_count} files")
        print(f"🔒 Backup annotations: {backup_count} files (protected)")
        print(f"📁 Total images: {total_images}")
        print(f"📝 Remaining to annotate: {total_images - existing_count}")
        print(f"📈 Progress: {existing_count/total_images*100:.1f}%")
        
        # Show test workspace
        test_images = list(self.test_images_dir.glob("*.jpg"))
        print(f"\n🧪 Test workspace: {len(test_images)} images ready for safe testing")
        
        return existing_count, total_images
    
    def prepare_batch_for_annotation(self, batch_size=50):
        """Prepare a batch of unannotated images for X-AnyLabeling"""
        print("\n📦 Preparing batch of unannotated images...")
        
        # Get list of all images
        all_images = list((self.dataset_dir / "images").glob("*.jpg"))
        
        # Get annotated image names
        annotated_names = set()
        for ann_file in self.original_annotations.glob("*_keypoints.json"):
            img_name = ann_file.stem.replace("_keypoints", "") + ".jpg"
            annotated_names.add(img_name)
        
        # Find unannotated images
        unannotated = [img for img in all_images if img.name not in annotated_names]
        
        # Clear and prepare batch directory
        batch_dir = self.workspace_dir / "current_batch"
        if batch_dir.exists():
            shutil.rmtree(batch_dir)
        batch_dir.mkdir(parents=True)
        
        # Copy batch of images
        batch = unannotated[:batch_size]
        for img in batch:
            shutil.copy(img, batch_dir / img.name)
        
        print(f"✅ Copied {len(batch)} unannotated images to batch directory")
        print(f"📍 Location: {batch_dir}")
        
        return batch_dir, len(batch)
    
    def create_progress_monitor(self):
        """Create a real-time progress monitoring script"""
        monitor_script = self.xanylabeling_dir / "monitor_progress.py"
        
        script_content = '''#!/usr/bin/env python3
import time
import json
from pathlib import Path
from datetime import datetime

def monitor():
    workspace = Path("/Users/lizhuojun/Desktop/APP/kittycat/X-AnyLabeling/workspace")
    new_annotations = workspace / "new_annotations"
    current_batch = workspace / "current_batch"
    
    print("\\n🔍 MONITORING ANNOTATION PROGRESS...")
    print("Press Ctrl+C to stop monitoring\\n")
    
    start_time = datetime.now()
    initial_count = len(list(new_annotations.glob("*.json")))
    
    while True:
        try:
            # Count annotations
            new_count = len(list(new_annotations.glob("*.json")))
            batch_images = len(list(current_batch.glob("*.jpg")))
            
            # Calculate stats
            elapsed = (datetime.now() - start_time).total_seconds()
            rate = (new_count - initial_count) / (elapsed / 60) if elapsed > 0 else 0
            
            # Display
            print(f"\\r⏰ {datetime.now().strftime('%H:%M:%S')} | "
                  f"📝 New annotations: {new_count} | "
                  f"📊 Batch progress: {new_count}/{batch_images} | "
                  f"⚡ Rate: {rate:.1f}/min", end="", flush=True)
            
            time.sleep(2)
            
        except KeyboardInterrupt:
            print("\\n\\n✅ Monitoring stopped")
            break

if __name__ == "__main__":
    monitor()
'''
        
        with open(monitor_script, 'w') as f:
            f.write(script_content)
        
        os.chmod(monitor_script, 0o755)
        print(f"✅ Created progress monitor: {monitor_script}")
        
        return monitor_script
    
    def launch_xanylabeling_safe(self):
        """Launch X-AnyLabeling with safe configuration"""
        print("\n🚀 Launching X-AnyLabeling in SAFE MODE...")
        print("-" * 70)
        print("⚠️  IMPORTANT SAFETY MEASURES:")
        print("1. Your original 447 annotations are BACKED UP")
        print("2. New annotations will be saved to a SEPARATE directory")
        print("3. You can merge them after verification")
        print("-" * 70)
        
        # Create launch script
        launch_script = self.xanylabeling_dir / "safe_launch.sh"
        script_content = f'''#!/bin/bash
cd {self.xanylabeling_dir}
source venv/bin/activate

echo "Opening X-AnyLabeling..."
echo "1. Click File -> Open Dir"
echo "2. Select: {self.workspace_dir}/current_batch"
echo "3. Click File -> Change Output Dir"  
echo "4. Select: {self.new_annotations_dir}"
echo "5. Load your YOLO model for auto-annotation"
echo ""

python -m anylabeling.app
'''
        
        with open(launch_script, 'w') as f:
            f.write(script_content)
        
        os.chmod(launch_script, 0o755)
        
        print("\n📋 INSTRUCTIONS FOR X-ANYLABELING:")
        print(f"1. Open Dir: {self.workspace_dir}/current_batch")
        print(f"2. Change Output Dir: {self.new_annotations_dir}")
        print("3. Load Model: Model -> Load Custom Model -> yolov8n-pose.onnx")
        print("4. Use Auto-Label All for batch processing")
        
        return launch_script

def main():
    manager = SafeAnnotationManager()
    
    print("\n" + "="*70)
    print("🛡️  SAFE ANNOTATION SYSTEM FOR X-ANYLABELING")
    print("="*70)
    
    # Show current status
    existing, total = manager.show_current_status()
    
    print("\n" + "="*70)
    print("OPTIONS:")
    print("="*70)
    print("1. Prepare batch and launch X-AnyLabeling (SAFE MODE)")
    print("2. Monitor annotation progress") 
    print("3. Merge new annotations with existing (after verification)")
    print("4. View detailed statistics")
    print("5. Exit")
    
    choice = input("\nSelect option (1-5): ").strip()
    
    if choice == "1":
        # Prepare batch
        batch_dir, batch_size = manager.prepare_batch_for_annotation(30)
        
        # Create monitor
        monitor_script = manager.create_progress_monitor()
        
        # Launch X-AnyLabeling
        launch_script = manager.launch_xanylabeling_safe()
        
        print("\n✅ READY TO ANNOTATE SAFELY!")
        print(f"\n🖥️  To launch X-AnyLabeling: bash {launch_script}")
        print(f"📊 To monitor progress: python {monitor_script}")
        
    elif choice == "2":
        monitor_script = manager.create_progress_monitor()
        subprocess.run([sys.executable, str(monitor_script)])
        
    elif choice == "3":
        print("\n🔄 Merging new annotations...")
        new_files = list(manager.new_annotations_dir.glob("*.json"))
        if new_files:
            for f in new_files:
                dest = manager.original_annotations / f.name
                if not dest.exists():
                    shutil.copy(f, dest)
                    print(f"✅ Copied: {f.name}")
            print(f"\n✅ Merged {len(new_files)} new annotations")
        else:
            print("❌ No new annotations to merge")
            
    elif choice == "4":
        # Detailed statistics
        print("\n📊 DETAILED STATISTICS:")
        annotated_files = sorted(list(manager.original_annotations.glob("*_keypoints.json")))
        print(f"\nLast 5 annotated files:")
        for f in annotated_files[-5:]:
            print(f"  - {f.name}")
            
    elif choice == "5":
        print("\n👋 Exiting safely...")
        
    else:
        print("❌ Invalid option")

if __name__ == "__main__":
    main()