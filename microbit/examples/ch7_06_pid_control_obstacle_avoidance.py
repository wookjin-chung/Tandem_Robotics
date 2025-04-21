# ch7_06_pid_control_obstacle_avoidance.py

from microbit import *
from microbit_abot import *
from ultrasonic import *

# Initialize the wheel servos on pins 13 (left) and 12 (right)
abot = bot(13, 12)
abot.servo_attachpins()

# Initialize the ultrasonic sensor on pin 9
ultrasonic_sensor = Ultrasonic(9)

# Initialize the servo for scanning on pin 10
scan_servo = bot(10)

# PID controller settings
Kp = 1.0  # Proportional gain
Ki = 0.0  # Integral gain (not used)
Kd = 0.0  # Differential gain (not used)

MAX_DISTANCE = 100  # <-- Maximum distance to clamp at 100 cm

# Movement functions
def move(speed_left, speed_right):
    abot.servo_speed(speed_left, speed_right)

def move_forward(speed_left, speed_right):
    abot.servo_speed(speed_left, speed_right)

def get_stable_distance(threshold=5, max_attempts=20):
    """
    Continuously measure with the ultrasonic sensor, and if 3 consecutive readings
    are similar (difference from the previous reading <= threshold), 
    take the average of those 3 readings as the final result.
    threshold : allowable difference (cm) between consecutive readings
    max_attempts : maximum number of measurement attempts
    """
    stable_count = 1

    # First reading
    reading = ultrasonic_sensor.distance('cm') or 0
    # Clamp the distance to MAX_DISTANCE
    if reading > MAX_DISTANCE:
        reading = MAX_DISTANCE
        
    stable_readings = [reading]

    for _ in range(max_attempts):
        new_reading = ultrasonic_sensor.distance('cm') or 0
        # Clamp the distance to MAX_DISTANCE
        if new_reading > MAX_DISTANCE:
            new_reading = MAX_DISTANCE
            
        sleep(20)  # short interval between measurements

        # If the difference from the previous reading is within the threshold,
        # consider it "similar"
        if abs(new_reading - stable_readings[-1]) <= threshold:
            stable_count += 1
            stable_readings.append(new_reading)
        else:
            # If the value changes significantly, reset
            stable_count = 1
            stable_readings = [new_reading]

        # If 3 consecutive similar values are found, stop
        if stable_count >= 3:
            break

    # If we have at least 3 readings, return the average of the last 3
    # (since they were consecutively similar)
    if len(stable_readings) >= 3:
        return sum(stable_readings[-3:]) / 3
    else:
        # If 3 consecutive similar readings were not obtained,
        # just return the average of what we have
        return sum(stable_readings) / len(stable_readings)

def measure_angle(angle):
    """
    Move the servo to the specified angle, wait 200ms for stabilization,
    then retrieve a stable distance value from the ultrasonic sensor.
    """
    scan_servo.servo_angle(angle)
    sleep(100)  # time for the servo to stabilize
    return get_stable_distance(threshold=5, max_attempts=20)
    
# Main loop
while True:
    # Base speed
    base_speed = 80
    
    # Measure distance to the object ahead
    center_distance = measure_angle(90)
    
    if 0 < center_distance < 40:
        # When an obstacle approaches, reduce speed
        base_speed = 20
        move(base_speed, -base_speed)

        left_distance = measure_angle(45)
        measure_angle(90)
        sleep(50)
        right_distance = measure_angle(135)
        measure_angle(90)

        # Error calculation
        error = right_distance - left_distance
        print(right_distance, left_distance, error)
        P = Kp * error

        # Limit the steering value
        steering = min(max(P, -20), 20)
        
        # Wheel speed control
        speed_left = base_speed - steering
        speed_right = -(base_speed + steering)
        
        # Move forward at a controlled speed
        move(speed_left, speed_right)
    else:
        # If there are no obstacles, move forward at normal speed
        move_forward(base_speed, -base_speed)
    
    sleep(100)
