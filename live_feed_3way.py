from signal_controller_3way import start_signal_simulation_gui_3way
from ultralytics import YOLO
import cv2
import time
import csv
import os

model = YOLO('yolov8n.pt')

def detect_vehicles_from_video(video_path, direction, duration=10):
    cap = cv2.VideoCapture(video_path)
    start_time = time.time()
    tracked_ids = set()
    model.track(persist=True, tracker="bytetrack.yaml")

    while True:
        if time.time() - start_time > duration:
            break
        ret, frame = cap.read()
        if not ret:
            break

        results = model.track(frame, persist=True)[0]

        for box in results.boxes:
            cls_id = int(box.cls[0])
            label = model.names[cls_id]
            if label in ['car', 'bus', 'truck', 'motorbike', 'motorcycle', 'bicycle', 'scooter', 'van']:
                if hasattr(box, 'id') and box.id is not None:
                    tracked_ids.add(int(box.id))

        annotated = results.plot()
        cv2.imshow(f"{direction.upper()} Lane Detection", annotated)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    return len(tracked_ids)

def log_vehicle_counts_3way(vehicle_counts):
    os.makedirs("results", exist_ok=True)
    log_path = os.path.join("results", "vehicle_log_3way.csv")

    if not os.path.isfile(log_path):
        with open(log_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Direction", "Vehicle Count", "Timestamp"])

    with open(log_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        for direction, count in vehicle_counts.items():
            writer.writerow([direction, count, timestamp])

    print("✅ Vehicle counts logged successfully.")

def start_yolov8_traffic_feed_3way(video_paths, callback=None):
    if len(video_paths) != 3:
        print("❌ Error: Exactly 3 videos required for 3-way system")
        return

    directions = ["direction1", "direction2", "direction3"]
    vehicle_counts = {}
    display_duration = 10

    for direction, path in zip(directions, video_paths):
        print(f"\n🚦 Detecting traffic in {direction.upper()}...")
        count = detect_vehicles_from_video(path, direction, duration=display_duration)
        vehicle_counts[direction] = count
        print(f"✅ {direction.upper()}: {count} unique vehicles detected")

    # ✅ Log vehicle counts to CSV
    log_vehicle_counts_3way(vehicle_counts)

    if callback:
        callback(vehicle_counts)
    else:
        start_signal_simulation_gui_3way(vehicle_counts)
