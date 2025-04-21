"""
abot_straight_calibrate.py
Calibration routines for straight driving of the Micro:bit-Arduino robot.
Extends microbit_abot.py to provide precise linear movement control.
Repo: https://github.com/wookjin-chung/Tandem_Robotics | MIT License
@fribot.com created Apr 11, 2025
@version 0.1.0
"""
from microbit_abot import bot
from microbit import *

class calibratedbot(bot):
    def __init__(self, p=27, q=33):
        super().__init__(p, q)
        self.left_base_speed = 0
        self.right_base_speed = 0
        self.left_speed_offset = 0
        self.right_speed_offset = 0
        self.max_offset = 20
        self.min_offset = -20
        self.calibration_animation = [
            Image("90009:09090:00900:09090:90009"),
            Image("00000:09090:00900:09090:00000")
        ]
        self.load_offsets()
        # Store the user-defined offset values to restore later
        self._default_left_offset = self.left_speed_offset
        self._default_right_offset = self.right_speed_offset

    def save_offsets(self):
        try:
            with open('offsets.txt', 'w') as f:
                f.write('{}\n{}\n'.format(self.left_speed_offset, self.right_speed_offset))
        except OSError:
            display.scroll("Save Error")

    def load_offsets(self):
        try:
            with open('offsets.txt', 'r') as f:
                lines = f.read().split('\n')
                if len(lines) >= 2:
                    self.left_speed_offset = int(lines[0].strip())
                    self.right_speed_offset = int(lines[1].strip())
                else:
                    display.scroll("Invalid")
        except OSError:
            pass

    def calibrate(self):
        display.scroll("Cal Start")
        animation_index = 0
        prev_a = prev_b = False
        while True:
            left_speed = self.left_base_speed + self.left_speed_offset
            right_speed = self.right_base_speed + self.right_speed_offset
            left_speed = max(min(left_speed, 100), -100)
            right_speed = max(min(right_speed, 100), -100)
            self.servo_speed(left_speed, right_speed)
            a_pressed = button_a.is_pressed()
            b_pressed = button_b.is_pressed()
            if a_pressed and b_pressed and not (prev_a and prev_b):
                self.left_speed_offset = 0
                self.right_speed_offset = 0
                display.show("0")
                sleep(500)
            elif a_pressed and not prev_a:
                self.left_speed_offset = min(max(self.left_speed_offset - 1, self.min_offset), self.max_offset)
                display.show(Image.ARROW_E)
                sleep(200)
            elif b_pressed and not prev_b:
                self.right_speed_offset = min(max(self.right_speed_offset + 1, self.min_offset), self.max_offset)
                display.show(Image.ARROW_W)
                sleep(200)
            elif accelerometer.was_gesture('right'):
                display.scroll("R Off: {}".format(self.right_speed_offset))
                sleep(500)
            elif accelerometer.was_gesture('left'):
                display.scroll("L Off: {}".format(self.left_speed_offset))
                sleep(500)
            elif pin_logo.is_touched():
                self.servo_speed(0, 0)
                display.scroll("Cal Done")
                self.save_offsets()
                sleep(500)
                break
            else:
                display.show(self.calibration_animation[animation_index])
                animation_index = (animation_index + 1) % len(self.calibration_animation)
                sleep(200)
            sleep(50)
            prev_a, prev_b = a_pressed, b_pressed

    def drive_straight(self, left_base_speed, right_base_speed, duration_ms):
        self.left_base_speed = left_base_speed
        self.right_base_speed = right_base_speed
        if abs(self.left_base_speed) < 20 and abs(self.right_base_speed) < 20:
            left_speed = self.left_base_speed
            right_speed = self.right_base_speed
        elif self.left_base_speed < -20 and self.right_base_speed > 20:
            left_speed = self.left_base_speed - self.left_speed_offset
            right_speed = self.right_base_speed - self.right_speed_offset
        else:
            left_speed = self.left_base_speed + self.left_speed_offset
            right_speed = self.right_base_speed + self.right_speed_offset
        left_speed = max(min(left_speed, 100), -100)
        right_speed = max(min(right_speed, 100), -100)
        self.servo_speed(int(left_speed), int(right_speed))
        start_time = running_time()
        while running_time() - start_time < duration_ms:
            if pin_logo.is_touched():
                self.servo_speed(0, 0)
                self.calibrate()
                start_time = running_time()
            sleep(50)
        self.servo_speed(0, 0)

    def servo_speed_calibrated(self, left_base_speed, right_base_speed):
        # If both speed values are 0, reset the offset values to 0
        if left_base_speed == 0 and right_base_speed == 0:
            self.left_speed_offset = 0
            self.right_speed_offset = 0
            self.servo_speed(0, 0)
            return
        # If nonzero speed is commanded and offsets are zero, restore the stored offset values
        if self.left_speed_offset == 0 and self.right_speed_offset == 0:
            self.left_speed_offset = self._default_left_offset
            self.right_speed_offset = self._default_right_offset
        self.left_base_speed = left_base_speed
        self.right_base_speed = right_base_speed
        if abs(self.left_base_speed) < 20 and abs(self.right_base_speed) < 20:
            left_speed = self.left_base_speed
            right_speed = self.right_base_speed
        elif self.left_base_speed < -20 and self.right_base_speed > 20:
            left_speed = self.left_base_speed - self.left_speed_offset
            right_speed = self.right_base_speed - self.right_speed_offset
        else:
            left_speed = self.left_base_speed + self.left_speed_offset
            right_speed = self.right_base_speed + self.right_speed_offset
        left_speed = max(min(left_speed, 100), -100)
        right_speed = max(min(right_speed, 100), -100)
        self.servo_speed(int(left_speed), int(right_speed))

    def set_left_speed_offset(self, value):
        self.left_speed_offset = min(max(value, self.min_offset), self.max_offset)
        self.save_offsets()

    def set_right_speed_offset(self, value):
        self.right_speed_offset = min(max(value, self.min_offset), self.max_offset)
        self.save_offsets()
