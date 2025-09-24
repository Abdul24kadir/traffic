# import tkinter as tk
# import time
# from tkinter import Toplevel, Label

# def calculate_green_time(vehicle_count, max_vehicles=60, min_time=10, max_time=30):
#     if vehicle_count <= 0:
#         return min_time

#     vehicle_count = min(vehicle_count, max_vehicles)
#     time_range = max_time - min_time
#     green_time = min_time + int((vehicle_count / max_vehicles) * time_range)
#     return green_time

# def start_signal_simulation_gui(vehicle_counts, root_window=None):
#     """
#     This function initializes a new Toplevel window for signal simulation and
#     schedules signal phases using `after()` for thread-safe UI updates.
#     """
#     root = Toplevel(root_window) if root_window else tk.Toplevel()
#     root.title("Traffic Signal Simulation")
#     root.geometry("500x400")
#     root.configure(bg="#1C2833")

#     title_label = Label(root, text="🚦 Smart Signal Simulation", font=("Arial", 16, "bold"), fg="white", bg="#1C2833")
#     title_label.pack(pady=10)

#     signal_label = Label(root, text="", font=("Arial", 14), fg="lime", bg="#1C2833")
#     signal_label.pack(pady=10)

#     countdown_label = Label(root, text="", font=("Arial", 32, "bold"), fg="cyan", bg="#1C2833")
#     countdown_label.pack(pady=10)

#     pedestrian_label = Label(root, text="", font=("Arial", 14, "italic"), fg="orange", bg="#1C2833")
#     pedestrian_label.pack(pady=10)

#     # Extract vehicle counts
#     east = vehicle_counts.get("east", 0)
#     west = vehicle_counts.get("west", 0)
#     north = vehicle_counts.get("north", 0)
#     south = vehicle_counts.get("south", 0)

#     ew_total = east + west
#     ns_total = north + south

#     if ns_total >= ew_total:
#         first_phase = ("North & South", "↑ ↓", max(north, south))
#         second_phase = ("East & West", "→ ←", max(east, west))
#     else:
#         first_phase = ("East & West", "→ ←", max(east, west))
#         second_phase = ("North & South", "↑ ↓", max(north, south))

#     def run_countdown(duration, on_tick, on_complete):
#         def tick(sec):
#             on_tick(sec)
#             if sec > 0:
#                 root.after(1000, lambda: tick(sec - 1))
#             else:
#                 on_complete()
#         tick(duration)

#     def run_phase(phase_name, direction, vehicle_count, next_phase=None):
#         green_time = calculate_green_time(vehicle_count)
#         signal_label.config(text=f"🟢 GREEN Signal: {phase_name} ({direction})",
#         fg="green")
#         pedestrian_label.config(text="")

#         def on_green_tick(sec): countdown_label.config(text=f"{sec}s")

#         def on_green_done():
#             signal_label.config(text=f"🟡 YELLOW Signal: {phase_name} ({direction})",
#             fg="yellow")

#             def on_yellow_tick(sec): countdown_label.config(text=f"{sec}s")

#             def on_yellow_done():
#                 signal_label.config(text=f"🔴 RED Signal: {phase_name}",
#                 fg="red")
#                 pedestrian_label.config(text="🚶 Pedestrians can cross the road now")

#                 def on_ped_tick(sec): countdown_label.config(text=f"{sec}s")

#                 def on_ped_done():
#                     pedestrian_label.config(text="")
#                     if next_phase:
#                         run_phase(*next_phase)

#                 run_countdown(5, on_ped_tick, on_ped_done)

#             run_countdown(3, on_yellow_tick, on_yellow_done)

#         run_countdown(green_time, on_green_tick, on_green_done)

#     # Start first phase
#     root.after(500, lambda: run_phase(*first_phase, next_phase=second_phase))

#     # Do not call root.mainloop() — it is handled in Main.py
# import tkinter as tk
# import time
# from tkinter import Toplevel, Label
# import csv
# import os

# def calculate_green_time(vehicle_count, max_vehicles=60, min_time=10, max_time=30):
#     if vehicle_count <= 0:
#         return min_time
#     vehicle_count = min(vehicle_count, max_vehicles)
#     time_range = max_time - min_time
#     green_time = min_time + int((vehicle_count / max_vehicles) * time_range)
#     return green_time

# def log_signal_state(phase_name, state, duration):
#     os.makedirs("results", exist_ok=True)
#     log_path = os.path.join("results", "signal_log.csv")

#     if not os.path.isfile(log_path):
#         with open(log_path, mode='w', newline='') as file:
#             writer = csv.writer(file)
#             writer.writerow(["Phase", "State", "Duration(s)", "Timestamp"])

#     with open(log_path, mode='a', newline='') as file:
#         writer = csv.writer(file)
#         writer.writerow([phase_name, state, duration, time.strftime("%Y-%m-%d %H:%M:%S")])

#     print(f"✅ Logged: {phase_name} | {state} | {duration}s")

# def start_signal_simulation_gui(vehicle_counts, root_window=None):
#     root = Toplevel(root_window) if root_window else tk.Toplevel()
#     root.title("Traffic Signal Simulation")
#     root.geometry("500x400")
#     root.configure(bg="#1C2833")

#     title_label = Label(root, text="🚦 Smart Signal Simulation", font=("Arial", 16, "bold"), fg="white", bg="#1C2833")
#     title_label.pack(pady=10)

#     signal_label = Label(root, text="", font=("Arial", 14), fg="lime", bg="#1C2833")
#     signal_label.pack(pady=10)

#     countdown_label = Label(root, text="", font=("Arial", 32, "bold"), fg="cyan", bg="#1C2833")
#     countdown_label.pack(pady=10)

#     pedestrian_label = Label(root, text="", font=("Arial", 14, "italic"), fg="orange", bg="#1C2833")
#     pedestrian_label.pack(pady=10)

#     # Extract vehicle counts
#     east = vehicle_counts.get("east", 0)
#     west = vehicle_counts.get("west", 0)
#     north = vehicle_counts.get("north", 0)
#     south = vehicle_counts.get("south", 0)

#     ew_total = east + west
#     ns_total = north + south

#     if ns_total >= ew_total:
#         first_phase = ("North & South", max(north, south))
#         second_phase = ("East & West", max(east, west))
#     else:
#         first_phase = ("East & West", max(east, west))
#         second_phase = ("North & South", max(north, south))

#     def run_countdown(duration, on_tick, on_complete):
#         def tick(sec):
#             on_tick(sec)
#             if sec > 0:
#                 root.after(1000, lambda: tick(sec - 1))
#             else:
#                 on_complete()
#         tick(duration)

#     def run_phase(phase_name, vehicle_count, next_phase=None):
#         green_time = calculate_green_time(vehicle_count)
#         signal_label.config(text=f"🟢 GREEN Signal: {phase_name}", fg="green")
#         pedestrian_label.config(text="")
#         log_signal_state(phase_name, "GREEN", green_time)

#         def on_green_tick(sec):
#             countdown_label.config(text=f"{sec}s")

#         def on_green_done():
#             signal_label.config(text=f"🟡 YELLOW Signal: {phase_name}", fg="yellow")
#             log_signal_state(phase_name, "YELLOW", 3)

#             def on_yellow_tick(sec):
#                 countdown_label.config(text=f"{sec}s")

#             def on_yellow_done():
#                 signal_label.config(text=f"🔴 RED Signal: {phase_name}", fg="red")
#                 pedestrian_label.config(text="🚶 Pedestrians can cross the road now")
#                 log_signal_state(phase_name, "RED", 5)

#                 def on_ped_tick(sec):
#                     countdown_label.config(text=f"{sec}s")

#                 def on_ped_done():
#                     pedestrian_label.config(text="")
#                     if next_phase:
#                         run_phase(*next_phase)

#                 run_countdown(5, on_ped_tick, on_ped_done)

#             run_countdown(3, on_yellow_tick, on_yellow_done)

#         run_countdown(green_time, on_green_tick, on_green_done)

#     # Start first phase
#     root.after(500, lambda: run_phase(*first_phase, next_phase=second_phase))

#     # No mainloop here — handled by caller/main.py

#############working animation1#####

# import tkinter as tk
# import time
# from tkinter import Toplevel, Label
# import csv
# import os
# import pygame
# import random

# # Constants
# SCREEN_WIDTH = 800
# SCREEN_HEIGHT = 800
# ROAD_WIDTH = 200
# JUNCTION_SIZE = 200
# VEHICLE_SIZE = (40, 80)
# VEHICLE_SPEED = 2
# SPACE_BETWEEN_VEHICLES = 90
# MAX_VEHICLES_DISPLAYED = 10

# # Stop lines
# STOP_LINE_N = 500
# STOP_LINE_S = 300
# STOP_LINE_E = 300
# STOP_LINE_W = 500

# # Logging
# def calculate_green_time(vehicle_count, max_vehicles=60, min_time=10, max_time=30):
#     if vehicle_count <= 0:
#         return min_time
#     vehicle_count = min(vehicle_count, max_vehicles)
#     time_range = max_time - min_time
#     green_time = min_time + int((vehicle_count / max_vehicles) * time_range)
#     return green_time

# def log_signal_state(phase_name, state, duration):
#     os.makedirs("results", exist_ok=True)
#     log_path = os.path.join("results", "signal_log.csv")

#     if not os.path.isfile(log_path):
#         with open(log_path, mode='w', newline='') as file:
#             writer = csv.writer(file)
#             writer.writerow(["Phase", "State", "Duration(s)", "Timestamp"])

#     with open(log_path, mode='a', newline='') as file:
#         writer = csv.writer(file)
#         writer.writerow([phase_name, state, duration, time.strftime("%Y-%m-%d %H:%M:%S")])

#     print(f"✅ Logged: {phase_name} | {state} | {duration}s")

# # Vehicle class
# class Vehicle:
#     def __init__(self, x, y, direction, image, lead=None):
#         self.image = pygame.transform.rotate(image, {
#             'N': 180, 'S': 0, 'E': 270, 'W': 90
#         }[direction])
#         self.rect = self.image.get_rect(center=(x, y))
#         self.direction = direction
#         self.lead = lead
#         self.passed_junction = False

#     def move(self, signal):
#         cx, cy = self.rect.center
#         next_pos = self.rect.copy()
#         move = False

#         if self.direction == 'E' and (cx < STOP_LINE_E or self.passed_junction or signal == 'green'):
#             move = True
#             next_pos.x += VEHICLE_SPEED
#         elif self.direction == 'W' and (cx > STOP_LINE_W or self.passed_junction or signal == 'green'):
#             move = True
#             next_pos.x -= VEHICLE_SPEED
#         elif self.direction == 'N' and (cy > STOP_LINE_N or self.passed_junction or signal == 'green'):
#             move = True
#             next_pos.y -= VEHICLE_SPEED
#         elif self.direction == 'S' and (cy < STOP_LINE_S or self.passed_junction or signal == 'green'):
#             move = True
#             next_pos.y += VEHICLE_SPEED

#         if self.lead and self.rect.colliderect(self.lead.rect.inflate(-VEHICLE_SIZE[0], -SPACE_BETWEEN_VEHICLES)):
#             return

#         if move:
#             self.rect = next_pos

#         if not self.passed_junction and self.rect.colliderect(pygame.Rect(300, 300, JUNCTION_SIZE, JUNCTION_SIZE)):
#             self.passed_junction = True

# # Signal box
# def draw_signal_box(screen, pos, state):
#     x, y = pos
#     pygame.draw.rect(screen, (30, 30, 30), (x, y, 30, 90))
#     for i, color in enumerate(['red', 'yellow', 'green']):
#         active = (color == state)
#         pygame.draw.circle(screen, (255, 0, 0) if color == 'red' and active else
#                                    (255, 255, 0) if color == 'yellow' and active else
#                                    (0, 255, 0) if color == 'green' and active else (50, 50, 50),
#                            (x+15, y+15+i*30), 10)

# def start_signal_simulation_gui(vehicle_counts, root_window=None):
#     # Normalize keys
#     directions = {'north': 'N', 'south': 'S', 'east': 'E', 'west': 'W'}
#     normalized_counts = {v: vehicle_counts.get(k, 0) for k, v in directions.items()}

#     pygame.init()
#     screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
#     pygame.display.set_caption("Smart Traffic Simulation")
#     clock = pygame.time.Clock()
#     font = pygame.font.SysFont("Arial", 24)
#     big_font = pygame.font.SysFont("Arial", 36)

#     images = [
#         pygame.transform.scale(pygame.image.load("assets/red_car.png"), VEHICLE_SIZE),
#         pygame.transform.scale(pygame.image.load("assets/blue_car.png"), VEHICLE_SIZE),
#         pygame.transform.scale(pygame.image.load("assets/yellow_car.png"), VEHICLE_SIZE),
#         pygame.transform.scale(pygame.image.load("assets/green_car.png"), VEHICLE_SIZE)
#     ]

#     vehicle_objs = []
#     for dir in ['N', 'S', 'E', 'W']:
#         count = min(normalized_counts[dir], MAX_VEHICLES_DISPLAYED)
#         offset = 0
#         lead = None
#         for _ in range(count):
#             offset += SPACE_BETWEEN_VEHICLES + random.randint(10, 40)
#             if dir == 'E':
#                 car = Vehicle(0 - offset, 390, 'E', random.choice(images), lead)
#             elif dir == 'W':
#                 car = Vehicle(SCREEN_WIDTH + offset, 370, 'W', random.choice(images), lead)
#             elif dir == 'N':
#                 car = Vehicle(410, SCREEN_HEIGHT + offset, 'N', random.choice(images), lead)
#             elif dir == 'S':
#                 car = Vehicle(390, 0 - offset, 'S', random.choice(images), lead)
#             vehicle_objs.append(car)
#             lead = car

#     ew_total = normalized_counts['E'] + normalized_counts['W']
#     ns_total = normalized_counts['N'] + normalized_counts['S']
#     phases = [('East & West', 'E', 'W'), ('North & South', 'N', 'S')] if ew_total >= ns_total else [('North & South', 'N', 'S'), ('East & West', 'E', 'W')]

#     def run_phase(name, dirs):
#         green_duration = calculate_green_time(max(normalized_counts[dirs[0]], normalized_counts[dirs[1]]))

#         for state in ['green', 'yellow', 'red']:
#             duration = green_duration if state == 'green' else 3 if state == 'yellow' else 5
#             log_signal_state(name, state.upper(), duration)
#             start_time = time.time()

#             while time.time() - start_time < duration:
#                 for event in pygame.event.get():
#                     if event.type == pygame.QUIT:
#                         pygame.quit()
#                         return

#                 screen.fill((20, 20, 20))
#                 pygame.draw.rect(screen, (50, 50, 50), (300, 0, ROAD_WIDTH, SCREEN_HEIGHT))
#                 pygame.draw.rect(screen, (50, 50, 50), (0, 300, SCREEN_WIDTH, ROAD_WIDTH))
#                 pygame.draw.rect(screen, (30, 30, 30), (300, 300, JUNCTION_SIZE, JUNCTION_SIZE), 4)
#                 draw_signal_box(screen, (50, 50), state)

#                 for v in vehicle_objs:
#                     if v.direction in dirs:
#                         v.move(state)
#                     screen.blit(v.image, v.rect)

#                 label = font.render(f"{state.upper()} Signal: {name}", True,
#                                      {'green': (0, 255, 0), 'yellow': (255, 255, 0), 'red': (255, 0, 0)}[state])
#                 countdown = int(duration - (time.time() - start_time))
#                 timer_text = big_font.render(f"{countdown}s", True, (0, 255, 255))
#                 screen.blit(label, (100, 30))
#                 screen.blit(timer_text, (100, 70))

#                 pygame.display.flip()
#                 clock.tick(60)

#     for phase in phases:
#         run_phase(phase[0], phase[1:])

#     pygame.time.wait(2000)
#     pygame.quit()

# if __name__ == '__main__':
#     dummy_counts = {'north': 4, 'south': 3, 'east': 9, 'west': 6}
#     start_signal_simulation_gui(dummy_counts)

#### finalworking animation####

# import tkinter as tk
# import time
# from tkinter import Toplevel, Label
# import csv
# import os
# import pygame
# import random

# # Constants
# SCREEN_WIDTH = 800
# SCREEN_HEIGHT = 800
# ROAD_WIDTH = 200
# JUNCTION_SIZE = 200
# VEHICLE_SIZE = (40, 80)
# VEHICLE_SPEED = 2
# SPACE_BETWEEN_VEHICLES = 90
# MAX_VEHICLES_DISPLAYED = 10

# STOP_LINE_N = 500
# STOP_LINE_S = 300
# STOP_LINE_E = 300
# STOP_LINE_W = 500

# def calculate_green_time(vehicle_count, max_vehicles=60, min_time=10, max_time=30):
#     if vehicle_count <= 0:
#         return min_time
#     vehicle_count = min(vehicle_count, max_vehicles)
#     time_range = max_time - min_time
#     green_time = min_time + int((vehicle_count / max_vehicles) * time_range)
#     return green_time

# def log_signal_state(phase_name, state, duration):
#     os.makedirs("results", exist_ok=True)
#     log_path = os.path.join("results", "signal_log.csv")

#     if not os.path.isfile(log_path):
#         with open(log_path, mode='w', newline='') as file:
#             writer = csv.writer(file)
#             writer.writerow(["Phase", "State", "Duration(s)", "Timestamp"])

#     with open(log_path, mode='a', newline='') as file:
#         writer = csv.writer(file)
#         writer.writerow([phase_name, state, duration, time.strftime("%Y-%m-%d %H:%M:%S")])

#     print(f"✅ Logged: {phase_name} | {state} | {duration}s")

# class Vehicle:
#     def __init__(self, x, y, direction, image, lead=None):
#         self.image = pygame.transform.rotate(image, {
#             'N': 180, 'S': 0, 'E': 270, 'W': 90
#         }[direction])
#         self.rect = self.image.get_rect(center=(x, y))
#         self.direction = direction
#         self.lead = lead
#         self.passed_junction = False

#     def move(self, signal):
#         cx, cy = self.rect.center
#         next_pos = self.rect.copy()
#         move = False

#         if self.direction == 'E' and (cx < STOP_LINE_E or self.passed_junction or signal == 'green'):
#             move = True
#             next_pos.x += VEHICLE_SPEED
#         elif self.direction == 'W' and (cx > STOP_LINE_W or self.passed_junction or signal == 'green'):
#             move = True
#             next_pos.x -= VEHICLE_SPEED
#         elif self.direction == 'N' and (cy > STOP_LINE_N or self.passed_junction or signal == 'green'):
#             move = True
#             next_pos.y -= VEHICLE_SPEED
#         elif self.direction == 'S' and (cy < STOP_LINE_S or self.passed_junction or signal == 'green'):
#             move = True
#             next_pos.y += VEHICLE_SPEED

#         if self.lead and self.rect.colliderect(self.lead.rect.inflate(-VEHICLE_SIZE[0], -SPACE_BETWEEN_VEHICLES)):
#             return

#         if move:
#             self.rect = next_pos

#         if not self.passed_junction and self.rect.colliderect(pygame.Rect(300, 300, JUNCTION_SIZE, JUNCTION_SIZE)):
#             self.passed_junction = True

# def draw_signal_box(screen, pos, state):
#     x, y = pos
#     pygame.draw.rect(screen, (30, 30, 30), (x, y, 30, 90))
#     for i, color in enumerate(['red', 'yellow', 'green']):
#         active = (color == state)
#         pygame.draw.circle(screen, (255, 0, 0) if color == 'red' and active else
#                                    (255, 255, 0) if color == 'yellow' and active else
#                                    (0, 255, 0) if color == 'green' and active else (50, 50, 50),
#                            (x+15, y+15+i*30), 10)

# def start_signal_simulation_gui(vehicle_counts, root_window=None):
#     directions = {'north': 'N', 'south': 'S', 'east': 'E', 'west': 'W'}
#     normalized_counts = {v: vehicle_counts.get(k, 0) for k, v in directions.items()}

#     pygame.init()
#     screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
#     pygame.display.set_caption("Smart Traffic Simulation")
#     clock = pygame.time.Clock()
#     font = pygame.font.SysFont("Arial", 20)
#     timer_font = pygame.font.SysFont("Arial", 24)
#     small_font = pygame.font.SysFont("Arial", 18)

#     images = [
#         pygame.transform.scale(pygame.image.load("assets/red_car.png"), VEHICLE_SIZE),
#         pygame.transform.scale(pygame.image.load("assets/blue_car.png"), VEHICLE_SIZE),
#         pygame.transform.scale(pygame.image.load("assets/yellow_car.png"), VEHICLE_SIZE),
#         pygame.transform.scale(pygame.image.load("assets/green_car.png"), VEHICLE_SIZE)
#     ]

#     vehicle_objs = []
#     for dir in ['N', 'S', 'E', 'W']:
#         count = min(normalized_counts[dir], MAX_VEHICLES_DISPLAYED)
#         offset = 0
#         lead = None
#         for _ in range(count):
#             offset += SPACE_BETWEEN_VEHICLES + random.randint(10, 40)
#             if dir == 'E':
#                 car = Vehicle(0 - offset, 390, 'E', random.choice(images), lead)
#             elif dir == 'W':
#                 car = Vehicle(SCREEN_WIDTH + offset, 370, 'W', random.choice(images), lead)
#             elif dir == 'N':
#                 car = Vehicle(410, SCREEN_HEIGHT + offset, 'N', random.choice(images), lead)
#             elif dir == 'S':
#                 car = Vehicle(390, 0 - offset, 'S', random.choice(images), lead)
#             vehicle_objs.append(car)
#             lead = car

#     ew_total = normalized_counts['E'] + normalized_counts['W']
#     ns_total = normalized_counts['N'] + normalized_counts['S']
#     phases = [('East & West', 'E', 'W'), ('North & South', 'N', 'S')] if ew_total >= ns_total else [('North & South', 'N', 'S'), ('East & West', 'E', 'W')]

#     def run_phase(name, dirs):
#         green_duration = calculate_green_time(max(normalized_counts[dirs[0]], normalized_counts[dirs[1]]))

#         for state in ['green', 'yellow', 'red']:
#             duration = green_duration if state == 'green' else 3 if state == 'yellow' else 5
#             log_signal_state(name, state.upper(), duration)
#             start_time = time.time()

#             while time.time() - start_time < duration:
#                 for event in pygame.event.get():
#                     if event.type == pygame.QUIT:
#                         pygame.quit()
#                         return

#                 screen.fill((20, 20, 20))
#                 pygame.draw.rect(screen, (50, 50, 50), (300, 0, ROAD_WIDTH, SCREEN_HEIGHT))
#                 pygame.draw.rect(screen, (50, 50, 50), (0, 300, SCREEN_WIDTH, ROAD_WIDTH))
#                 pygame.draw.rect(screen, (30, 30, 30), (300, 300, JUNCTION_SIZE, JUNCTION_SIZE), 4)

#                 # Top-left info box
#                 pygame.draw.rect(screen, (40, 40, 40), (40, 40, 250, 120))
#                 pygame.draw.rect(screen, (255, 255, 255), (40, 40, 250, 120), 2)

#                 draw_signal_box(screen, (50, 50), state)

#                 label = small_font.render(f"{state.upper()} Signal: {name}", True,
#                                           {'green': (0, 255, 0), 'yellow': (255, 255, 0), 'red': (255, 0, 0)}[state])
#                 screen.blit(label, (90, 50))

#                 countdown = int(duration - (time.time() - start_time))
#                 timer_text = timer_font.render(f"{countdown}s", True, (0, 255, 255))
#                 screen.blit(timer_text, (90, 75))

#                 for v in vehicle_objs:
#                     if v.direction in dirs:
#                         v.move(state)
#                     screen.blit(v.image, v.rect)

#                 pygame.display.flip()
#                 clock.tick(60)

#     for phase in phases:
#         run_phase(phase[0], phase[1:])

#     pygame.time.wait(2000)
#     pygame.quit()

# if __name__ == '__main__':
#     dummy_counts = {'north': 4, 'south': 3, 'east': 9, 'west': 6}
#     start_signal_simulation_gui(dummy_counts)


# import tkinter as tk
# import time
# from tkinter import Toplevel, Label
# import csv
# import os
# import pygame
# import random

# # Constants
# SCREEN_WIDTH = 800
# SCREEN_HEIGHT = 800
# ROAD_WIDTH = 200
# JUNCTION_SIZE = 200
# VEHICLE_SIZE = (40, 80)
# VEHICLE_SPEED = 1.5
# SPACE_BETWEEN_VEHICLES = 90
# MAX_VEHICLES_DISPLAYED = 10

# STOP_LINE_N = 500
# STOP_LINE_S = 300
# STOP_LINE_E = 300
# STOP_LINE_W = 500

# def calculate_green_time(vehicle_count, max_vehicles=60, min_time=10, max_time=30):
#     if vehicle_count <= 0:
#         return min_time
#     vehicle_count = min(vehicle_count, max_vehicles)
#     time_range = max_time - min_time
#     green_time = min_time + int((vehicle_count / max_vehicles) * time_range)
#     return green_time

# def log_signal_state(phase_name, state, duration):
#     os.makedirs("results", exist_ok=True)
#     log_path = os.path.join("results", "signal_log.csv")

#     if not os.path.isfile(log_path):
#         with open(log_path, mode='w', newline='') as file:
#             writer = csv.writer(file)
#             writer.writerow(["Phase", "State", "Duration(s)", "Timestamp"])

#     with open(log_path, mode='a', newline='') as file:
#         writer = csv.writer(file)
#         writer.writerow([phase_name, state, duration, time.strftime("%Y-%m-%d %H:%M:%S")])

#     print(f"✅ Logged: {phase_name} | {state} | {duration}s")

# class Vehicle:
#     def __init__(self, x, y, direction, image, lead=None):
#         self.image = pygame.transform.rotate(image, {
#             'N': 180, 'S': 0, 'E': 270, 'W': 90
#         }[direction])
#         self.rect = self.image.get_rect(center=(x, y))
#         self.direction = direction
#         self.lead = lead
#         self.passed_junction = False

#     def move(self, signal):
#         cx, cy = self.rect.center
#         next_pos = self.rect.copy()
#         move = False

#         if self.direction == 'E' and (cx < STOP_LINE_E or self.passed_junction or signal == 'green'):
#             move = True
#             next_pos.x += VEHICLE_SPEED
#         elif self.direction == 'W' and (cx > STOP_LINE_W or self.passed_junction or signal == 'green'):
#             move = True
#             next_pos.x -= VEHICLE_SPEED
#         elif self.direction == 'N' and (cy > STOP_LINE_N or self.passed_junction or signal == 'green'):
#             move = True
#             next_pos.y -= VEHICLE_SPEED
#         elif self.direction == 'S' and (cy < STOP_LINE_S or self.passed_junction or signal == 'green'):
#             move = True
#             next_pos.y += VEHICLE_SPEED

#         if self.lead and self.rect.colliderect(self.lead.rect.inflate(-VEHICLE_SIZE[0], -SPACE_BETWEEN_VEHICLES)):
#             return

#         if move:
#             self.rect = next_pos

#         if not self.passed_junction and self.rect.colliderect(pygame.Rect(300, 300, JUNCTION_SIZE, JUNCTION_SIZE)):
#             self.passed_junction = True

# def draw_signal_box(screen, pos, state):
#     x, y = pos
#     pygame.draw.rect(screen, (30, 30, 30), (x, y, 30, 90))
#     for i, color in enumerate(['red', 'yellow', 'green']):
#         active = (color == state)
#         pygame.draw.circle(screen, (255, 0, 0) if color == 'red' and active else
#                                    (255, 255, 0) if color == 'yellow' and active else
#                                    (0, 255, 0) if color == 'green' and active else (50, 50, 50),
#                            (x+15, y+15+i*30), 10)

# def start_signal_simulation_gui(vehicle_counts, root_window=None):
#     directions = {'north': 'N', 'south': 'S', 'east': 'E', 'west': 'W'}
#     normalized_counts = {v: vehicle_counts.get(k, 0) for k, v in directions.items()}

#     pygame.init()
#     screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
#     pygame.display.set_caption("Smart Traffic Simulation")
#     clock = pygame.time.Clock()
#     font = pygame.font.SysFont("Arial", 20)
#     timer_font = pygame.font.SysFont("Arial", 24)
#     small_font = pygame.font.SysFont("Arial", 18)

#     images = [
#         pygame.transform.scale(pygame.image.load("assets/red_car.png"), VEHICLE_SIZE),
#         pygame.transform.scale(pygame.image.load("assets/blue_car.png"), VEHICLE_SIZE),
#         pygame.transform.scale(pygame.image.load("assets/yellow_car.png"), VEHICLE_SIZE),
#         pygame.transform.scale(pygame.image.load("assets/green_car.png"), VEHICLE_SIZE)
#     ]

#     vehicle_objs = []
#     for dir in ['N', 'S', 'E', 'W']:
#         count = min(normalized_counts[dir], MAX_VEHICLES_DISPLAYED)
#         offset = 0
#         lead = None
#         for _ in range(count):
#             offset += SPACE_BETWEEN_VEHICLES + random.randint(10, 40)
#             if dir == 'E':
#                 car = Vehicle(STOP_LINE_E - offset, 390, 'E', random.choice(images), lead)
#             elif dir == 'W':
#                 car = Vehicle(STOP_LINE_W + offset, 370, 'W', random.choice(images), lead)
#             elif dir == 'N':
#                 car = Vehicle(410, STOP_LINE_N + offset, 'N', random.choice(images), lead)
#             elif dir == 'S':
#                 car = Vehicle(390, STOP_LINE_S - offset, 'S', random.choice(images), lead)
#             vehicle_objs.append(car)
#             lead = car

#     ew_total = normalized_counts['E'] + normalized_counts['W']
#     ns_total = normalized_counts['N'] + normalized_counts['S']
#     phases = [('East & West', 'E', 'W'), ('North & South', 'N', 'S')] if ew_total >= ns_total else [('North & South', 'N', 'S'), ('East & West', 'E', 'W')]

#     def run_phase(name, dirs):
#         green_duration = calculate_green_time(max(normalized_counts[dirs[0]], normalized_counts[dirs[1]]))

#         for state in ['green', 'yellow', 'red']:
#             duration = green_duration if state == 'green' else 3 if state == 'yellow' else 5
#             log_signal_state(name, state.upper(), duration)
#             start_time = time.time()

#             while time.time() - start_time < duration:
#                 for event in pygame.event.get():
#                     if event.type == pygame.QUIT:
#                         pygame.quit()
#                         return

#                 screen.fill((20, 20, 20))
#                 pygame.draw.rect(screen, (50, 50, 50), (300, 0, ROAD_WIDTH, SCREEN_HEIGHT))
#                 pygame.draw.rect(screen, (50, 50, 50), (0, 300, SCREEN_WIDTH, ROAD_WIDTH))
#                 pygame.draw.rect(screen, (30, 30, 30), (300, 300, JUNCTION_SIZE, JUNCTION_SIZE), 4)

#                 pygame.draw.rect(screen, (40, 40, 40), (40, 40, 250, 120))
#                 pygame.draw.rect(screen, (255, 255, 255), (40, 40, 250, 120), 2)

#                 draw_signal_box(screen, (50, 50), state)

#                 label = small_font.render(f"{state.upper()} Signal: {name}", True,
#                                           {'green': (0, 255, 0), 'yellow': (255, 255, 0), 'red': (255, 0, 0)}[state])
#                 screen.blit(label, (90, 50))

#                 countdown = int(duration - (time.time() - start_time))
#                 timer_text = timer_font.render(f"{countdown}s", True, (0, 255, 255))
#                 screen.blit(timer_text, (90, 75))

#                 for v in vehicle_objs:
#                     if v.direction in dirs:
#                         v.move(state)
#                     screen.blit(v.image, v.rect)

#                 pygame.display.flip()
#                 clock.tick(60)

#     for phase in phases:
#         run_phase(phase[0], phase[1:])

#     pygame.time.wait(2000)
#     pygame.quit()

# if __name__ == '__main__':
#     dummy_counts = {'north': 4, 'south': 3, 'east': 9, 'west': 6}
#     start_signal_simulation_gui(dummy_counts)

import tkinter as tk
import time
from tkinter import Toplevel, Label
import csv
import os
import pygame
import random

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
ROAD_WIDTH = 200
JUNCTION_SIZE = 200
VEHICLE_SIZE = (40, 80)
VEHICLE_SPEED = 1.5
SPACE_BETWEEN_VEHICLES = 90
MAX_VEHICLES_DISPLAYED = 10

STOP_LINE_N = 500
STOP_LINE_S = 300
STOP_LINE_E = 300
STOP_LINE_W = 500

def calculate_green_time(vehicle_count, max_vehicles=60, min_time=10, max_time=30):
    if vehicle_count <= 0:
        return min_time
    vehicle_count = min(vehicle_count, max_vehicles)
    time_range = max_time - min_time
    green_time = min_time + int((vehicle_count / max_vehicles) * time_range)
    return green_time

def log_signal_state(phase_name, state, duration):
    os.makedirs("results", exist_ok=True)
    log_path = os.path.join("results", "signal_log.csv")

    if not os.path.isfile(log_path):
        with open(log_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Phase", "State", "Duration(s)", "Timestamp"])

    with open(log_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([phase_name, state, duration, time.strftime("%Y-%m-%d %H:%M:%S")])

    print(f"✅ Logged: {phase_name} | {state} | {duration}s")

class Vehicle:
    def __init__(self, x, y, direction, image, lead=None):
        self.image = pygame.transform.rotate(image, {
            'N': 0, 'S': 180, 'E': 270, 'W': 90
        }[direction])
        self.rect = self.image.get_rect(center=(x, y))
        self.direction = direction
        self.lead = lead
        self.passed_junction = False

    def move(self, signal):
        cx, cy = self.rect.center
        next_pos = self.rect.copy()
        move = False

        if self.direction == 'E' and (cx < STOP_LINE_E or self.passed_junction or signal == 'green'):
            move = True
            next_pos.x += VEHICLE_SPEED
        elif self.direction == 'W' and (cx > STOP_LINE_W or self.passed_junction or signal == 'green'):
            move = True
            next_pos.x -= VEHICLE_SPEED
        elif self.direction == 'N' and (cy > STOP_LINE_N or self.passed_junction or signal == 'green'):
            move = True
            next_pos.y -= VEHICLE_SPEED
        elif self.direction == 'S' and (cy < STOP_LINE_S or self.passed_junction or signal == 'green'):
            move = True
            next_pos.y += VEHICLE_SPEED

        if self.lead and self.rect.colliderect(self.lead.rect.inflate(-VEHICLE_SIZE[0], -SPACE_BETWEEN_VEHICLES)):
            return

        if move:
            self.rect = next_pos

        if not self.passed_junction and self.rect.colliderect(pygame.Rect(300, 300, JUNCTION_SIZE, JUNCTION_SIZE)):
            self.passed_junction = True

def draw_signal_box(screen, pos, state):
    x, y = pos
    pygame.draw.rect(screen, (30, 30, 30), (x, y, 30, 90))
    for i, color in enumerate(['red', 'yellow', 'green']):
        active = (color == state)
        pygame.draw.circle(screen, (255, 0, 0) if color == 'red' and active else
                                   (255, 255, 0) if color == 'yellow' and active else
                                   (0, 255, 0) if color == 'green' and active else (50, 50, 50),
                           (x+15, y+15+i*30), 10)

def draw_dashed_lines(screen):
    dash_length = 15
    gap_length = 15
    line_color = (255, 255, 255)

    # Vertical line
    y = 0
    while y < SCREEN_HEIGHT:
        pygame.draw.line(screen, line_color, (400, y), (400, y + dash_length))
        y += dash_length + gap_length

    # Horizontal line
    x = 0
    while x < SCREEN_WIDTH:
        pygame.draw.line(screen, line_color, (x, 400), (x + dash_length, 400))
        x += dash_length + gap_length

def start_signal_simulation_gui(vehicle_counts, root_window=None):
    directions = {'north': 'N', 'south': 'S', 'east': 'E', 'west': 'W'}
    normalized_counts = {v: vehicle_counts.get(k, 0) for k, v in directions.items()}

    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Smart Traffic Simulation")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 20)
    timer_font = pygame.font.SysFont("Arial", 24)
    small_font = pygame.font.SysFont("Arial", 18)

    images = [
        pygame.transform.scale(pygame.image.load("assets/red_car.png"), VEHICLE_SIZE),
        pygame.transform.scale(pygame.image.load("assets/blue_car.png"), VEHICLE_SIZE),
        pygame.transform.scale(pygame.image.load("assets/yellow_car.png"), VEHICLE_SIZE),
        pygame.transform.scale(pygame.image.load("assets/green_car.png"), VEHICLE_SIZE)
    ]

    vehicle_objs = []
    for dir in ['N', 'S', 'E', 'W']:
        count = min(normalized_counts[dir], MAX_VEHICLES_DISPLAYED)
        offset = 0
        lead = None
        for _ in range(count):
            offset += SPACE_BETWEEN_VEHICLES + random.randint(10, 40)
            if dir == 'E':
                car = Vehicle(STOP_LINE_E - offset, 430, 'E', random.choice(images), lead)
            elif dir == 'W':
                car = Vehicle(STOP_LINE_W + offset, 370, 'W', random.choice(images), lead)
            elif dir == 'N':
                car = Vehicle(440, STOP_LINE_N + offset, 'N', random.choice(images), lead)
            elif dir == 'S':
                car = Vehicle(370, STOP_LINE_S - offset, 'S', random.choice(images), lead)
            vehicle_objs.append(car)
            lead = car

    ew_total = normalized_counts['E'] + normalized_counts['W']
    ns_total = normalized_counts['N'] + normalized_counts['S']
    phases = [('East & West', 'E', 'W'), ('North & South', 'N', 'S')] if ew_total >= ns_total else [('North & South', 'N', 'S'), ('East & West', 'E', 'W')]

    def draw_direction_labels():
        label_n = font.render("NORTH", True, (255, 255, 255))
        label_s = font.render("SOUTH", True, (255, 255, 255))
        label_e = font.render("EAST", True, (255, 255, 255))
        label_w = font.render("WEST", True, (255, 255, 255))
        screen.blit(label_n, (SCREEN_WIDTH // 2 - label_n.get_width() // 2, 20))
        screen.blit(label_s, (SCREEN_WIDTH // 2 - label_s.get_width() // 2, SCREEN_HEIGHT - 40))
        screen.blit(label_e, (SCREEN_WIDTH - 80, SCREEN_HEIGHT // 2 - label_e.get_height() // 2))
        screen.blit(label_w, (20, SCREEN_HEIGHT // 2 - label_w.get_height() // 2))

    def run_phase(name, dirs):
        green_duration = calculate_green_time(max(normalized_counts[dirs[0]], normalized_counts[dirs[1]]))

        for state in ['green', 'yellow', 'red']:
            duration = green_duration if state == 'green' else 3 if state == 'yellow' else 5
            log_signal_state(name, state.upper(), duration)
            start_time = time.time()

            while time.time() - start_time < duration:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        return

                screen.fill((20, 20, 20))
                pygame.draw.rect(screen, (50, 50, 50), (300, 0, ROAD_WIDTH, SCREEN_HEIGHT))
                pygame.draw.rect(screen, (50, 50, 50), (0, 300, SCREEN_WIDTH, ROAD_WIDTH))
                pygame.draw.rect(screen, (30, 30, 30), (300, 300, JUNCTION_SIZE, JUNCTION_SIZE), 4)

                draw_dashed_lines(screen)

                pygame.draw.rect(screen, (40, 40, 40), (40, 40, 250, 120))
                pygame.draw.rect(screen, (255, 255, 255), (40, 40, 250, 120), 2)

                draw_signal_box(screen, (50, 50), state)

                label = small_font.render(f"{state.upper()} Signal: {name}", True,
                                          {'green': (0, 255, 0), 'yellow': (255, 255, 0), 'red': (255, 0, 0)}[state])
                screen.blit(label, (90, 50))

                countdown = int(duration - (time.time() - start_time))
                timer_text = timer_font.render(f"{countdown}s", True, (0, 255, 255))
                screen.blit(timer_text, (90, 75))

                for v in vehicle_objs:
                    if v.direction in dirs:
                        v.move(state)
                    screen.blit(v.image, v.rect)

                draw_direction_labels()

                pygame.display.flip()
                clock.tick(60)

    for phase in phases:
        run_phase(phase[0], phase[1:])

    pygame.time.wait(2000)
    pygame.quit()

if __name__ == '__main__':
    dummy_counts = {'north': 4, 'south': 3, 'east': 9, 'west': 6}
    start_signal_simulation_gui(dummy_counts)
