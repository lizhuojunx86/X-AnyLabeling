#!/usr/bin/env python3
import time
import json
from pathlib import Path
from datetime import datetime

def monitor():
    workspace = Path("/Users/lizhuojun/Desktop/APP/kittycat/X-AnyLabeling/workspace")
    new_annotations = workspace / "new_annotations"
    current_batch = workspace / "current_batch"
    
    print("\n🔍 MONITORING ANNOTATION PROGRESS...")
    print("Press Ctrl+C to stop monitoring\n")
    
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
            print(f"\r⏰ {datetime.now().strftime('%H:%M:%S')} | "
                  f"📝 New annotations: {new_count} | "
                  f"📊 Batch progress: {new_count}/{batch_images} | "
                  f"⚡ Rate: {rate:.1f}/min", end="", flush=True)
            
            time.sleep(2)
            
        except KeyboardInterrupt:
            print("\n\n✅ Monitoring stopped")
            break

if __name__ == "__main__":
    monitor()
