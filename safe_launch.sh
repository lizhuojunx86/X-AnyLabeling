#!/bin/bash
cd /Users/lizhuojun/Desktop/APP/kittycat/X-AnyLabeling
source venv/bin/activate

echo "Opening X-AnyLabeling..."
echo "1. Click File -> Open Dir"
echo "2. Select: /Users/lizhuojun/Desktop/APP/kittycat/X-AnyLabeling/workspace/current_batch"
echo "3. Click File -> Change Output Dir"  
echo "4. Select: /Users/lizhuojun/Desktop/APP/kittycat/X-AnyLabeling/workspace/new_annotations"
echo "5. Load your YOLO model for auto-annotation"
echo ""

python -m anylabeling.app
