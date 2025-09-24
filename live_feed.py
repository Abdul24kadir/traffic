# def start_live_traffic_feed(*args):
#     import cv2
#     import os
#     import numpy as np

#     # Absolute paths to config, weights, and classes
#     config_path = r"C:\Users\abdul\OneDrive\Desktop\batch c2 zip\Batch C2\MSPC31Density Based Smart Traffic Control System\yolo-cfg\yolov4-tiny.cfg"
#     weights_path = r"C:\Users\abdul\OneDrive\Desktop\batch c2 zip\Batch C2\MSPC31Density Based Smart Traffic Control System\yolo-cfg\yolov4-tiny.weights"
#     names_path = r"C:\Users\abdul\OneDrive\Desktop\batch c2 zip\Batch C2\MSPC31Density Based Smart Traffic Control System\yolo-cfg\coco.names"

#     # Load YOLO network
#     net = cv2.dnn.readNet(weights_path, config_path)
#     net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
#     net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

#     # Load class labels
#     with open(names_path, "r") as f:
#         classes = [line.strip() for line in f.readlines()]

#     layer_names = net.getLayerNames()
#     output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers().flatten()]

#     # Use video file if provided, else webcam
#     video_path = args[0] if args else None
#     if video_path and os.path.isfile(video_path):
#         cap = cv2.VideoCapture(video_path)
#         print(f"Using video file: {video_path}")
#     else:
#         cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
#         print("Using webcam")

#     while True:
#         ret, frame = cap.read()
#         if not ret:
#             break

#         height, width = frame.shape[:2]

#         # Higher size for better detection (e.g., 608x608 or 640x640)
#         blob = cv2.dnn.blobFromImage(frame, 1 / 255.0, (640, 640), swapRB=True, crop=False)
#         net.setInput(blob)
#         outs = net.forward(output_layers)

#         class_ids = []
#         confidences = []
#         boxes = []

#         # Target vehicle-related classes
#         vehicle_labels = ["car", "bus", "truck", "motorbike", "motorcycle", "bicycle", "scooter", "van"]

#         for out in outs:
#             for detection in out:
#                 scores = detection[5:]
#                 class_id = int(np.argmax(scores))
#                 confidence = scores[class_id]

#                 if confidence > 0.3 and classes[class_id] in vehicle_labels:
#                     center_x = int(detection[0] * width)
#                     center_y = int(detection[1] * height)
#                     w = int(detection[2] * width)
#                     h = int(detection[3] * height)
#                     x = int(center_x - w / 2)
#                     y = int(center_y - h / 2)

#                     boxes.append([x, y, w, h])
#                     confidences.append(float(confidence))
#                     class_ids.append(class_id)

#         indexes = cv2.dnn.NMSBoxes(boxes, confidences, score_threshold=0.3, nms_threshold=0.4)
#         vehicle_count = 0

#         if len(indexes) > 0:
#             for i in indexes.flatten():
#                 x, y, w, h = boxes[i]
#                 label = f"{classes[class_ids[i]]}: {int(confidences[i] * 100)}%"
#                 cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
#                 cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
#                 vehicle_count += 1

#         # Display total count
#         cv2.putText(frame, f"Vehicles: {vehicle_count}", (10, 30),
#                     cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

#         # Show frame
#         cv2.imshow("YOLOv4-tiny Vehicle Detection", frame)
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break

#     cap.release()
#     cv2.destroyAllWindows()
# from signal_controller import calculate_green_time, start_signal_simulation_gui
# from ultralytics import YOLO
# import cv2
# import time

# # Load YOLOv8 model
# model = YOLO('yolov8n.pt')


# def start_single_video_feed(source, callback=None):
#     cap = cv2.VideoCapture(0 if source == "0" or source == 0 else source)
#     print("🎥 Using webcam" if source == "0" or source == 0 else f"📼 Using video file: {source}")

#     tracked_ids = set()
#     model.track(persist=True, tracker="bytetrack.yaml")

#     while True:
#         ret, frame = cap.read()
#         if not ret:
#             break

#         results = model.track(frame, persist=True)[0]

#         for box in results.boxes:
#             cls_id = int(box.cls[0])
#             label = model.names[cls_id]
#             if label in ['car', 'bus', 'truck', 'motorbike', 'motorcycle', 'bicycle', 'scooter', 'van']:
#                 if hasattr(box, 'id') and box.id is not None:
#                     tracked_ids.add(int(box.id))

#         total_count = len(tracked_ids)
#         annotated_frame = results.plot()
#         cv2.imshow("Live Vehicle Detection", annotated_frame)

#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break

#     cap.release()
#     cv2.destroyAllWindows()

#     print(f"✅ Total unique vehicles detected: {total_count}")
#     if callback:
#         callback(total_count)


# def start_yolov8_traffic_feed(video_paths, callback=None):
#     if len(video_paths) != 4:
#         print("❌ Error: Exactly 4 videos required (east, west, north, south)")
#         return

#     lane_names = ["east", "west", "north", "south"]
#     vehicle_counts = {}
#     display_duration = 10  # seconds to detect from each video

#     for lane, path in zip(lane_names, video_paths):
#         print(f"\n🚦 Detecting traffic in {lane.upper()} lane...")
#         count = detect_vehicles_from_video(path, lane, duration=display_duration)
#         vehicle_counts[lane] = count
#         print(f"✅ {lane.upper()} lane: {count} unique vehicles detected")

#     if callback:
#         callback(vehicle_counts)
#     else:
#         start_signal_simulation_gui(vehicle_counts)


# def detect_vehicles_from_video(video_path, lane, duration=10):
#     cap = cv2.VideoCapture(video_path)
#     start_time = time.time()
#     tracked_ids = set()

#     model.track(persist=True, tracker="bytetrack.yaml")

#     while True:
#         if time.time() - start_time > duration:
#             break

#         ret, frame = cap.read()
#         if not ret:
#             break

#         results = model.track(frame, persist=True)[0]

#         for box in results.boxes:
#             cls_id = int(box.cls[0])
#             label = model.names[cls_id]
#             if label in ['car', 'bus', 'truck', 'motorbike', 'motorcycle', 'bicycle', 'scooter', 'van']:
#                 if hasattr(box, 'id') and box.id is not None:
#                     tracked_ids.add(int(box.id))

#         annotated = results.plot()
#         cv2.imshow(f"{lane.upper()} Lane Detection", annotated)
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break

#     cap.release()
#     cv2.destroyAllWindows()

#     return len(tracked_ids)
from signal_controller import calculate_green_time, start_signal_simulation_gui
from ultralytics import YOLO
import cv2
import time
import os
import csv

# Load YOLOv8 model
model = YOLO('yolov8n.pt')


def log_vehicle_count(lane, count, save_folder="results"):
    os.makedirs(save_folder, exist_ok=True)  # create folder if not exist
    log_path = os.path.join(save_folder, "vehicle_counts_log.csv")

    # Create file with header if it doesn't exist
    if not os.path.isfile(log_path):
        with open(log_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Lane", "Vehicle Count", "Timestamp"])

    # Append log entry
    with open(log_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([lane, count, time.strftime("%Y-%m-%d %H:%M:%S")])

    print(f"✅ Log saved for {lane.upper()} in {log_path}")


def start_single_video_feed(source, callback=None):
    cap = cv2.VideoCapture(0 if source == "0" or source == 0 else source)
    print("🎥 Using webcam" if source == "0" or source == 0 else f"📼 Using video file: {source}")

    tracked_ids = set()
    model.track(persist=True, tracker="bytetrack.yaml")

    while True:
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

        total_count = len(tracked_ids)
        annotated_frame = results.plot()
        cv2.imshow("Live Vehicle Detection", annotated_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    print(f"✅ Total unique vehicles detected: {total_count}")
    if callback:
        callback(total_count)


def start_yolov8_traffic_feed(video_paths, callback=None):
    if len(video_paths) != 4:
        print("❌ Error: Exactly 4 videos required (east, west, north, south)")
        return

    lane_names = ["east", "west", "north", "south"]
    vehicle_counts = {}
    display_duration = 10  # seconds to detect from each video

    for lane, path in zip(lane_names, video_paths):
        print(f"\n🚦 Detecting traffic in {lane.upper()} lane...")
        count = detect_vehicles_from_video(path, lane, duration=display_duration)
        vehicle_counts[lane] = count
        print(f"✅ {lane.upper()} lane: {count} unique vehicles detected")

        # Log the result
        log_vehicle_count(lane, count)

    if callback:
        callback(vehicle_counts)
    else:
        start_signal_simulation_gui(vehicle_counts)


def detect_vehicles_from_video(video_path, lane, duration=10):
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
        cv2.imshow(f"{lane.upper()} Lane Detection", annotated)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    return len(tracked_ids)
