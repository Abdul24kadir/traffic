import os
from ultralytics import YOLO

# Get script's folder
base_path = os.path.dirname(__file__)
data_yaml = os.path.join(base_path, 'dataset', 'data.yaml')

# Load model
model = YOLO('yolov8n.pt')

# Train
model.train(data=data_yaml, epochs=50, batch=8, imgsz=640)
