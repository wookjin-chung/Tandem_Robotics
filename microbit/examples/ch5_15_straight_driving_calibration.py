# ch5_15_straight_driving_calibration.py

from microbit import *
from microbit_abot import *

left_servo_pin = 13
right_servo_pin = 12

robot = bot(left_servo_pin, right_servo_pin)
robot.servo_attachpins()

left_base_speed = 40   # servo_speed parameter value: 30-120
right_base_speed = -40
left_speed_offset = 0
right_speed_offset = 0
max_offset = 20
min_offset = -20

calibration_animation = [
    Image("90009:"
          "09090:"
          "00900:"
          "09090:"
          "90009"),
    Image("00000:"
          "09090:"
          "00900:"
          "09090:"
          "00000"),
]

def calibrate():
    global left_speed_offset, right_speed_offset
    display.scroll("Cal Start")
    animation_index = 0
    prev_button_a_state = False
    prev_button_b_state = False

    while True:
        left_speed = left_base_speed + left_speed_offset
        right_speed = right_base_speed + right_speed_offset
        left_speed = max(min(left_speed, 100), -100)
        right_speed = max(min(right_speed, 100), -100)
        robot.servo_speed(int(left_speed), int(right_speed))

        current_button_a_state = button_a.is_pressed()
        current_button_b_state = button_b.is_pressed()

        if current_button_a_state and current_button_b_state and not (prev_button_a_state and prev_button_b_state):
            left_speed_offset = 0
            right_speed_offset = 0
            display.show("0")
            sleep(500)
        elif current_button_a_state and not prev_button_a_state:
            left_speed_offset -= 1
            left_speed_offset = min(max(left_speed_offset, min_offset), max_offset)
            display.show(Image.ARROW_E)
            sleep(200)
        elif current_button_b_state and not prev_button_b_state:
            right_speed_offset += 1
            right_speed_offset = min(max(right_speed_offset, min_offset), max_offset)
            display.show(Image.ARROW_W)
            sleep(200)
        elif accelerometer.was_gesture('right'):
            display.scroll("Off: {}".format(right_speed_offset))
            sleep(500)
        elif accelerometer.was_gesture('left'):
            display.scroll("Off: {}".format(left_speed_offset))
            sleep(500)
        elif pin_logo.is_touched():
            robot.servo_speed(0, 0)
            display.scroll("Cal Done")
            sleep(500)
            break
        else:
            display.show(calibration_animation[animation_index])
            animation_index = (animation_index + 1) % len(calibration_animation)
            sleep(200)
        sleep(50)

        prev_button_a_state = current_button_a_state
        prev_button_b_state = current_button_b_state

def drive_straight(duration_ms):
    global left_speed_offset, right_speed_offset

    left_speed = left_base_speed + left_speed_offset
    right_speed = right_base_speed + right_speed_offset
    left_speed = max(min(left_speed, 100), -100)
    right_speed = max(min(right_speed, 100), -100)

    robot.servo_speed(int(left_speed), int(right_speed))

    start_time = running_time()
    while running_time() - start_time < duration_ms:
        if pin_logo.is_touched():
            robot.servo_speed(0, 0)
            calibrate()
            left_speed = left_base_speed + left_speed_offset
            right_speed = right_base_speed + right_speed_offset
            left_speed = max(min(left_speed, 100), -100)
            right_speed = max(min(right_speed, 100), -100)
            robot.servo_speed(int(left_speed), int(right_speed))
            start_time = running_time()
        sleep(50)
    robot.servo_speed(0, 0)

def main():
    robot.servo_speed(0, 0)
    sleep(500)
    display.scroll("Ready")
    while True:
        drive_straight(5000)  
        sleep(1000)  
         
main()
