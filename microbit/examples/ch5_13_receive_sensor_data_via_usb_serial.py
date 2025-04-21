# ch5_13_receive_sensor_data_via_usb_serial.py

import serial
import serial.tools.list_ports

# Print available ports
ports = serial.tools.list_ports.comports()
print("Available Ports:")
for port in ports:
    print(f"Device: {port.device}, Description: {port.description}")

serial_port = 'COM4'  # Change to the actual port
baud_rate = 115200    # Set baud rate to 115200

try:
    ser = serial.Serial(serial_port, baud_rate, timeout=1)
    print(serial_port + " is connected.")
except serial.SerialException as e:
    print(f"Cannot open serial port {serial_port}: {e}")
    ser = None

if ser:
    try:
        while True:
            line = ser.readline().decode('utf-8').strip()
            if line:
                print("received data:", line)
                try:
                    angle_str, distance_str = line.split(',')
                    angle = int(angle_str)
                    distance = float(distance_str.strip('.'))
                    print(f"angle: {angle}°, distance: {distance} cm")
                except ValueError:
                    print("wrong data format")
    except KeyboardInterrupt:
        print("closing the program.")
    finally:
        ser.close()
