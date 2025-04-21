"""
abot_calibrated.py
Performs calibrated robot operations using external correction values.
Requires prior calibration of both straight driving and in-place rotation.
Built as a child of microbit_abot.py for refined motion control.
Repo: https://github.com/wookjin-chung/Tandem_Robotics | MIT License
@fribot.com created Apr 13, 2025
@version 0.1.0
"""
from microbit_abot import bot
from microbit import *

class CalibratedMotionBot(bot):
    def __init__(self, p=27, q=33):
        super().__init__(p, q)
        # Offsets and limits for straight driving calibration
        self.left_speed_offset = 0
        self.right_speed_offset = 0
        self.min_offset = -20
        self.max_offset = 20
        
        # Default values for in-place rotation calibration
        self.cw_magnitude = 70       # Clockwise rotation speed
        self.ccw_magnitude = -70     # Counterclockwise rotation speed
        self.base_rotation_time = 2200  # Base time required for a 360° rotation (milliseconds)
        
        self.load_offsets()
        # Store the user-defined offset values to restore later
        self._default_left_offset = self.left_speed_offset
        self._default_right_offset = self.right_speed_offset

    # Functions for saving and setting calibration offsets (for straight driving)
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

    def set_left_speed_offset(self, value):
        self.left_speed_offset = min(max(value, self.min_offset), self.max_offset)
        self.save_offsets()

    def set_right_speed_offset(self, value):
        self.right_speed_offset = min(max(value, self.min_offset), self.max_offset)
        self.save_offsets()

    # Function that applies calibration offsets to the servo motor speeds (for straight driving)
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

    # External input function for in-place rotation calibration
    def set_calibrated_speed(self, cw_speed, ccw_speed, base_rotation_time=None):
        self.cw_magnitude = cw_speed
        self.ccw_magnitude = ccw_speed
        if base_rotation_time is not None:
            self.base_rotation_time = base_rotation_time

    # Function that performs an in-place rotation
    def rotate_degrees(self, angle):
        # The rotation time is calculated proportionally to the base time required for a 360° rotation
        rotation_time = self.base_rotation_time * abs(angle) / 360
        # Rotate clockwise for positive angles and counterclockwise for negative angles
        speed = self.cw_magnitude if angle > 0 else self.ccw_magnitude
        self.servo_speed(speed, speed)
        sleep(int(rotation_time))
        self.servo_speed(0, 0)
