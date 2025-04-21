"""
abot_rotation_calibrate.py
Calibration routines for in-place rotation of the Micro:bit-Arduino robot.
Derived from abot_straight_calibrate.py for enhanced turning accuracy.
Repo: https://github.com/wookjin-chung/Tandem_Robotics | MIT License
@fribot.com created Apr 11, 2025
@version 0.1.0
"""
from microbit_abot import bot
from microbit import *

class rotationCalibratedBot(bot):
    def __init__(self, p=27, q=33):
        super().__init__(p, q)
        self.cw_magnitude = 70
        self.ccw_magnitude = -70
        self.base_rotation_time = 2200
        self.load_rotation_speeds()
        self.calibration_animation = [
            Image("90009:09090:00900:09090:90009"),
            Image("00000:09090:00900:09090:00000")
        ]
    
    def save_rotation_speeds(self, is_cw):
        try:
            cw = self.cw_magnitude
            ccw = self.ccw_magnitude
            base_time = self.base_rotation_time
            try:
                with open('rotation_speeds.txt', 'r') as f:
                    lines = f.read().strip().split('\n')
                    if len(lines) >= 3:
                        cw = int(lines[0].strip())
                        ccw = int(lines[1].strip())
                        base_time = int(lines[2].strip())
            except OSError:
                pass
            if is_cw:
                cw = self.cw_magnitude
            else:
                ccw = self.ccw_magnitude
            with open('rotation_speeds.txt', 'w') as f:
                f.write('{}\n{}\n{}\n'.format(cw, ccw, base_time))
        except OSError:
            display.scroll("Save Error")
    
    def load_rotation_speeds(self):
        try:
            with open('rotation_speeds.txt', 'r') as f:
                lines = f.read().strip().split('\n')
                if len(lines) >= 3:
                    self.cw_magnitude = int(lines[0].strip())
                    self.ccw_magnitude = int(lines[1].strip())
                    self.base_rotation_time = int(lines[2].strip())
                else:
                    display.scroll("Rot Speeds Invalid")
        except OSError:
            pass
    
    def set_calibrated_speed(self, cw_speed, ccw_speed, base_rotation_time=None):
        self.cw_magnitude = cw_speed
        self.ccw_magnitude = ccw_speed
        if base_rotation_time is not None:
            self.base_rotation_time = base_rotation_time
        try:
            with open('rotation_speeds.txt', 'w') as f:
                f.write('{}\n{}\n{}\n'.format(self.cw_magnitude, self.ccw_magnitude, self.base_rotation_time))
        except OSError:
            display.scroll("Save Error")
    
    def start_rotation(self, speed, direction=True, base_rotation_time=None):
        self.load_rotation_speeds()
        try:
            with open('rotation_speeds.txt', 'r') as f:
                lines = f.read().strip().split('\n')
        except OSError:
            lines = []
    
        if not lines or len(lines) < 3:
            if base_rotation_time is not None:
                if direction:
                    self.set_calibrated_speed(speed, self.ccw_magnitude, base_rotation_time)
                else:
                    self.set_calibrated_speed(self.cw_magnitude, speed, base_rotation_time)
                self.base_rotation_time = base_rotation_time
            else:
                if direction:
                    self.set_calibrated_speed(speed, self.ccw_magnitude)
                else:
                    self.set_calibrated_speed(self.cw_magnitude, speed)
    
        self.rotate_degrees(360 if direction else -360)
        start_time = running_time()
        while running_time() - start_time < 2000:
            if pin_logo.is_touched():
                self.servo_speed(0, 0)
                self.calibrate_rotation(is_cw=direction, base_rotation_time=None)
                start_time = running_time()
            sleep(50)
        self.servo_speed(0, 0)
    
    def calibrate_rotation(self, is_cw=True, base_rotation_time=None):
        display.scroll("Cal Start")
        animation_index = 0
        value_scrolled = False
        while True:
            if base_rotation_time is not None:
                self.base_rotation_time = base_rotation_time
    
            if button_a.is_pressed() and button_b.is_pressed():
                if is_cw:
                    self.cw_magnitude = 70
                    display.scroll("CW Reset")
                else:
                    self.ccw_magnitude = -70
                    display.scroll("CCW Reset")
                sleep(500)
                value_scrolled = False
                continue
    
            if button_a.was_pressed():
                if is_cw:
                    self.cw_magnitude = min(self.cw_magnitude + 1, 100)
                    display.scroll("CW: {}".format(self.cw_magnitude))
                else:
                    self.ccw_magnitude = max(self.ccw_magnitude - 1, -100)
                    display.scroll("CCW: {}".format(self.ccw_magnitude))
                sleep(200)
                value_scrolled = False
                continue
    
            if button_b.was_pressed():
                if is_cw:
                    self.cw_magnitude = max(self.cw_magnitude - 1, 0)
                    display.scroll("CW: {}".format(self.cw_magnitude))
                else:
                    self.ccw_magnitude = min(self.ccw_magnitude + 1, 0)
                    display.scroll("CCW: {}".format(self.ccw_magnitude))
                sleep(200)
                value_scrolled = False
                continue
    
            if pin_logo.is_touched():
                self.servo_speed(0, 0)
                display.scroll("Cal Done")
                self.save_rotation_speeds(is_cw)
                sleep(500)
                break
    
            self.servo_speed(0, 0)
            display.show(self.calibration_animation[animation_index])
            if not value_scrolled:
                if is_cw:
                    display.scroll("CW: {}".format(self.cw_magnitude))
                else:
                    display.scroll("CCW: {}".format(self.ccw_magnitude))
                value_scrolled = True
            animation_index = (animation_index + 1) % len(self.calibration_animation)
            sleep(200)
    
    def rotate_degrees(self, angle):
        rotation_time = self.base_rotation_time * abs(angle) / 360
        speed = self.cw_magnitude if angle > 0 else self.ccw_magnitude
        self.servo_speed(speed, speed)
        sleep(int(rotation_time))
        self.servo_speed(0, 0)
