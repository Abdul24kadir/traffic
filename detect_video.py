##without saving 
import cv2
from ultralytics import YOLO
from tkinter import Tk, filedialog, messagebox
import time
from datetime import datetime
import csv
import os

# Initialize and hide tkinter window
root = Tk()
root.withdraw()

# Prompt to select 4 video files
video_paths = filedialog.askopenfilenames(
    title="Select 4 Video Files (One per Direction: East, West, North, South)",
    filetypes=[("MP4 files", "*.mp4"), ("All files", "*.*")]
)

if len(video_paths) != 4:
    messagebox.showerror("Error", "Please select exactly 4 video files.")
    exit()

# Load YOLO model
model = YOLO('runs/detect/train2/weights/best.pt')
confidence_threshold = 0.89
detection_duration = 10  # seconds

# Directions and results
directions = ['East', 'West', 'North', 'South']
ambulance_detected = {dir: False for dir in directions}

# Ensure 'results' folder exists
results_folder = "results"
os.makedirs(results_folder, exist_ok=True)

# CSV file path inside results folder
csv_file = os.path.join(results_folder, "ambulance_detection_log.csv")

# Create CSV file with headers if it doesn't exist
if not os.path.exists(csv_file):
    with open(csv_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["detectionID", "timestamp", "confidenceScore", "direction"])

def log_detection(confidence, direction):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Calculate detectionID as current number of lines in file (excluding header)
    with open(csv_file, 'r') as file:
        row_count = sum(1 for row in file) - 1  # exclude header

    detection_id = row_count + 1

    with open(csv_file, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([detection_id, timestamp, confidence, direction])

def detect_ambulance(video_path, direction):
    cap = cv2.VideoCapture(video_path)
    start_time = time.time()

    window_name = f'{direction} - YOLO Ambulance Detection'
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(window_name, 640, 360)

    while True:
        ret, frame = cap.read()
        if not ret or time.time() - start_time >= detection_duration:
            break

        results = model(frame)[0]

        for box in results.boxes:
            conf = box.conf[0].item()
            if conf >= confidence_threshold:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                cls = int(box.cls[0].item())
                label = model.names[cls]

                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, f'{label} {conf:.2f}', (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

                if label.lower() == "ambulance":
                    ambulance_detected[direction] = True
                    log_detection(conf, direction)

        cv2.imshow(window_name, frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyWindow(window_name)

# Run detection for each direction
for path, direction in zip(video_paths, directions):
    detect_ambulance(path, direction)

# Show results
priority_directions = [dir for dir, detected in ambulance_detected.items() if detected]

if not priority_directions:
    messagebox.showinfo("Ambulance Priority", "No ambulance detected.")
elif len(priority_directions) == 1:
    messagebox.showinfo("Ambulance Priority", f"Ambulance detected in the {priority_directions[0]} direction. Give green signal.")
else:
    joined_dirs = ', '.join(priority_directions[:-1]) + f' and {priority_directions[-1]}'
    messagebox.showinfo("Ambulance Priority", f"Ambulance detected in {joined_dirs} directions. Give green signal.")


##with saving :
# import cv2
# from ultralytics import YOLO
# from tkinter import Tk, filedialog, messagebox
# import time
# from datetime import datetime
# import csv
# import os

# # Initialize and hide tkinter window
# root = Tk()
# root.withdraw()

# # Prompt to select 4 video files
# video_paths = filedialog.askopenfilenames(
#     title="Select 4 Video Files (One per Direction: East, West, North, South)",
#     filetypes=[("MP4 files", "*.mp4"), ("All files", "*.*")]
# )

# if len(video_paths) != 4:
#     messagebox.showerror("Error", "Please select exactly 4 video files.")
#     exit()

# # Load YOLO model
# model = YOLO('runs/detect/train2/weights/best.pt')
# confidence_threshold = 0.89
# detection_duration = 10  # seconds

# # Directions and results
# directions = ['East', 'West', 'North', 'South']
# ambulance_detected = {dir: False for dir in directions}

# # Ensure 'results' folder exists
# results_folder = "results"
# os.makedirs(results_folder, exist_ok=True)

# # CSV file path inside results folder
# csv_file = os.path.join(results_folder, "ambulance_detection_log.csv")

# # Create CSV file with headers if it doesn't exist
# if not os.path.exists(csv_file):
#     with open(csv_file, mode='w', newline='') as file:
#         writer = csv.writer(file)
#         writer.writerow(["detectionID", "timestamp", "confidenceScore", "direction"])

# def log_detection(confidence, direction):
#     timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#     with open(csv_file, 'r') as file:
#         row_count = sum(1 for row in file) - 1  # exclude header
#     detection_id = row_count + 1
#     with open(csv_file, mode='a', newline='') as file:
#         writer = csv.writer(file)
#         writer.writerow([detection_id, timestamp, confidence, direction])

# def detect_ambulance(video_path, direction):
#     cap = cv2.VideoCapture(video_path)
#     start_time = time.time()

#     window_name = f'{direction} - YOLO Ambulance Detection'
#     cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
#     cv2.resizeWindow(window_name, 640, 360)

#     # VideoWriter setup
#     fourcc = cv2.VideoWriter_fourcc(*'mp4v')
#     fps = cap.get(cv2.CAP_PROP_FPS)
#     width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
#     height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

#     output_path = os.path.join(results_folder, f"{direction}_detection_output.mp4")
#     out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

#     while True:
#         ret, frame = cap.read()
#         if not ret or time.time() - start_time >= detection_duration:
#             break

#         results = model(frame)[0]

#         for box in results.boxes:
#             conf = box.conf[0].item()
#             if conf >= confidence_threshold:
#                 x1, y1, x2, y2 = map(int, box.xyxy[0])
#                 cls = int(box.cls[0].item())
#                 label = model.names[cls]

#                 cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
#                 cv2.putText(frame, f'{label} {conf:.2f}', (x1, y1 - 10),
#                             cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

#                 if label.lower() == "ambulance":
#                     ambulance_detected[direction] = True
#                     log_detection(conf, direction)

#         out.write(frame)  # write frame to video file
#         cv2.imshow(window_name, frame)
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break

#     cap.release()
#     out.release()  # release the video writer
#     cv2.destroyWindow(window_name)

# # Run detection for each direction
# for path, direction in zip(video_paths, directions):
#     detect_ambulance(path, direction)

# # Show results
# priority_directions = [dir for dir, detected in ambulance_detected.items() if detected]

# if not priority_directions:
#     messagebox.showinfo("Ambulance Priority", "No ambulance detected.")
# elif len(priority_directions) == 1:
#     messagebox.showinfo("Ambulance Priority", f"Ambulance detected in the {priority_directions[0]} direction. Give green signal.")
# else:
#     joined_dirs = ', '.join(priority_directions[:-1]) + f' and {priority_directions[-1]}'
#     messagebox.showinfo("Ambulance Priority", f"Ambulance detected in {joined_dirs} directions. Give green signal.")
