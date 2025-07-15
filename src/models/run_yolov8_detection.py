from ultralytics import YOLO
import json
import os
import cv2
import logging
from datetime import datetime
from ultralytics.nn.tasks import DetectionModel
from torch.nn import Sequential

import torch

torch.serialization.add_safe_globals([
    DetectionModel,
    Sequential,
])

# Setup logging
log_format = "[%(levelname)s] %(asctime)s - %(message)s"
logging.basicConfig(format=log_format, level=logging.INFO)

logging.info(" Starting YOLOv8 inference script...")

# Load YOLOv8 model
model = YOLO('yolov8l.pt')  # Switch to 'yolov8x.pt' for better detection
logging.info("✅ YOLOv8 model loaded")

# Load message index
index_path = '../../data/raw/media_index_2025-07-12.json'
try:
    with open(index_path, 'r') as f:
        index_data = json.load(f)
    logging.info(f"📄 Loaded message index from {index_path} with {len(index_data)} entries")
except Exception as e:
    logging.error(f"❌ Failed to load index file: {e}")
    exit(1)

# Output setup
output_json_path = '../../data/processed/media_detection_results.json'
bounding_dir = '../../data/processed/annotated'
os.makedirs(bounding_dir, exist_ok=True)

results = []

for entry in index_data:
    image_path = os.path.join("../../", entry["image_path"])
    message_id = entry["message_id"]
    channel = entry["channel_name"]
    filename = os.path.basename(image_path)

    logging.info(f"🔍 Processing image: {filename} (message_id={message_id})")

    if not os.path.isfile(image_path):
        logging.warning(f"⚠️ Image not found: {image_path}")
        continue

    try:
        result = model(image_path)[0]
        boxes = result.boxes

        # Save annotated image
        imarray = result.plot()
        annotated_path = os.path.join(bounding_dir, f"processed_{filename}")
        cv2.imwrite(annotated_path, imarray)
        logging.info(f"📸 Saved annotated image to {annotated_path}")

        # Extract detections
        image_detections = []
        for box in boxes:
            cls = int(box.cls[0])
            conf = float(box.conf[0])
            label = model.names[cls]

            image_detections.append({
                "label": label,
                "confidence": round(conf, 3)
            })

        results.append({
            "message_id": message_id,
            "channel_name": channel,
            "image_path": image_path,
            "detections": image_detections
        })

    except Exception as e:
        logging.error(f"❌ Error during detection: {e}")

logging.info("✅ Finished YOLOv8 inference script")
logging.info(f"📄 Saving detection result for {len(results)} images")

# Save all results
try:
    with open(output_json_path, 'w') as f:
        json.dump(results, f, indent=2)
    logging.info(f"✅ Saved full detection results to {output_json_path}")
except Exception as e:
    logging.error(f"❌ Failed to write JSON output: {e}")