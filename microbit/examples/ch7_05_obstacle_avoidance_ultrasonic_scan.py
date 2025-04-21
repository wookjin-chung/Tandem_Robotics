# ch7_05_obstacle_avoidance_ultrasonic_scan.py

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

# Movement function
def move_forward(speed_left, speed_right):
    abot.servo_speed(speed_left, speed_right)

# Main loop
while True:
    # Measure distance to the object ahead
    scan_servo.servo_angle(90)
    sleep(50)
    distance_center = ultrasonic_sensor.distance('cm') or 0
    
    if 0 < distance_center < 50:
        # As an obstacle approaches, the speed decreases
        move_forward(40, -40)
        sleep(50)
        
        # Scan left and right while moving
        angles = [60, 75, 90, 105, 120]
        distances = {}
        for angle in angles:
            scan_servo.servo_angle(angle)
            sleep(20)
            distance = ultrasonic_sensor.distance('cm') or 0
            distances[angle] = distance
            sleep(20)
        
        # Average distance left and right
        left_avg_distance = (distances.get(60, 0) + distances.get(75, 0)) / 2
        right_avg_distance = (distances.get(105, 0) + distances.get(120, 0)) / 2
        
        # The distance difference (positive if farther to the right)
        error = right_avg_distance - left_avg_distance
        
        # Gain setting for speed control
        steering_gain = 2.0  # Adjustable
        speed_adjustment = - steering_gain * error
        
        # Speed control value limit
        speed_adjustment = min(max(speed_adjustment, -20), 20)
        
        # Wheel speed control
        base_speed = 30
        speed_left = base_speed - speed_adjustment
        speed_right = -(base_speed + speed_adjustment)
        
        # Moving forward at a controlled speed
        move_forward(speed_left, speed_right)
    else:
        # No obstacles, move forward at normal speed
        move_forward(80, -80)
    
    sleep(100)
