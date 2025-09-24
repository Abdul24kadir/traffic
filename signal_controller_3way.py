import tkinter as tk
import time
from tkinter import Toplevel, Label
import csv
import os

def calculate_green_time(vehicle_count, max_vehicles=60, min_time=10, max_time=30):
    if vehicle_count <= 0:
        return min_time
    vehicle_count = min(vehicle_count, max_vehicles)
    time_range = max_time - min_time
    green_time = min_time + int((vehicle_count / max_vehicles) * time_range)
    return green_time

def log_signal_state(phase_name, state, duration):
    os.makedirs("results", exist_ok=True)
    log_path = os.path.join("results", "signal_log_3way.csv")

    if not os.path.isfile(log_path):
        with open(log_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Phase", "State", "Duration(s)", "Timestamp"])

    with open(log_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([phase_name, state, duration, time.strftime("%Y-%m-%d %H:%M:%S")])

    print(f"✅ Logged: {phase_name} | {state} | {duration}s")

def start_signal_simulation_gui_3way(vehicle_counts, root_window=None):
    root = Toplevel(root_window) if root_window else tk.Toplevel()
    root.title("Traffic Signal Simulation - 3 Way")
    root.geometry("500x400")
    root.configure(bg="#1C2833")

    title_label = Label(root, text="🚦 Smart 3-Way Signal Simulation", font=("Arial", 16, "bold"), fg="white", bg="#1C2833")
    title_label.pack(pady=10)

    signal_label = Label(root, text="", font=("Arial", 14), fg="lime", bg="#1C2833")
    signal_label.pack(pady=10)

    countdown_label = Label(root, text="", font=("Arial", 32, "bold"), fg="cyan", bg="#1C2833")
    countdown_label.pack(pady=10)

    pedestrian_label = Label(root, text="", font=("Arial", 14, "italic"), fg="orange", bg="#1C2833")
    pedestrian_label.pack(pady=10)

    # Extract vehicle counts
    dir1 = vehicle_counts.get("direction1", 0)
    dir2 = vehicle_counts.get("direction2", 0)
    dir3 = vehicle_counts.get("direction3", 0)

    # Create sorted phases by vehicle count descending
    phases = sorted(
        [("Direction 1", dir1), ("Direction 2", dir2), ("Direction 3", dir3)],
        key=lambda x: x[1],
        reverse=True
    )

    def run_countdown(duration, on_tick, on_complete):
        def tick(sec):
            on_tick(sec)
            if sec > 0:
                root.after(1000, lambda: tick(sec - 1))
            else:
                on_complete()
        tick(duration)

    def run_phase(phase_name, vehicle_count, next_phases):
        green_time = calculate_green_time(vehicle_count)
        signal_label.config(text=f"🟢 GREEN Signal: {phase_name}", fg="green")
        pedestrian_label.config(text="")
        log_signal_state(phase_name, "GREEN", green_time)

        def on_green_tick(sec):
            countdown_label.config(text=f"{sec}s")

        def on_green_done():
            signal_label.config(text=f"🟡 YELLOW Signal: {phase_name}", fg="yellow")
            log_signal_state(phase_name, "YELLOW", 3)

            def on_yellow_tick(sec):
                countdown_label.config(text=f"{sec}s")

            def on_yellow_done():
                signal_label.config(text=f"🔴 RED Signal: {phase_name}", fg="red")
                pedestrian_label.config(text="🚶 Pedestrians can cross now")
                log_signal_state(phase_name, "RED", 5)

                def on_ped_tick(sec):
                    countdown_label.config(text=f"{sec}s")

                def on_ped_done():
                    pedestrian_label.config(text="")
                    if next_phases:
                        run_phase(*next_phases[0], next_phases=next_phases[1:])

                run_countdown(5, on_ped_tick, on_ped_done)

            run_countdown(3, on_yellow_tick, on_yellow_done)

        run_countdown(green_time, on_green_tick, on_green_done)

    # Start first phase
    root.after(500, lambda: run_phase(*phases[0], next_phases=phases[1:]))

