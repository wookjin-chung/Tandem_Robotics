# ch5_14_cylindrical_coordinate_plot_for_ultrasonic_distance.py

import serial
import math
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import threading
import queue
import serial.tools.list_ports

# Print available serial ports (for debugging)
ports = serial.tools.list_ports.comports()
print("Available ports:")
for port, desc, hwid in sorted(ports):
    print(f"{port}: {desc}")

# Set serial port
serial_port = 'COM7'  # Change to your actual port
baud_rate = 115200

# Initialize data queue
data_queue = queue.Queue()

# Function to read serial data in a separate thread
def read_serial_data(ser, q):
    while True:
        try:
            # Read data until '.' character
            line_data = ser.read_until(b'.').decode('utf-8').strip()
            if line_data:
                q.put(line_data)
        except serial.SerialException:
            print("Serial connection lost.")
            break
        except UnicodeDecodeError:
            print("Received non-UTF-8 data.")
            continue

# Open serial port
try:
    ser = serial.Serial(serial_port, baud_rate, timeout=1)
    print(f"{serial_port} is connected.")
except serial.SerialException as e:
    print(f"Could not open serial port {serial_port}: {e}")
    exit()

# Start serial data reading thread
serial_thread = threading.Thread(target=read_serial_data, args=(ser, data_queue), daemon=True)
serial_thread.start()

# Initialize lists to store data
angles = []      # Angles in radians
distances = []   # Distances in cm

# Set up the polar plot
fig, ax = plt.subplots(figsize=(8, 8), subplot_kw={'projection': 'polar'})
line, = ax.plot([], [], 'bo-', markersize=3)  # Blue circles with lines

# Set plot title and labels
ax.set_title('Real-time Ultrasonic Sensor Scan', va='bottom')

# Set maximum visualization distance (adjustable by user)
max_rmax = 100  # Set to desired maximum distance in cm
ax.set_rmax(max_rmax)  # Set maximum radius
ax.set_rticks([20, 40, 60, 80, 100])  # Set radial ticks at 20cm intervals
ax.set_rlabel_position(-22.5)  # Adjust radial label position

ax.grid(True)

# Ensure minus signs are displayed correctly
plt.rcParams['axes.unicode_minus'] = False

# Set maximum number of data points (for memory management)
max_points = 1000

def update(frame):
    global angles, distances
    updated = False
    while not data_queue.empty():
        line_data = data_queue.get()
        # Print received data for debugging
        print(f"Received line: {line_data}")
        # Remove trailing '.' from data
        line_data = line_data.strip('.')
        try:
            angle_str, distance_str = line_data.split(',')
            angle_deg = float(angle_str)
            distance = float(distance_str)

            # Convert angle to radians
            angle_rad = math.radians(angle_deg)

            # Print parsed data for debugging
            print(f"Parsed data - Angle: {angle_deg}°, Distance: {distance} cm")

            # Clear data if angle is 0° or 180°
            if angle_deg == 0 or angle_deg == 180:
                angles.clear()
                distances.clear()
                print("Data cleared due to angle reset.")

            # Filter distance values: add data only if distance is less than or equal to max_rmax
            if distance <= max_rmax:
                angles.append(angle_rad)
                distances.append(distance)
                updated = True
            else:
                # Replace distance exceeding max_rmax with max_rmax
                angles.append(angle_rad)
                distances.append(max_rmax)
                updated = True
                print(f"Distance {distance} cm exceeds max_rmax. Replaced with {max_rmax} cm.")

            # Remove oldest data points if exceeding max_points
            if len(angles) > max_points:
                angles.pop(0)
                distances.pop(0)

        except ValueError:
            print(f"Invalid data format: {line_data}")

    if updated:
        # Update the plot with new data
        line.set_data(angles, distances)

    return line,

# Set up the animation
ani = FuncAnimation(fig, update, interval=100, blit=True)

try:
    plt.show()
except KeyboardInterrupt:
    print("Program terminated.")
finally:
    ser.close()
