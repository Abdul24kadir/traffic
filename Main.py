from threading import Thread
from tkinter import messagebox, Tk, Label, Button, filedialog, Entry, Frame, CENTER
from tkinter import *
from tkinter.filedialog import askopenfilename
from live_feed import start_single_video_feed, start_yolov8_traffic_feed
from live_feed_3way import start_yolov8_traffic_feed_3way
from signal_controller import calculate_green_time, start_signal_simulation_gui
from signal_controller_3way import start_signal_simulation_gui_3way
import tkinter as tk
import numpy as np
import cv2
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
from CannyEdgeDetector import *
import queue
import os
import skimage
import subprocess

# Login credentials
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "1234"

# Globals
result_queue = queue.Queue()
global filename
global refrence_pixels
global sample_pixels

# ---------- LOGIN WINDOW FUNCTION -----------
def verify_login():
    username = username_entry.get()
    password = password_entry.get()
    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        login_window.destroy()
        launch_main_ui()
    else:
        messagebox.showerror("Login Failed", "Invalid Username or Password")

def launch_main_ui():
    root = Tk()
    root.title("Smart Traffic Control System")
    root.state('zoomed')  # Fullscreen window
    root.configure(bg="#2C3E50")

    def rgb2gray(rgb):
        r, g, b = rgb[:,:,0], rgb[:,:,1], rgb[:,:,2]
        gray = 0.2989 * r + 0.5870 * g + 0.1140 * b
        return gray

    def uploadTrafficImage():
        global filename
        filename = filedialog.askopenfilename(initialdir="images")
        path_label.config(text=filename)

    def visualize(imgs, format=None, gray=False):
        j = 0
        plt.figure(figsize=(20, 40))
        for i, img in enumerate(imgs):
            if img.shape[0] == 3:
                img = img.transpose(1,2,0)
            plt_idx = i+1
            plt.subplot(2, 2, plt_idx)
            if j == 0:
                plt.title('Sample Image')
                plt.imshow(img, format)
                j += 1
            else:
                plt.title('Reference Image')
                plt.imshow(img, format)
        plt.show()

    def applyCanny():
        imgs = []
        img = mpimg.imread(filename)
        img = rgb2gray(img)
        imgs.append(img)
        edge = CannyEdgeDetector(imgs, sigma=1.4, kernel_size=5, lowthreshold=0.09, highthreshold=0.20, weak_pixel=100)
        imgs = edge.detect()
        for i, img in enumerate(imgs):
            if img.shape[0] == 3:
                img = img.transpose(1,2,0)
        cv2.imwrite("gray/test.png",img)
        temp = []
        img1 = mpimg.imread('gray/test.png')
        img2 = mpimg.imread('gray/refrence.png')
        temp.append(img1)
        temp.append(img2)
        visualize(temp)

    def pixelcount():
        global refrence_pixels
        global sample_pixels
        img = cv2.imread('gray/test.png', cv2.IMREAD_GRAYSCALE)
        sample_pixels = np.sum(img == 255)
        img = cv2.imread('gray/refrence.png', cv2.IMREAD_GRAYSCALE)
        refrence_pixels = np.sum(img == 255)
        messagebox.showinfo("Pixel Counts", f"Sample White Pixels: {sample_pixels}\nReference White Pixels: {refrence_pixels}")

    def timeAllocation():
        if refrence_pixels == 0:
            messagebox.showerror("Error", "Reference pixel count is zero. Check reference image.")
            return
        avg = (sample_pixels / refrence_pixels) * 100
        if avg >= 90:
            msg = "Traffic is very high: 60 secs"
        elif avg > 85:
            msg = "Traffic is high: 50 secs"
        elif avg > 75:
            msg = "Traffic is moderate: 40 secs"
        elif avg > 50:
            msg = "Traffic is low: 30 secs"
        else:
            msg = "Traffic is very low: 20 secs"
        messagebox.showinfo("Green Signal Allocation Time", msg)

    def start_feed():
        choice = messagebox.askquestion("Feed Type", "Use webcam or single video?\nClick 'No' for 4-lane video input.")
        if choice == 'yes':
            webcam_choice = messagebox.askquestion("Choose Source", "Use Webcam?\nClick 'No' to select a video file.")
            if webcam_choice == 'yes':
                Thread(target=start_single_video_feed, args=("0", lambda c: result_queue.put(('single', c))), daemon=True).start()
            else:
                video_path = filedialog.askopenfilename(initialdir="videos", title="Select Video",
                                                        filetypes=[("Video Files", "*.mp4 *.avi *.mov")])
                if video_path:
                    Thread(target=start_single_video_feed, args=(video_path, lambda c: result_queue.put(('single', c))), daemon=True).start()
        else:
            messagebox.showinfo("Select Videos", "Select 4 videos: East, West, North, South")
            paths = filedialog.askopenfilenames(initialdir="videos", title="Select 4 Lane Videos",
                                                filetypes=[("Video Files", "*.mp4 *.avi *.mov")])
            if len(paths) != 4:
                messagebox.showerror("Error", "Please select exactly 4 videos.")
                return
            Thread(target=start_yolov8_traffic_feed, args=(paths, lambda c: result_queue.put(('multi', c))), daemon=True).start()

    def start_3way_feed():
        messagebox.showinfo("Select Videos", "Select 3 videos for Direction1, Direction2, Direction3")
        paths = filedialog.askopenfilenames(initialdir="videos", title="Select 3 Videos",
                                            filetypes=[("Video Files", "*.mp4 *.avi *.mov")])
        if len(paths) != 3:
            messagebox.showerror("Error", "Please select exactly 3 videos.")
            return
        Thread(target=start_yolov8_traffic_feed_3way, args=(paths, lambda c: result_queue.put(('3way', c))), daemon=True).start()

    def process_result_queue():
        while not result_queue.empty():
            mode, result = result_queue.get()
            if mode == 'single':
                handle_single_video_result(result)
            elif mode == 'multi':
                handle_lane_video_result(result)
            elif mode == '3way':
                handle_3way_result(result)
        root.after(500, process_result_queue)

    def handle_single_video_result(count):
        messagebox.showinfo("Vehicle Count", f"Vehicles Detected: {count}")
        green_time = calculate_green_time(int(count))
        messagebox.showinfo("Green Time", f"Suggested Green Time: {green_time} seconds")

    def handle_lane_video_result(vehicle_counts):
        msg = "\n".join([f"{lane.capitalize()}: {count} vehicles" for lane, count in vehicle_counts.items()])
        messagebox.showinfo("4-Way Vehicle Counts", msg)
        start_signal_simulation_gui(vehicle_counts)

    def handle_3way_result(vehicle_counts):
        msg = "\n".join([f"{lane}: {count} vehicles" for lane, count in vehicle_counts.items()])
        messagebox.showinfo("3-Way Vehicle Counts", msg)
        start_signal_simulation_gui_3way(vehicle_counts, root_window=root)

    def detect_video():
        subprocess.Popen(["python", "detect_video.py"])

    Label(root, text="Density Based Smart Traffic Control System", fg="white", bg="#34495E",
          font=("Arial", 24, "bold"), pady=10).pack(fill=tk.X)

    button_style = {"font": ("Arial", 14, "bold"), "bg": "#2980B9", "fg": "white", "width": 40, "height": 2}

    Button(root, text="Upload Traffic Image", command=uploadTrafficImage, **button_style).pack(pady=5)
    path_label = Label(root, text="No file chosen", fg="white", bg="#2C3E50", font=("Arial", 12))
    path_label.pack()

    Button(root, text="Apply Canny Edge Detection", command=applyCanny, **button_style).pack(pady=5)
    Button(root, text="White Pixel Count", command=pixelcount, **button_style).pack(pady=5)
    Button(root, text="Calculate Green Signal Time", command=timeAllocation, **button_style).pack(pady=5)
    Button(root, text="Start 4-Way Live Traffic Simulation", command=start_feed, **button_style).pack(pady=5)
    Button(root, text="Start 3-Way Live Traffic Simulation", command=start_3way_feed, **button_style).pack(pady=5)
    Button(root, text="Ambulance Detection", command=lambda: Thread(target=detect_video, daemon=True).start(), **button_style).pack(pady=5)
    Button(root, text="Exit", command=root.destroy, bg="#E74C3C", fg="white", font=("Arial", 14, "bold"), width=40, height=2).pack(pady=10)

    root.after(500, process_result_queue)
    root.mainloop()

# ------------------ LOGIN WINDOW ------------------
login_window = Tk()
login_window.title("Admin Login")
login_window.state('zoomed')
login_window.configure(bg="#2C3E50")

login_frame = Frame(login_window, bg="#34495E", padx=30, pady=30)
login_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

Label(login_frame, text="Admin Login", fg="white", bg="#34495E", font=("Arial", 24, "bold"), pady=10).pack(pady=10)
Label(login_frame, text="Username:", bg="#34495E", fg="white", font=("Arial", 14)).pack(pady=5)
username_entry = Entry(login_frame, font=("Arial", 14))
username_entry.pack(pady=5)

Label(login_frame, text="Password:", bg="#34495E", fg="white", font=("Arial", 14)).pack(pady=5)
password_entry = Entry(login_frame, show="*", font=("Arial", 14))
password_entry.pack(pady=5)

Button(login_frame, text="Login", command=verify_login, bg="#2980B9", fg="white", font=("Arial", 14, "bold"), width=20).pack(pady=20)

login_window.mainloop()



# ###style 2


# from threading import Thread
# from tkinter import messagebox, Tk, Label, Button, filedialog, Entry, Frame, CENTER, Text, BOTH, Y, LEFT, RIGHT, WORD
# from tkinter import *
# from tkinter.filedialog import askopenfilename
# from live_feed import start_single_video_feed, start_yolov8_traffic_feed
# from live_feed_3way import start_yolov8_traffic_feed_3way
# from signal_controller import calculate_green_time, start_signal_simulation_gui
# from signal_controller_3way import start_signal_simulation_gui_3way
# import tkinter as tk
# import numpy as np
# import cv2
# import matplotlib.image as mpimg
# import matplotlib.pyplot as plt
# from CannyEdgeDetector import *
# import queue
# import os
# import subprocess

# # Login credentials
# ADMIN_USERNAME = "admin"
# ADMIN_PASSWORD = "1234"

# # Globals
# result_queue = queue.Queue()
# global filename
# global refrence_pixels
# global sample_pixels

# # ---------- LOGIN WINDOW FUNCTION -----------
# def verify_login():
#     username = username_entry.get()
#     password = password_entry.get()
#     if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
#         login_window.destroy()
#         launch_main_ui()
#     else:
#         messagebox.showerror("Login Failed", "Invalid Username or Password")

# def launch_main_ui():
#     root = Tk()
#     root.title("Smart Traffic Control System")
#     root.state('zoomed')
#     root.configure(bg="#2C3E50")

#     # Main frame division
#     main_frame = Frame(root, bg="#2C3E50")
#     main_frame.pack(fill=BOTH, expand=True)

#     left_frame = Frame(main_frame, bg="#34495E", width=400)
#     left_frame.pack(side=LEFT, fill=Y)

#     right_frame = Frame(main_frame, bg="#1C2833")
#     right_frame.pack(side=RIGHT, fill=BOTH, expand=True)

#     message_board = Text(right_frame, bg="#212F3D", fg="white", font=("Arial", 14), wrap=WORD)
#     message_board.pack(padx=20, pady=20, fill=BOTH, expand=True)

#     def log_message(message):
#         message_board.insert(END, f"{message}\n\n")
#         message_board.see(END)

#     def rgb2gray(rgb):
#         r, g, b = rgb[:,:,0], rgb[:,:,1], rgb[:,:,2]
#         gray = 0.2989 * r + 0.5870 * g + 0.1140 * b
#         return gray

#     def uploadTrafficImage():
#         global filename
#         filename = filedialog.askopenfilename(initialdir="images")
#         log_message(f"Selected Traffic Image: {filename}")

#     def visualize(imgs, format=None, gray=False):
#         j = 0
#         plt.figure(figsize=(20, 40))
#         for i, img in enumerate(imgs):
#             if img.shape[0] == 3:
#                 img = img.transpose(1,2,0)
#             plt_idx = i+1
#             plt.subplot(2, 2, plt_idx)
#             if j == 0:
#                 plt.title('Sample Image')
#                 plt.imshow(img, format)
#                 j += 1
#             else:
#                 plt.title('Reference Image')
#                 plt.imshow(img, format)
#         plt.show()

#     def applyCanny():
#         imgs = []
#         img = mpimg.imread(filename)
#         img = rgb2gray(img)
#         imgs.append(img)
#         edge = CannyEdgeDetector(imgs, sigma=1.4, kernel_size=5, lowthreshold=0.09, highthreshold=0.20, weak_pixel=100)
#         imgs = edge.detect()
#         for i, img in enumerate(imgs):
#             if img.shape[0] == 3:
#                 img = img.transpose(1,2,0)
#         cv2.imwrite("gray/test.png", img)
#         log_message("Canny Edge Detection applied and image saved.")
#         temp = []
#         img1 = mpimg.imread('gray/test.png')
#         img2 = mpimg.imread('gray/refrence.png')
#         temp.append(img1)
#         temp.append(img2)
#         visualize(temp)

#     def pixelcount():
#         global refrence_pixels
#         global sample_pixels
#         img = cv2.imread('gray/test.png', cv2.IMREAD_GRAYSCALE)
#         sample_pixels = np.sum(img == 255)
#         img = cv2.imread('gray/refrence.png', cv2.IMREAD_GRAYSCALE)
#         refrence_pixels = np.sum(img == 255)
#         log_message(f"Sample White Pixels: {sample_pixels}\nReference White Pixels: {refrence_pixels}")

#     def timeAllocation():
#         if refrence_pixels == 0:
#             log_message("Error: Reference pixel count is zero. Check reference image.")
#             return
#         avg = (sample_pixels / refrence_pixels) * 100
#         if avg >= 90:
#             msg = "Traffic is very high: 60 secs"
#         elif avg > 85:
#             msg = "Traffic is high: 50 secs"
#         elif avg > 75:
#             msg = "Traffic is moderate: 40 secs"
#         elif avg > 50:
#             msg = "Traffic is low: 30 secs"
#         else:
#             msg = "Traffic is very low: 20 secs"
#         log_message(f"Green Signal Allocation Time: {msg}")

#     def start_feed():
#         choice = messagebox.askquestion("Feed Type", "Use webcam or single video?\nClick 'No' for 4-lane video input.")
#         if choice == 'yes':
#             webcam_choice = messagebox.askquestion("Choose Source", "Use Webcam?\nClick 'No' to select a video file.")
#             if webcam_choice == 'yes':
#                 Thread(target=start_single_video_feed, args=("0", lambda c: result_queue.put(('single', c))), daemon=True).start()
#                 log_message("Started webcam feed for traffic detection.")
#             else:
#                 video_path = filedialog.askopenfilename(initialdir="videos", title="Select Video",
#                                                         filetypes=[("Video Files", "*.mp4 *.avi *.mov")])
#                 if video_path:
#                     Thread(target=start_single_video_feed, args=(video_path, lambda c: result_queue.put(('single', c))), daemon=True).start()
#                     log_message(f"Started video feed: {video_path}")
#         else:
#             log_message("Select 4 videos for East, West, North, South")
#             paths = filedialog.askopenfilenames(initialdir="videos", title="Select 4 Lane Videos",
#                                                 filetypes=[("Video Files", "*.mp4 *.avi *.mov")])
#             if len(paths) != 4:
#                 log_message("Error: Please select exactly 4 videos.")
#                 return
#             Thread(target=start_yolov8_traffic_feed, args=(paths, lambda c: result_queue.put(('multi', c))), daemon=True).start()
#             log_message("Started 4-lane traffic detection feed.")

#     def start_3way_feed():
#         log_message("Select 3 videos for Direction1, Direction2, Direction3")
#         paths = filedialog.askopenfilenames(initialdir="videos", title="Select 3 Videos",
#                                             filetypes=[("Video Files", "*.mp4 *.avi *.mov")])
#         if len(paths) != 3:
#             log_message("Error: Please select exactly 3 videos.")
#             return
#         Thread(target=start_yolov8_traffic_feed_3way, args=(paths, lambda c: result_queue.put(('3way', c))), daemon=True).start()
#         log_message("Started 3-way traffic detection feed.")

#     def detect_video():
#         subprocess.Popen(["python", "detect_video.py"])
#         log_message("Started Ambulance Detection")

#     def process_result_queue():
#         while not result_queue.empty():
#             mode, result = result_queue.get()
#             if mode == 'single':
#                 log_message(f"Vehicles Detected: {result}")
#                 green_time = calculate_green_time(int(result))
#                 log_message(f"Suggested Green Time: {green_time} seconds")
#             elif mode == 'multi':
#                 msg = "\n".join([f"{lane.capitalize()}: {count} vehicles" for lane, count in result.items()])
#                 log_message(f"4-Way Vehicle Counts:\n{msg}")
#                 start_signal_simulation_gui(result)
#             elif mode == '3way':
#                 msg = "\n".join([f"{lane}: {count} vehicles" for lane, count in result.items()])
#                 log_message(f"3-Way Vehicle Counts:\n{msg}")
#                 start_signal_simulation_gui_3way(result, root_window=root)
#         root.after(500, process_result_queue)

#     Label(left_frame, text="Smart Traffic Control", fg="white", bg="#34495E",
#           font=("Arial", 20, "bold"), pady=10).pack(pady=10)

#     button_style = {"font": ("Arial", 14, "bold"), "bg": "#2980B9", "fg": "white", "width": 25, "height": 2}

#     Button(left_frame, text="Upload Traffic Image", command=uploadTrafficImage, **button_style).pack(pady=5)
#     Button(left_frame, text="Apply Canny Edge Detection", command=applyCanny, **button_style).pack(pady=5)
#     Button(left_frame, text="White Pixel Count", command=pixelcount, **button_style).pack(pady=5)
#     Button(left_frame, text="Calculate Green Signal Time", command=timeAllocation, **button_style).pack(pady=5)
#     Button(left_frame, text="Start 4-Way Simulation", command=start_feed, **button_style).pack(pady=5)
#     Button(left_frame, text="Start 3-Way Simulation", command=start_3way_feed, **button_style).pack(pady=5)
#     Button(left_frame, text="Ambulance Detection", command=lambda: Thread(target=detect_video, daemon=True).start(), **button_style).pack(pady=5)
#     Button(left_frame, text="Exit", command=root.destroy, bg="#E74C3C", fg="white",
#            font=("Arial", 14, "bold"), width=25, height=2).pack(pady=10)

#     root.after(500, process_result_queue)
#     root.mainloop()

# # ------------------ LOGIN WINDOW ------------------
# login_window = Tk()
# login_window.title("Admin Login")
# login_window.state('zoomed')
# login_window.configure(bg="#2C3E50")

# login_frame = Frame(login_window, bg="#34495E", padx=30, pady=30)
# login_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

# Label(login_frame, text="Admin Login", fg="white", bg="#34495E", font=("Arial", 24, "bold"), pady=10).pack(pady=10)
# Label(login_frame, text="Username:", bg="#34495E", fg="white", font=("Arial", 14)).pack(pady=5)
# username_entry = Entry(login_frame, font=("Arial", 14))
# username_entry.pack(pady=5)

# Label(login_frame, text="Password:", bg="#34495E", fg="white", font=("Arial", 14)).pack(pady=5)
# password_entry = Entry(login_frame, show="*", font=("Arial", 14))
# password_entry.pack(pady=5)

# Button(login_frame, text="Login", command=verify_login, bg="#2980B9", fg="white", font=("Arial", 14, "bold"), width=20).pack(pady=20)

# login_window.mainloop()
