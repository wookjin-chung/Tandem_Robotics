# ch7_11_sequential_controlled_follower.py

from microbit import *
from microbit_abot import *         # Provides basic robot control functions
from ultrasonic import *            # Provides ultrasonic sensor functions
from abot_calibrated import *       # Provides calibrated in-place rotation & servo control functions

# ===============================================
# 1. Constants and Initial Setup
# ===============================================
MIN_ANGLE = 20                 # Minimum servo angle (°)
MAX_ANGLE = 160                # Maximum servo angle (°)
STEP = 2                       # Servo angle increment (°) per iteration
MAX_SENSOR_DISTANCE = 100      # Maximum measurable distance (cm) for the ultrasonic sensor
OBJECT_THRESHOLD = 50          # Threshold distance (cm) to consider an object detected
STEERING_TARGET = 90           # Target forward direction (°)
STEERING_KP = 0.3              # Steering PD: proportional gain
STEERING_KD = 0.4              # Steering PD: derivative gain

# Kalman filter parameters (for angle estimation)
kalman_estimate = STEERING_TARGET  # Initial estimate (starts at 90°)
kalman_error = 15                  # Initial error variance (tuning parameter)
R = 15                             # Measurement noise variance (tuning parameter)
Q = 0.2                            # Process noise variance (tuning parameter)

# Distance control parameters
TARGET_DISTANCE = 20             # Desired front distance (cm)
DISTANCE_KP = -10                # Distance PD: proportional gain (negative for forward drive)
# For improved sensitivity, consider adjusting the derivative term for distance control.
DISTANCE_KD = -2                 # Distance PD: derivative gain

# ===============================================
# 2. Create Instances for Robot, Sensor, and Servo
# ===============================================
abot = CalibratedMotionBot(13, 12)
abot.servo_attachpins()          # Attach servo control pins
abot.set_left_speed_offset(-5)
abot.set_calibrated_speed(65, -66, 2200)
abot.servo_speed_calibrated(0, 0)  # Initially stopped

# Create instances for the servo motor and ultrasonic sensor
scan = bot(10)
ultrasonic_sensor = Ultrasonic(9)

display.scroll("Ready")
sleep(500)

# ===============================================
# 3. Steering Control Function (PD Control)
# ===============================================
prev_error = 0  # Previous error for derivative calculation
def steering_control(detection_angle):
    """
    Steering (PD Control):
    Rotates the robot in place based on the error between the target
    forward direction (90°) and the estimated object's angle (from the Kalman filter).
    Uses both proportional and derivative terms.
    """
    global prev_error
    display.show("R")  # Indicate rotation phase
    error = STEERING_TARGET - detection_angle
    derivative = error - prev_error
    prev_error = error
    rotation_angle = STEERING_KP * error + STEERING_KD * derivative
    # Avoid jitter: only apply if control signal is significant
    if abs(rotation_angle) > 8:
        abot.rotate_degrees(rotation_angle)
        sleep(100)

# ===============================================
# 4. Simple 1D Kalman Filter Function
# ===============================================
def kalman_update(measurement, prev_estimate, prev_err, R, Q):
    """
    Basic Kalman filter update:
      - measurement: current servo angle measurement
      - prev_estimate: previous angle estimate
      - prev_err: previous error variance
      - R: measurement noise variance
      - Q: process noise variance
    Returns: (new_estimate, new_error)
    """
    kalman_gain = prev_err / (prev_err + R)
    new_estimate = prev_estimate + kalman_gain * (measurement - prev_estimate)
    new_error = (1 - kalman_gain) * prev_err + Q
    return new_estimate, new_error

# ===============================================
# 5. Distance Control Function (Using PD Control)
# ===============================================
prev_distance_error = 0
def distance_control():
    """
    Distance Control (PD):
    Fixes the ultrasonic sensor at 90° and continuously measures the distance to the front object.
    A PD controller (using both proportional and derivative terms) maintains TARGET_DISTANCE (20cm).
    If the measured distance exceeds OBJECT_THRESHOLD (e.g., 70cm), the object is considered lost and control stops.
    """
    # Directly show a display indicator for distance control
    display.show("D")
    # Fix the servo at 90° (forward)
    scan.servo_angle(90)
    sleep(50)
    
    global prev_distance_error
    prev_distance_error = 0
    
    while True:
        dist = ultrasonic_sensor.distance('cm')
        if dist is None:
            measured = MAX_SENSOR_DISTANCE
        else:
            measured = int(dist)
            if measured > MAX_SENSOR_DISTANCE:
                measured = MAX_SENSOR_DISTANCE
        
        if measured > OBJECT_THRESHOLD:  # Object lost
            abot.servo_speed_calibrated(0, 0)
            break
        
        # Calculate the error and derivative (for PD control)
        error = TARGET_DISTANCE - measured
        derivative = error - prev_distance_error
        prev_distance_error = error
        
        speed_adjust = DISTANCE_KP * error + DISTANCE_KD * derivative
        # Limit the control signal
        if speed_adjust > 200:
            speed_adjust = 200
        elif speed_adjust < -200:
            speed_adjust = -200
        
        # Drive both motors with opposite signs for forward motion
        abot.servo_speed_calibrated(int(speed_adjust), int(-speed_adjust))
        sleep(30)

# ===============================================
# 6. Main Loop (Continuous Scanning)
# ===============================================
angle = MIN_ANGLE
scanning_direction = STEP  # Positive: increasing; negative: decreasing

while True:
    # Set the servo to the current angle and scan
    scan.servo_angle(angle)
    sleep(15)
    
    # Measure distance using ultrasonic sensor
    sensor_reading = ultrasonic_sensor.distance('cm')
    if sensor_reading is None:
        measured_distance = MAX_SENSOR_DISTANCE
    else:
        measured_distance = int(sensor_reading)
        if measured_distance > MAX_SENSOR_DISTANCE:
            measured_distance = MAX_SENSOR_DISTANCE

    display.show("C")  # Indicate scanning mode
    
    # If an object is detected (i.e., measured distance is below threshold)
    if measured_distance <= OBJECT_THRESHOLD:
        # Update the Kalman filter using the current servo angle
        kalman_estimate, kalman_error = kalman_update(angle, kalman_estimate, kalman_error, R, Q)
        print("Detected at", angle, "° with distance", measured_distance, "cm; Kalman estimate =", kalman_estimate)
        
        # Apply steering control using the Kalman estimate
        steering_control(kalman_estimate)
        
        # When the estimated angle is very close to forward (within ±2° of 90°),
        # assume the front robot is aligned and switch to distance control mode.
        if abs(kalman_estimate - STEERING_TARGET) < 2:
            distance_control()
            # When distance control ends (e.g., object is lost), resume scanning.
    else:
        # Continue scanning if no object is detected.
        pass

    # Update the servo angle for the next scan iteration.
    angle += scanning_direction
    if angle >= MAX_ANGLE:
        angle = MAX_ANGLE
        scanning_direction = -STEP  # Reverse direction at the upper bound.
    elif angle <= MIN_ANGLE:
        angle = MIN_ANGLE
        scanning_direction = STEP   # Reverse direction at the lower bound.
        
    sleep(10)  # Short delay for processing time.
