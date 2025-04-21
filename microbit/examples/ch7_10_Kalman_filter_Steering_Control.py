# ch7_10_Kalman_filter_Steering_Control.py

from microbit import *
from microbit_abot import *         # Provides basic robot control functions
from ultrasonic import *            # Provides ultrasonic sensor functions
from abot_calibrated import *       # Provides calibrated in-place rotation and servo control functions

# ===============================================
# 1. Constants and Initial Setup
# ===============================================
MIN_ANGLE = 20                 # Lower bound for servo scanning (°)
MAX_ANGLE = 160                # Upper bound for servo scanning (°)
STEP = 2                       # Increment (°) per iteration for continuous scan
MAX_SENSOR_DISTANCE = 100      # Maximum measurable distance (cm) for ultrasonic sensor
OBJECT_THRESHOLD = 50          # Distance threshold (cm) to consider an object detected
STEERING_TARGET = 90           # Target forward direction (°)
STEERING_KP = 0.3              # Proportional constant for steering control
STEERING_KD = 0.4              # Derivative constant for steering control

# Kalman filter parameters for estimating the object’s angle:
kalman_estimate = STEERING_TARGET  # Initial estimate (start at forward direction)
kalman_error = 15                  # Initial error variance (tuning parameter)
R = 15                             # Measurement noise variance (tuning parameter)
Q = 0.2                            # Process noise variance (tuning parameter)

# ===============================================
# 2. Create Instances for Robot, Sensor, and Servo
# ===============================================
# Create a robot instance for calibrated rotation and straight motion
abot = CalibratedMotionBot(13, 12)
abot.servo_attachpins()          # Attach control pins
abot.set_left_speed_offset(-5)
abot.set_calibrated_speed(65, -66, 2200)
abot.servo_speed_calibrated(0, 0)  # Start with the robot stopped

# Setup the ultrasonic sensor servo on pin 10
scan = bot(10)
ultrasonic_sensor = Ultrasonic(9)

display.scroll("Ready")
sleep(500)

# ===============================================
# 3. Steering Control Function (PD Control)
# ===============================================
prev_error = 0  # Initialize the previous error for derivative calculation
def steering_control(detection_angle):
    """
    [Steering Control - PD Control]
    Rotates the robot based on the error between the steering target (90°)
    and the estimated object angle. Both proportional and derivative terms are used.
    """
    global prev_error
    # Optionally, show "R" on the display to indicate a rotation command is being executed.
    display.show("R")
    error = STEERING_TARGET - detection_angle
    derivative = error - prev_error
    prev_error = error
    rotation_angle = STEERING_KP * error + STEERING_KD * derivative
    
    # Execute rotation if the signal is significant to avoid jitter.
    if abs(rotation_angle) > 8:
        abot.rotate_degrees(rotation_angle)
        sleep(100)

# ===============================================
# 4. Simple 1D Kalman Filter Function
# ===============================================
def kalman_update(measurement, prev_estimate, prev_error, R, Q):
    """
    Performs a basic Kalman filter update.
    
    Parameters:
      measurement    - current measurement (servo angle at which object is detected)
      prev_estimate  - previous estimate of the object angle
      prev_error     - previous error variance
      R              - measurement noise variance
      Q              - process noise variance

    Returns:
      (new_estimate, new_error) - updated estimate and error variance.
    """
    # Compute the Kalman gain.
    kalman_gain = prev_error / (prev_error + R)
    # Update the estimate with the new measurement.
    new_estimate = prev_estimate + kalman_gain * (measurement - prev_estimate)
    # Update the error variance.
    new_error = (1 - kalman_gain) * prev_error + Q
    return new_estimate, new_error

# ===============================================
# 5. Continuous Scanning Main Loop
# ===============================================
# In continuous scanning, the servo sweeps from MIN_ANGLE to MAX_ANGLE and back.
angle = MIN_ANGLE
scanning_direction = STEP  # Positive means increasing angle; negative reverses the scan.

while True:
    # Set the servo to the current angle
    scan.servo_angle(angle)
    sleep(15)
    
    # Read the ultrasonic sensor's current distance measurement
    sensor_reading = ultrasonic_sensor.distance('cm')
    if sensor_reading is None:
        measured_distance = MAX_SENSOR_DISTANCE
    else:
        measured_distance = int(sensor_reading)
        if measured_distance > MAX_SENSOR_DISTANCE:
            measured_distance = MAX_SENSOR_DISTANCE

    # Display "C" to indicate continuous scanning mode
    display.show("C")
    
    # If the measured distance is below the threshold, update the Kalman filter with the current angle.
    if measured_distance <= OBJECT_THRESHOLD:
        # Using the current servo angle as the measurement for the object’s position.
        kalman_estimate, kalman_error = kalman_update(angle, kalman_estimate, kalman_error, R, Q)
        # For debugging purposes, print the details to the serial console.
        print("Detected at", angle, "° with distance", measured_distance, "cm; Kalman estimate =", kalman_estimate)
        
        # Use the filtered angle to update the robot’s orientation.
        steering_control(kalman_estimate)
    else:
        # Optionally, you could choose to decay the Kalman filter if no detection is available.
        pass

    # Update the servo angle continuously:
    angle += scanning_direction
    if angle >= MAX_ANGLE:
        angle = MAX_ANGLE
        scanning_direction = -STEP  # Reverse direction at the upper bound.
    elif angle <= MIN_ANGLE:
        angle = MIN_ANGLE
        scanning_direction = STEP   # Reverse direction at the lower bound.

    sleep(10)  # Short pause to yield processing time.
